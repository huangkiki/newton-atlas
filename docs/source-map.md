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
