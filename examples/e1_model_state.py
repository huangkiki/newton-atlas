"""E1 native API reading example. Syntax checked; never executed for this lesson.

One offset primitive illustrates COM, state ownership and cold reset.
This is not a benchmark or a verified physical experiment.
Source baseline: Newton 1.6.1, 713fecdc41caf0c9d726f5c016939f36e66e3dff.
"""

import newton
import warp as wp


def main():
    wp.init()
    builder = newton.ModelBuilder(
        up_axis=newton.Axis.Z, gravity=(0.0, 0.0, -9.81)
    )
    body = builder.add_body(
        xform=wp.transform(wp.vec3(0.0, 0.0, 1.0), wp.quat_identity()),
        label="offset_box",
    )
    builder.add_shape_box(
        body,
        xform=wp.transform(wp.vec3(0.10, 0.0, 0.0), wp.quat_identity()),
        hx=0.10,
        hy=0.05,
        hz=0.025,
        cfg=newton.ModelBuilder.ShapeConfig(density=1000.0),
    )
    builder.add_ground_plane()
    model = builder.finalize(device="cpu")
    solver = newton.solvers.SolverXPBD(model, iterations=2, angular_damping=0.0)
    state_0 = model.state()
    state_1 = model.state()
    control = model.control()
    pipeline = newton.CollisionPipeline(model)
    contacts = pipeline.contacts()

    # FK writes maximal body fields; State's initial joint arrays already exist.
    newton.eval_fk(model, state_0.joint_q, state_0.joint_qd, state_0)
    state_1.assign(state_0)
    initial_state = model.state()
    initial_state.assign(state_0)  # independent device arrays, not an alias
    initial_pose = wp.clone(state_0.body_q)  # pose-only history is narrower

    frame_dt = 1.0 / 60.0
    substeps = 4
    dt = frame_dt / substeps
    sim_time = 0.0  # application clock; not stored in State

    for _ in range(substeps):
        state_0.clear_forces()
        # Any per-step body/particle forces belong here, after clear_forces.
        pipeline.collide(state_0, contacts)  # geometry sampled at sim_time
        solver.step(state_0, state_1, control, contacts, dt)
        state_0, state_1 = state_1, state_0
        sim_time += dt

    # XPBD advances body fields. Reconstruct generalized coordinates explicitly.
    newton.eval_ik(model, state_0, state_0.joint_q, state_0.joint_qd)
    # Recompute geometry if a consumer requires contacts at the final pose.
    pipeline.collide(state_0, contacts)

    # Restore t=0 public state in both buffers, and rebuild independent inputs.
    # Recreating the solver is a cold reset, not arbitrary checkpoint replay.
    state_0.assign(initial_state)
    state_1.assign(initial_state)
    state_0.clear_forces()
    state_1.clear_forces()
    control = model.control()
    solver = newton.solvers.SolverXPBD(model, iterations=2, angular_damping=0.0)
    pipeline = newton.CollisionPipeline(model)
    contacts = pipeline.contacts()
    pipeline.collide(state_0, contacts)
    sim_time = 0.0
    # The pose clone is independent; it contains no velocities or solver history.
    del initial_pose


if __name__ == "__main__":
    main()
