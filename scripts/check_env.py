"""环境自检：确认 Python / PyTorch / CUDA 是否就绪。

用法（WSL 内）：
    python scripts/check_env.py
"""

import platform
import sys


def main() -> int:
    print("=" * 48)
    print("python   :", sys.version.split()[0])
    print("platform :", platform.platform())
    print("=" * 48)

    try:
        import torch
    except Exception as exc:  # noqa: BLE001
        print("[FAIL] 无法导入 torch:", exc)
        return 1

    print("torch    :", torch.__version__)
    print("cuda ver :", torch.version.cuda)
    print("cuda ok  :", torch.cuda.is_available())

    if not torch.cuda.is_available():
        print("[FAIL] CUDA 不可用：检查驱动版本与 torch 的 CUDA 版本是否匹配")
        return 1

    print("device   :", torch.cuda.get_device_name(0))
    props = torch.cuda.get_device_properties(0)
    print("vram     : %.1f GB" % (props.total_memory / 1024**3))

    # 真跑一次矩阵乘法，确认不只是"能识别"而是"能计算"
    x = torch.randn(2048, 2048, device="cuda")
    y = x @ x
    torch.cuda.synchronize()
    print("matmul   :", tuple(y.shape), y.dtype, "ok")
    print("[PASS] 环境就绪")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
