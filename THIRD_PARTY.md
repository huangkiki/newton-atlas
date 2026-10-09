# 来源与许可

原创教程、脚本和程序化小模型采用本仓 [Apache-2.0](LICENSE)。引擎通过官方安装包或固定源码获取，不重授权其代码或依赖。

- 引擎：[官方 Newton Physics 项目](https://github.com/newton-physics/newton)；以其对应版本 LICENSE/NOTICE 为准。
- 教学组织参考：[Albusgive/mujoco_learning](https://github.com/Albusgive/mujoco_learning)，本次没有整仓复制其代码、图像或正文。
- 实验链接：[DexLab](https://github.com/huangkiki/Dexlab)，历史报告保留原版本、协议和范围。

新增第三方文件时记录作者、固定来源、许可证与修改情况；先核实再纳入仓库。

E1 依据固定版本的官方代码（文件头标注 Apache-2.0）与官方说明（所读 RST 文件头标注 CC-BY-4.0）进行原创解释、公式推导和语义核对，具体文件与提交见 [来源清单](docs/sources.json)。本文重组了教学顺序，并明确标出上游两处公式表述的修正依据；未将官方全文、引擎源码或外部资产纳入仓库。新增 `examples/e1_model_state.py` 为原创 primitive 例子。

E2 同样以固定官方代码/文档为依据进行原创讲解；新增的标量驱动、二连杆目标 IK 与任务阶段函数均为原创示例，未复制官方机器人资产或神经网络 checkpoint。仅链接官方示例以核对 API 与调用语义。

E3 新增原创的接触/求解/观测讲解与 API 例子；Newton 来源仍是固定提交。另核对官方 MuJoCo-Warp 3.12.0 的三个 Apache-2.0 源文件，身份记录在独立 [依赖清单](docs/e3-dependency-sources.json)，并与锁定包摘要交叉核对。未将上游源码、sdist 或第三方资产复制进本仓。
