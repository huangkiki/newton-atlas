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
