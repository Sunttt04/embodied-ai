# embodied-ai

控制工程 → 具身智能：32 周学习与工程仓库（2026.11 – 2027.06）

## 这个仓库是什么

- 路线图、周计划与交付物的**唯一真实来源**（Single Source of Truth）
- 代码：机器人学工具库、ROS 2 功能包、模仿学习（ACT / Diffusion Policy）训练与部署
- 目标产物：一套能在真实机械臂上跑通的抓取 pipeline + 可量化的性能对比

## 快速开始

```bash
# 1. 克隆
git clone git@github.com:<your-id>/embodied-ai.git
cd embodied-ai

# 2. 环境（示例：conda）
conda create -n ea python=3.10 -y
conda activate ea
pip install -r requirements.txt   # 尚未创建时忽略

# 3. 看进度
打开 docs/roadmap.md
```

## 目录结构

| 目录 | 用途 |
|---|---|
| `docs/` | 路线图、周计划、标定报告、实验记录 |
| `src/` | Python / C++ 源码（机器人学工具、控制器） |
| `ros2_ws/` | ROS 2 工作空间（功能包） |
| `sim/` | 仿真模型（URDF / MJCF）与场景 |
| `notebooks/` | 探索性分析与可视化 |
| `scripts/` | 环境安装、批量任务、数据处理 |
| `data/` | 数据集（**不进 git**） |
| `models/` | 权重与导出模型（**不进 git**） |

## 进度

见 [docs/roadmap.md](docs/roadmap.md)。每周一个交付物，做完打勾。

## 约定

- 提交信息：`feat: ...` / `fix: ...` / `docs: ...` / `chore: ...`
- 分支：`main` 保持可运行；功能在 `feat/w05-transform` 这类分支上开发
- 数据与权重不进仓库，用网盘/对象存储，仓库里只放**下载脚本与校验和**
