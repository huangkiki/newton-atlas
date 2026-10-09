"""Read an XPBD contact buffer through native APIs; syntax checked only.

Newton 1.6.1, 713fecdc41caf0c9d726f5c016939f36e66e3dff.
No imports or this example have been executed for the lesson.

The snapshot would contain position-correction equivalent forces, with XPBD's
contact-count weighting approximation. Restitution is deliberately disabled:
its separate velocity correction is absent from update_contacts() in this
version. A single step establishes no equilibrium, physical accuracy or score.
"""

import newton
from newton.sensors import SensorContact
import warp as wp


def main():
    wp.init()
    builder = newton.ModelBuilder(up_axis=newton.Axis.Z)
    material = newton.ModelBuilder.ShapeConfig(
        density=500.0,
        mu=0.4,
        restitution=0.0,
        mu_torsional=0.0,
        mu_rolling=0.0,
        margin=0.0,
        gap=0.01,
    )
    ground = builder.add_ground_plane(cfg=material)
    body = builder.add_body(
        xform=wp.transform(wp.vec3(0.0, 0.0, 0.1), wp.quat_identity()),
        label="sphere_body",
    )
    sphere = builder.add_shape_sphere(body, radius=0.1, cfg=material)
    model = builder.finalize(device="cpu")

    # Request optional storage before allocating Contacts. SensorContact also
    # requests this attribute, but the explicit call makes the lifecycle clear.
    model.request_contact_attributes("force")
    sensor = SensorContact(
        model, sensing_shapes=[sphere], counterpart_shapes=[ground], verbose=False
    )
    solver = newton.solvers.SolverXPBD(
        model, iterations=2, enable_restitution=False,
        rigid_contact_con_weighting=True,
    )
    state_in, state_out = model.state(), model.state()
    newton.eval_fk(model, state_in.joint_q, state_in.joint_qd, state_in)
    control = model.control()
    pipeline = newton.CollisionPipeline(model, rigid_contact_max=16, verify_buffers=True)
    contacts = pipeline.contacts()

    dt = 0.001
    state_in.clear_forces()
    pipeline.collide(state_in, contacts)  # geometry at t = 0
    count = int(contacts.rigid_contact_count.numpy()[0])  # explicit host sync
    if not 0 <= count <= contacts.rigid_contact_max:
        raise ValueError("Contact overflow: refuse an incomplete solve/readback")
    solver.step(state_in, state_out, control, contacts, dt)
    solver.update_contacts(contacts)  # same buffer; no intervening collide/clear
    sensor.update(state_out, contacts)

    # Copy before the next collision pass changes contact slots. The wrench's
    # moment is accumulated about iteration-time body0 COM positions; it is
    # not an exact continuous-time measurement at the final COM.
    snapshot = {
        "geometry_time_s": 0.0,
        "step_end_time_s": dt,
        "dt_s": dt,
        "readback_kind": "xpbd_position_correction_equivalent_weighted",
        "restitution_enabled": False,
        "shape0": contacts.rigid_contact_shape0.numpy()[:count].copy(),
        "shape1": contacts.rigid_contact_shape1.numpy()[:count].copy(),
        "normal_world": contacts.rigid_contact_normal.numpy()[:count].copy(),
        "wrench_on_body0_world_N_Nm": contacts.force.numpy()[:count].copy(),
        "sphere_force_world_N": sensor.total_force.numpy().copy(),
    }
    return snapshot  # no printing, scoring, asset export or benchmark


if __name__ == "__main__":
    main()
