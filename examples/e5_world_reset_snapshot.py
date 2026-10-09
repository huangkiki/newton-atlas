"""Two-world public-buffer reset and host snapshot, for source reading only.

Newton 1.6.1 / 713fecdc41caf0c9d726f5c016939f36e66e3dff; Warp 1.18.0.
AST checked only: not imported, JIT compiled, or executed for this lesson.
No solver is created: this is not a complete episode reset or checkpoint.
"""

import newton
import warp as wp


@wp.kernel
def reset_scalar_worlds(
    selected: wp.array[wp.bool],
    coord_start: wp.array[wp.int32],
    q_default: wp.array[float],
    qd_default: wp.array[float],
    target_default: wp.array[float],
    q: wp.array[float],
    qd: wp.array[float],
    target_q: wp.array[float],
    target_qd: wp.array[float],
    effort: wp.array[float],
):
    world = wp.tid()
    if selected[world]:
        # This example has exactly one scalar revolute joint in each world.
        # Coordinate, target and DOF indices coincide ONLY for this model.
        for i in range(coord_start[world], coord_start[world + 1]):
            q[i] = q_default[i]
            qd[i] = qd_default[i]
            target_q[i] = target_default[i]
            target_qd[i] = 0.0
            effort[i] = 0.0


def main():
    wp.init()
    newton.use_coord_layout_targets = True
    template = newton.ModelBuilder()
    link = template.add_link(label="lever")
    template.add_shape_box(
        link,
        xform=wp.transform(wp.vec3(0.2, 0.0, 0.0), wp.quat_identity()),
        hx=0.2, hy=0.025, hz=0.025,
        cfg=newton.ModelBuilder.ShapeConfig(density=500.0),
    )
    hinge = template.add_joint_revolute(
        parent=-1, child=link, axis=newton.Axis.Z,
        parent_xform=wp.transform(wp.vec3(0.0, 0.0, 0.5), wp.quat_identity()),
        label="hinge",
    )
    template.add_articulation([hinge], label="robot")
    builder = newton.ModelBuilder()
    builder.add_ground_plane()  # Global shape, excluded from local joint strides.
    builder.replicate(template, 2, label_prefixes=["world0", "world1"])
    model = builder.finalize(device="cpu")
    state_0, state_1 = model.state(), model.state()
    control = model.control()  # Default clone_variables=True; independent inputs.
    pipeline = newton.CollisionPipeline(model)
    contacts = pipeline.contacts()
    selected = wp.array([True, False, False], dtype=wp.bool, device=model.device)

    # Non-default joint poses make the selective public-array write explicit.
    # No physics has advanced: generalized coordinates are authoritative here.
    state_0.joint_q.fill_(0.25)
    state_1.joint_q.fill_(0.25)
    for state in (state_0, state_1):
        wp.launch(
            reset_scalar_worlds,
            dim=model.world_count,
            inputs=[selected, model.joint_coord_world_start,
                    model.joint_q, model.joint_qd, model.joint_target_q,
                    state.joint_q, state.joint_qd, control.joint_target_q,
                    control.joint_target_qd, control.joint_f],
            device=model.device,
        )
        newton.eval_fk(model, state.joint_q, state.joint_qd, state)
    # There is no solver/cache or applied force in this construction example.
    # A live environment must also reset those owners and application history.
    contacts.clear()  # Whole batch: no contact geometry/force is now valid.

    # CPU numpy() may alias; copy() makes each retained host value independent.
    snapshot = {
        "joint_q": state_0.joint_q.numpy().copy(),
        "joint_qd": state_0.joint_qd.numpy().copy(),
        "target_q": control.joint_target_q.numpy().copy(),
        "joint_world": model.joint_world.numpy().copy(),
        "metadata": {
            "time_seconds": 0.0,
            "stage": "public reset then FK; no physics step",
            "joint_labels": list(model.joint_label),
            "position_unit": "rad", "velocity_unit": "rad/s",
            "newton_commit": "713fecdc41caf0c9d726f5c016939f36e66e3dff",
            "warp_source_commit": "f2eaed82d8d03b37bf1014cc975954067fefcf16",
            "runtime_verified": False,
            "contact_observation_valid": False,
        },
    }
    # Deliberately no file exporter, solver step, graph, policy or training loop.
    return snapshot


if __name__ == "__main__":
    main()
