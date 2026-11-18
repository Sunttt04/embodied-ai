import numpy as np


def rotation(theta):
    """返回逆时针旋转 theta 弧度的 2x2 矩阵。"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s],
                     [s,  c]])


def show(deg, p):
    R = rotation(np.deg2rad(deg))
    q = R @ p
    print(f"转 {deg:>3}°: {p} -> {np.round(q, 3)}")


p = np.array([2.0, 0.0])

show(0,   p)
show(90,  p)
show(180, p)
show(270, p)
show(45,  p)
