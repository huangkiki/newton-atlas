"""Native scalar drive reading example; syntax checked, never executed here.

Newton 1.6.1 at 713fecdc41caf0c9d726f5c016939f36e66e3dff.
Parameters illustrate API wiring, not qualified controller gains.
"""

import newton
from newton.actuators import ClampingMaxEffort, DrivePD
import warp as wp


@wp.kernel
def write_scalar_reference(
    target_q: wp.array[float],
    target_qd: wp.array[float],
    q_index: int,
    qd_index: int,
    position: float,
    velocity: float,
):
    target_q[q_index] = position
    target_qd[qd_index] = velocity


def main():
    wp.init()
    newton.use_coord_layout_targets = True  # choose before building
    builder = newton.ModelBuilder(gravity=(0.0, 0.0, -9.81))
    link = builder.add_link(label="lever")
    builder.add_shape_box(
        link,
        xform=wp.transform(wp.vec3(0.2, 0.0, 0.0), wp.quat_identity()),
        hx=0.2,
        hy=0.025,
        hz=0.025,
        cfg=newton.ModelBuilder.ShapeConfig(density=500.0),
    )
    joint = builder.add_joint_revolute(
        parent=-1,
        child=link,
        axis=newton.Axis.Z,
        parent_xform=wp.transform(wp.vec3(0.0, 0.0, 0.5), wp.quat_identity()),
        target_ke=0.0,  # avoid a second, solver-native position drive
        target_kd=0.0,
        damping=0.0,
        limit_lower=-1.0,
        limit_upper=1.0,
        label="hinge",
    )
    builder.add_articulation([joint], label="single_joint_robot")
    builder.add_actuator(
        DrivePD,
        index=builder.joint_qd_start[joint],
        pos_index=builder.joint_q_start[joint],
        kp=20.0,
        kd=2.0,
        clamping=[(ClampingMaxEffort, {"max_effort": 3.0})],
    )
    model = builder.finalize(device="cpu")
    state_0, state_1 = model.state(), model.state()
    newton.eval_fk(model, state_0.joint_q, state_0.joint_qd, state_0)
    state_1.assign(state_0)
    control = model.control()
    solver = newton.solvers.SolverXPBD(model, iterations=2)
    pipeline = newton.CollisionPipeline(model)
    contacts = pipeline.contacts()
    target_index = int(model.joint_target_q_start.numpy()[joint])
    velocity_index = int(model.joint_qd_start.numpy()[joint])
    dt = 0.002

    for _ in range(4):
        # XPBD owns maximal body state: refresh generalized feedback before PD.
        newton.eval_ik(model, state_0, state_0.joint_q, state_0.joint_qd)
        state_0.clear_forces()
        control.joint_f.zero_()  # once before this round of actuator accumulation
        wp.launch(
            write_scalar_reference,
            dim=1,
            inputs=[control.joint_target_q, control.joint_target_qd,
                    target_index, velocity_index, 0.25, 0.0],
            device=model.device,
        )
        for actuator in model.actuators:
            actuator.step(state_0, control, dt=dt)  # stateless PD, no delay
        pipeline.collide(state_0, contacts)
        solver.step(state_0, state_1, control, contacts, dt)
        state_0, state_1 = state_1, state_0

    # The resulting state and input effort are not measured tutorial results.


if __name__ == "__main__":
    main()
