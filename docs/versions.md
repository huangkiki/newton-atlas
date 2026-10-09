# 版本与证据边界

| 身份 | 当前记录 |
|---|---|
| 阅读版本 | 1.6.1；关联 Warp 候选版本 1.18.0 |
| 官方源码 | [newton-physics/newton](https://github.com/newton-physics/newton/tree/713fecdc41caf0c9d726f5c016939f36e66e3dff) |
| 固定提交 | `713fecdc41caf0c9d726f5c016939f36e66e3dff` |
| 源文件身份 | [sources.json](sources.json) 中的 Git blob 已与下载文件核对 |
| 已完成检查范围 | 文档相对链接、固定来源与源码文件身份；API 片段只做语法检查 |
| 原生运行与实验 | 本阶段未开展 |
| 专题交付 | [E1](modeling-state-time.md) 的 A1/A2 已交付；B0/B4 核心由 E1/E3 展开，[E2](control-robotics-tasks.md) 的 A3/A5/A7 已交付；[E3](contact-solvers-forces.md) 的 A4/B1–B5 核心已交付；[E4](sensors-rendering.md) 的 A6 已交付；其他专题见[课程目录](curriculum.md) |

固定文件身份不能证明整个引擎已审查，也不能证明候选二进制与源码具有相同构建配置。核心、绑定、插件和宿主身份分别记录。当前版本的默认值不用于补填 DexLab 历史配置。

[DexLab](https://github.com/huangkiki/Dexlab) 保留实验版本与协议；本仓不修改或追认其结果。

E3 为核对后端读回与停止条件，单列 [MuJoCo-Warp 3.12.0 源码依赖身份](e3-dependency-sources.json)：其官方固定 commit 与 Newton 固定 uv.lock 中 sdist 的文件逐字一致。这不证明本机安装版本、运行配置或历史 DexLab 依赖；不会用该依赖版本替换 Newton 的引擎版本。

E4 读取固定 Newton adapter 的 sensing/rendering/viewer 实现；OVRTX、OVStage、USD、Rerun、Viser、pyglet 和驱动仍有独立版本身份，本轮没有安装、窗口或渲染验收。Camera/IMU 示例与源审不能作为真实传感器模型的标定或资格证据。
