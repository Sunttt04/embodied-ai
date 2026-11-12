# 开发环境记录

> 记录本机具身智能开发环境的搭建过程、版本号与踩坑。
> 换机器时按本文档可以 30 分钟内复现。

## 1. 硬件与系统

| 项 | 值 |
|---|---|
| 机型 | 笔记本（Windows 11，build 26200） |
| GPU | NVIDIA GeForce RTX 3060 **Laptop**，**6 GB** 显存 |
| 显卡驱动 | 546.30 |
| 磁盘 | C: 约 52 GB 可用；D: 约 48 GB 可用；WSL 虚拟盘在 D 盘 |
| 结论 | **显卡只够推理和小实验，训练一律上云**（AutoDL 4090） |

## 2. 最终环境

| 组件 | 版本 | 说明 |
|---|---|---|
| WSL | 3.0.5.0 | 内核 6.18.58.1 |
| Ubuntu | 22.04.1 LTS | 安装在 `D:\wsl\Ubuntu-22.04` |
| 默认用户 | `suntong` | uid 1000，在 sudo 组 |
| Miniconda | 26.9.4 | `/home/suntong/miniconda3` |
| conda 环境 | `ea` | Python **3.10.22** |
| PyTorch | **2.7.1+cu126** | CUDA 12.6 |
| CUDA 可用性 | **True** | 通过 `scripts/check_env.py` 验证 |
| VS Code | 1.145.3 | 已装 Remote-WSL 扩展 |
| 基础工具 | git 2.34.1 / cmake 3.22.1 / gcc 11.4.0 | build-essential、curl、wget、unzip、htop、tmux |

## 3. 安装步骤

### 3.1 卸载 VirtualBox

- [x] 卸载 Oracle VirtualBox 7.2.6
- **原因**：VirtualBox 在 Windows 宿主上**没有 NVIDIA GPU 直通**，`torch.cuda.is_available()` 永远为 False；且它与 WSL2 所需的 Hyper-V 争抢 VT-x，会报 `VERR_VMX_NO_VMX`

### 3.2 安装 WSL2（离线包路线）

- [x] 启用功能：`dism /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`
- [x] 启用功能：`... /featurename:VirtualMachinePlatform ...`
- [x] 重启
- [x] 下载 AppxBundle（1065 MB）→ 解包取 `install.tar.gz` → `wsl --import Ubuntu-22.04 D:\wsl\Ubuntu-22.04 <tar> --version 2`
- **注意**：Store 版 WSL 下 `Add-AppxPackage` 会显示成功但 `wsl -l` 为空，必须用 `--import` 手动注册

### 3.3 用户与网络

- [x] `useradd -m -s /bin/bash suntong` + `chpasswd` + `usermod -aG sudo`
- [x] `/etc/wsl.conf` 设 `[user] default=suntong`
- [x] `C:\Users\<user>\.wslconfig` 开启 **mirrored 网络模式**（见 §5）

### 3.4 Python 环境

- [x] 安装 Miniconda（Linux x86_64）
- [x] `conda tos accept`（conda 25+ 必须先接受频道条款，否则 `conda create` 静默失败）
- [x] `conda create -n ea python=3.10`
- [x] `pip install torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1`

## 4. 验证

```bash
# WSL 里执行
python scripts/check_env.py
```

期望输出包含：

```
torch    : 2.7.1+cu126
cuda ok  : True
device   : NVIDIA GeForce RTX 3060 Laptop GPU
[PASS] 环境就绪
```

## 5. 踩坑记录

| # | 问题 | 现象 | 解决 |
|---|---|---|---|
| 1 | `wsl --install` 卡住 | 连 `185.199.109.133:443`（GitHub raw），速率约 100 KB/s | 放弃在线安装，改用微软 CDN 的离线 AppxBundle |
| 2 | Appx 装完没有发行版 | `Add-AppxPackage` 成功，`wsl -l` 为空 | 解包 `install.tar.gz` 用 `wsl --import` |
| 3 | WSL 内大文件下载必挂 | 下到约 500 MB 后速率归零、连接挂死（清华源、阿里云均如此） | 开启 **mirrored 网络模式**，让 WSL 复用 Windows 的 Clash 代理 |
| 4 | torch 默认是 cu13 | 驱动 546.30 只支持到 CUDA 12.3 | 钉死 `torch==2.7.1`（cu126，12.x 向下兼容） |
| 5 | Miniconda 自带 Python 3.14 | PyTorch 无对应 wheel | 单独建 Python 3.10 环境 |
| 6 | `conda create` 静默失败 | 退出码 0，但环境不存在 | 先 `conda tos accept` 接受频道条款 |
| 7 | `apt-get update` 卡死 | 十几分钟无输出、`/tmp/apt.log` 为 0 字节 | mirrored 模式注入的 `http_proxy` 让 apt 挂住；写 `Acquire::http::Proxy "DIRECT";` 后立即正常 |

### 关键修复：mirrored 网络模式

`C:\Users\<user>\.wslconfig`：

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
autoProxy=true
firewall=true
```

生效方式：`wsl --shutdown`，等待 8 秒后重新进入。

效果：WSL 自动继承 Windows 的代理设置（`http_proxy=http://127.0.0.1:7897`），下载速率从 40 KB/s 提升到 40+ MB/s。

### 配套修复：apt 直连

`/etc/apt/apt.conf.d/99noproxy`：

```
Acquire::http::Proxy "DIRECT";
Acquire::https::Proxy "DIRECT";
```

原因：mirrored 模式自动注入的 `http_proxy` 会让 `apt-get` 长时间无响应；国内镜像直连即可。
同时 `/etc/apt/sources.list` 已替换为 `https://mirrors.aliyun.com/ubuntu`。

## 6. 常用命令

```bash
wsl -d Ubuntu-22.04      # 进入 WSL
conda activate ea        # 激活环境
wsl --shutdown           # 改配置后必须执行
wsl -l -v                # 查看发行版与版本
```

## 7. 备注

- **不要**在 `/mnt/c` 下做开发（跨文件系统 IO 极慢），项目放 `~/code`
- Windows 侧建议用 VS Code 的 Remote-WSL 打开 `\\wsl$\Ubuntu-22.04\home\suntong\code\embodied-ai`
