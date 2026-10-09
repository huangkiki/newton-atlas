# Newton Physics Atlas

Understand Newton Physics through native APIs, physics concepts and versioned source code.

[中文](README.md) · [Sim Atlas home](https://github.com/huangkiki/sim-atlas) · [Introductory guide](docs/guide.md) · [Curriculum](docs/curriculum.md) · [Source map](docs/source-map.md) · [Versions](docs/versions.md) · [Roadmap](docs/roadmap.md) · [Project tracker](https://github.com/users/huangkiki/projects/2)

Part of **[Sim Atlas](https://github.com/huangkiki/sim-atlas)**, an independent community learning series with two complete planned tracks: applications (modeling, control, robotics, sensing and data) and principles/source (dynamics, contact, solvers, integration and extensions).

The introductory guide and the following source-grounded lessons are available in Chinese:

- [E1: modeling, frames, state and time](docs/modeling-state-time.md) covers A1/A2: construction/import, inertia and units, state ownership, reset/snapshots, sampling and integration foundations. See the [native API example](examples/e1_model_state.py) and [static validation](docs/e1-validation.md).
- [E2: control, robotics and task interfaces](docs/control-robotics-tasks.md) covers A3/A5/A7: actuator-to-solver consumption, joint/target indexing, FK versus target IK, tool frames and phase transitions. Its [validation record](docs/e2-validation.md) distinguishes source review from execution.
- [E3: contacts, solvers and force observation](docs/contact-solvers-forces.md) covers A4/B1–B5 and the core B0 dynamics chain: material mixing, collision geometry, XPBD correction/restitution, integration and backend differences, stopping rules and force frames. The [E3 validation record](docs/e3-validation.md) retains readback limitations, including the pinned MuJoCo-Warp torque-origin mismatch.

The complete course is still in development. E1 foundations in B0/B4 are extended by E3; sensing/rendering, parallel learning interfaces and specialist solver extensions remain planned in E4–E7.

This phase prioritizes understanding engine subsystems. E1/E2/E3 examples and Python snippets are syntax checked but unexecuted. Source identity and static checks do not establish runtime or physical correctness. No new simulation campaigns, benchmarks, training or scoring are included; later experimental material will reuse [DexLab](https://github.com/huangkiki/Dexlab) with its original version and workload boundaries.

[Pinned upstream source](https://github.com/newton-physics/newton/tree/713fecdc41caf0c9d726f5c016939f36e66e3dff) · [Attribution](THIRD_PARTY.md)
