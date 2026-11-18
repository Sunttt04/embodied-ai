import numpy as np


def transform(tx, ty, theta):
    """先旋转 theta，再平移 (tx, ty)，返回 3x3 齐次矩阵。"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, tx],
        [s,  c, ty],
        [0,  0,  1],
    ])


def apply(T, x, y):
    p = np.array([x, y, 1.0])
    q = T @ p
    return q[:2]


T = transform(tx=1, ty=2, theta=np.deg2rad(90))

print("齐次矩阵:")
print(np.round(T, 3))
print()
print("点 (1,0) 变换后:", np.round(apply(T, 1, 0), 3))
print("点 (0,0) 变换后:", np.round(apply(T, 0, 0), 3))
