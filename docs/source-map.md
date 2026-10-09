# newton-atlas 固定版本源码入口

阅读基线：`713fecdc41caf0c9d726f5c016939f36e66e3dff`。以下入口已核对官方 Git 树与文件内容身份；不是全仓审查或运行验收记录。

本阶段先理解引擎架构、建模、步进、控制、接触/求解、传感器/渲染、性能与扩展。独立实验、基准、训练和评分暂不开展，后续复用 DexLab。

| 源码文件 | 阅读目的 |
|---|---|
| [docs/guide/overview.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/guide/overview.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [docs/guide/installation.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/guide/installation.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [docs/concepts/conventions.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/concepts/conventions.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [docs/concepts/collisions.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/concepts/collisions.rst) | 区分接触几何、接触律与数值近似 |
| [docs/concepts/worlds.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/concepts/worlds.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [docs/solvers/index.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/solvers/index.rst) | 识别算法、输入状态、配置与限制 |
| [newton/_src/sim/model.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/model.py) | 核对对象职责、数据布局、参数与版本约定 |
| [newton/_src/sim/state.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/state.py) | 核对对象职责、数据布局、参数与版本约定 |
| [newton/_src/sim/builder.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/builder.py) | 核对对象职责、数据布局、参数与版本约定 |
| [newton/_src/sim/control.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/control.py) | 核对对象职责、数据布局、参数与版本约定 |
| [newton/_src/solvers/xpbd/solver_xpbd.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/xpbd/solver_xpbd.py) | 识别算法、输入状态、配置与限制 |
| [newton/_src/solvers/mujoco/solver_mujoco.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/mujoco/solver_mujoco.py) | 识别算法、输入状态、配置与限制 |
| [newton/examples/basic/example_basic_pendulum.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/examples/basic/example_basic_pendulum.py) | 理解官方最小使用顺序；本轮不执行 |

## E1 精读入口

[正文](modeling-state-time.md)的行号链接指向下面的固定文件，身份见 [sources.json](sources.json)。重点是实现分支，而不仅是 docstring。

| 文件 | 本章具体核对内容 |
|---|---|
| [newton/_src/sim/articulation.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/articulation.py) | 关节父/子变换、COM 速度换点、eval_fk/ik 的输入输出边界 |
| [newton/_src/sim/enums.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/enums.py) | body flag 与不同 joint 的坐标/速度维度 |
| [newton/_src/solvers/solver.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/solver.py) | 半隐式预测、局部惯量、kinematic 传递、base reset no-op |
| [newton/_src/utils/import_urdf.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/utils/import_urdf.py) | visual/collision 分离，显式质量、惯量与 scale |
| [newton/_src/utils/import_mjcf.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/utils/import_mjcf.py) | 角度/四元数解析，显式 inertial 与缩放 |
| [newton/_src/utils/import_usd.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/utils/import_usd.py) | 非单位 metadata 的不同路径及 legacy 刚体限制 |
| [newton/_src/geometry/inertia.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/geometry/inertia.py) | box 质量/惯量、旋转与平行轴定理 |
| [newton/_src/math/spatial.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/math/spatial.py) | Newton/Warp 空间量排列适配、换点和换系 |
| [newton/_src/solvers/xpbd/kernels.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/xpbd/kernels.py) | 以实际 COM 力臂与叉积核对 conventions 的符号冲突 |

E1 还精读上表已有的 builder.py（构建/导入/finalize）、model.py（状态/控制分配）、state.py（字段/assign）、control.py（FREE/DISTANCE 力约定）、XPBD step 与 MuJoCo reset。上游 conventions 存在本章记录的两处符号不一致，不能仅凭文件身份哈希认为其中所有公式都正确。

## E2 精读入口

[控制、机器人与任务专题](control-robotics-tasks.md)从公开导出、参数、执行分支追到输出数组。以下新增文件与 E1 的 builder/control/XPBD/MuJoCo 入口共同构成 E2 来源；仅核对所引关键分支，不宣称全文件全部功能审查。

| 文件 | 本章核对目的 |
|---|---|
| [docs/concepts/actuators.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/concepts/actuators.rst) | 原生概念、公开使用流程与当前版本限制 |
| [docs/concepts/articulations.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/concepts/articulations.rst) | 原生概念、公开使用流程与当前版本限制 |
| [docs/concepts/sites.rst](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/docs/concepts/sites.rst) | 原生概念、公开使用流程与当前版本限制 |
| [newton/_src/actuators/actuator.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/actuator.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/actuators/clamping/clamping_max_effort.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/clamping/clamping_max_effort.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/actuators/delay.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/delay.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/actuators/drives/drive_pd.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/drives/drive_pd.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/actuators/drives/drive_pid.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/drives/drive_pid.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/actuators/effort_mode_explicit.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/effort_mode_explicit.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/actuators/effort_mode_implicit.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/actuators/effort_mode_implicit.py) | Drive、Delay、Clamping、显式/隐式 effort、状态和输出生命周期 |
| [newton/_src/controllers/impl/_common.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/impl/_common.py) | 模型型端口、工具 Jacobian 换点、DLS/阻抗的实际输出与能力边界 |
| [newton/_src/controllers/impl/differential_ik/_common.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/impl/differential_ik/_common.py) | 模型型端口、工具 Jacobian 换点、DLS/阻抗的实际输出与能力边界 |
| [newton/_src/controllers/impl/differential_ik/model_based.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/impl/differential_ik/model_based.py) | 模型型端口、工具 Jacobian 换点、DLS/阻抗的实际输出与能力边界 |
| [newton/_src/controllers/impl/differential_ik/model_free.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/impl/differential_ik/model_free.py) | 模型型端口、工具 Jacobian 换点、DLS/阻抗的实际输出与能力边界 |
| [newton/_src/controllers/impl/joint_impedance/model_based.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/impl/joint_impedance/model_based.py) | 模型型端口、工具 Jacobian 换点、DLS/阻抗的实际输出与能力边界 |
| [newton/_src/controllers/joint_selection.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/joint_selection.py) | 关节 compact 映射、标签、1-DOF 限制与唯一工具 site |
| [newton/_src/controllers/tool_selection.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/controllers/tool_selection.py) | 关节 compact 映射、标签、1-DOF 限制与唯一工具 site |
| [newton/_src/sim/ik/ik_lm_optimizer.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/ik/ik_lm_optimizer.py) | 目标、residual、候选/采样、LM 与 scalar 限位的实现 |
| [newton/_src/sim/ik/ik_objectives.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/ik/ik_objectives.py) | 目标、residual、候选/采样、LM 与 scalar 限位的实现 |
| [newton/_src/sim/ik/ik_solver.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/sim/ik/ik_solver.py) | 目标、residual、候选/采样、LM 与 scalar 限位的实现 |
| [newton/_src/solvers/featherstone/kernels.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/featherstone/kernels.py) | 目标/广义力的具体消费者、内置驱动与限位路径 |
| [newton/_src/solvers/featherstone/solver_featherstone.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/featherstone/solver_featherstone.py) | 目标/广义力的具体消费者、内置驱动与限位路径 |
| [newton/_src/solvers/mujoco/kernels.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/mujoco/kernels.py) | 目标/广义力的具体消费者、内置驱动与限位路径 |
| [newton/_src/solvers/semi_implicit/kernels_body.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/semi_implicit/kernels_body.py) | 目标/广义力的具体消费者、内置驱动与限位路径 |
| [newton/_src/solvers/semi_implicit/solver_semi_implicit.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/_src/solvers/semi_implicit/solver_semi_implicit.py) | 目标/广义力的具体消费者、内置驱动与限位路径 |
| [newton/actuators.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/actuators.py) | 公开导出与实验性 API 边界，防止把内部 helper 当公共入口 |
| [newton/controllers.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/controllers.py) | 公开导出与实验性 API 边界，防止把内部 helper 当公共入口 |
| [newton/examples/controllers/example_controller_differential_ik.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/examples/controllers/example_controller_differential_ik.py) | 核对官方示例是运动学展示还是物理执行；不运行、不复制资产 |
| [newton/examples/ik/example_ik_franka.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/examples/ik/example_ik_franka.py) | 核对官方示例是运动学展示还是物理执行；不运行、不复制资产 |
| [newton/ik.py](https://github.com/newton-physics/newton/blob/713fecdc41caf0c9d726f5c016939f36e66e3dff/newton/ik.py) | 公开导出与实验性 API 边界，防止把内部 helper 当公共入口 |

E2 特别区分：`eval_ik` 状态重建与 `newton.ik.IKSolver` 目标优化；controller 输出接 State 的展示与接 Control 的动力学链；模型 effort_limit、单 actuator clamp 和任意外部力输入的不同作用范围。
