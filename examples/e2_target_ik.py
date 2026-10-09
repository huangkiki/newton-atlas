"""Native target-IK API example; syntax checked, never executed here.

Two scalar joints avoid conflating quaternion coordinates with scalar limits.
No physics step, external asset, viewer or task-success claim is included.
Source: Newton 1.6.1, 713fecdc41caf0c9d726f5c016939f36e66e3dff.
"""

import newton
import newton.ik as ik
import warp as wp


def main():
    wp.init()
    builder = newton.ModelBuilder()
    links = []
    joints = []
    for index in range(2):
        link = builder.add_link(label=f"link_{index}")
        builder.add_shape_box(
            link,
            xform=wp.transform(wp.vec3(0.2, 0.0, 0.0), wp.quat_identity()),
            hx=0.2,
            hy=0.025,
            hz=0.025,
        )
        joint = builder.add_joint_revolute(
            parent=-1 if index == 0 else links[-1],
            child=link,
            axis=newton.Axis.Z,
            parent_xform=wp.transform(
                wp.vec3(0.0, 0.0, 0.5) if index == 0 else wp.vec3(0.4, 0.0, 0.0),
                wp.quat_identity(),
            ),
            limit_lower=-2.5,
            limit_upper=2.5,
            label=f"hinge_{index}",
        )
        links.append(link)
        joints.append(joint)
    builder.add_articulation(joints, label="planar_arm")
    builder.joint_q[builder.joint_q_start[joints[0]]] = 0.2
    builder.joint_q[builder.joint_q_start[joints[1]]] = -0.4
    tool_offset = wp.vec3(0.4, 0.0, 0.0)
    builder.add_site(
        links[-1],
        xform=wp.transform(tool_offset, wp.quat_identity()),
        label="tcp",
    )
    model = builder.finalize(device="cpu")
    position = ik.IKObjectivePosition(
        link_index=links[-1],
        link_offset=tool_offset,
        target_positions=wp.array([wp.vec3(0.65, 0.15, 0.5)], dtype=wp.vec3,
                                  device=model.device),
    )
    limits = ik.IKObjectiveJointLimit(
        model.joint_limit_lower, model.joint_limit_upper, weight=10.0
    )
    solver = ik.IKSolver(
        model,
        n_problems=1,
        objectives=[position, limits],
        optimizer=ik.IKOptimizer.LM,
        jacobian_mode=ik.IKJacobianType.ANALYTIC,
        sampler=ik.IKSampler.NONE,
    )
    # Clone first: reshape alone would alias Model's initial coordinates.
    seed = wp.clone(model.joint_q).reshape((1, model.joint_coord_count))
    candidate = wp.empty_like(seed)
    solver.step(seed, candidate, iterations=20)

    # Separate kinematic preview. Do not overwrite an executing physics State.
    preview = model.state()
    preview.joint_q.assign(candidate.reshape((model.joint_coord_count,)))
    preview.joint_qd.zero_()
    newton.eval_fk(model, preview.joint_q, preview.joint_qd, preview)
    # A future caller must inspect residuals/limits/collisions, then generate a
    # trajectory and drive Control. This file makes no convergence claim.


if __name__ == "__main__":
    main()
