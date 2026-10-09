"""One force extension, one native solver, and a complete discrete gradient.

Source/AST reviewed against Newton 1.6.1 and Warp 1.18.0 only. Not executed.
Assumptions: one active particle, zero gravity, no contacts/elastic elements,
positive mass, constant linear drag, and an inactive velocity clamp.
See docs/extensions-boundaries.md for the analytic initial-velocity gradient.
"""

import newton
import newton.solvers
import warp as wp


@wp.kernel
def write_drag(
    velocity: wp.array[wp.vec3],
    coefficient: wp.array[float],
    force: wp.array[wp.vec3],
):
    particle = wp.tid()
    # coefficient: kg/s; velocity: m/s; force: N. Overwrite after clear_forces.
    force[particle] = -coefficient[0] * velocity[particle]


@wp.kernel
def terminal_loss(position: wp.array[wp.vec3], target: wp.vec3, loss: wp.array[float]):
    error = position[0] - target
    loss[0] = wp.dot(error, error)  # m^2; this launch has exactly one thread.


def differentiable_drag():
    """Future native execution entry; returns independent host copies, no training."""
    wp.init()
    builder = newton.ModelBuilder(gravity=(0.0, 0.0, 0.0))
    builder.add_particle(pos=(0.0, 0.0, 0.0), vel=(1.0, 0.0, 0.0), mass=1.0)
    model = builder.finalize(device="cpu", requires_grad=True)
    # SemiImplicit warns that particle-particle contact may corrupt gradients.
    # This example intentionally has no collisions, including particle pairs.
    model.particle_grid = None
    solver = newton.solvers.SolverSemiImplicit(model)
    step_count, dt = 4, 0.01
    states = [model.state(requires_grad=True) for _ in range(step_count + 1)]
    control = model.control()
    coefficient = wp.array([0.4], dtype=float, device=model.device, requires_grad=True)
    loss = wp.zeros(1, dtype=float, device=model.device, requires_grad=True)
    target = wp.vec3(0.1, 0.0, 0.0)

    tape = wp.Tape()
    with tape:
        for k in range(step_count):
            # Distinct buffers preserve every forward value for the adjoint.
            states[k].clear_forces()
            wp.launch(
                write_drag,
                dim=model.particle_count,
                inputs=[states[k].particle_qd, coefficient],
                outputs=[states[k].particle_f],
                device=model.device,
            )
            solver.step(states[k], states[k + 1], control, None, dt)
        wp.launch(
            terminal_loss,
            dim=1,
            inputs=[states[-1].particle_q, target],
            outputs=[loss],
            device=model.device,
        )
    tape.backward(loss)
    # v0 uses the initial-state chain rule; c uses the dynamics-parameter term.
    # CPU numpy() may alias storage, so keep explicit independent snapshots.
    return {
        "loss_m2": loss.numpy().copy(),
        "d_loss_d_initial_velocity_m_s": states[0].particle_qd.grad.numpy().copy(),
        "d_loss_d_drag_m2_s_per_kg": coefficient.grad.numpy().copy(),
    }


if __name__ == "__main__":
    differentiable_drag()
