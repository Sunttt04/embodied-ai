import numpy as np


def link(L, theta):
    """一段连杆的齐次变换：先转 theta，再沿 x 前进 L。"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, L * c],
        [s,  c, L * s],
        [0,  0,   1  ],
    ])


def forward_kinematics(lengths, angles):
    """连乘所有连杆矩阵，返回末端位置和中间关节位置。"""
    T = np.eye(3)
    joints = [T[:2, 2].copy()]        # 基座位置

    for L, a in zip(lengths, angles):
        T = T @ link(L, a)
        joints.append(T[:2, 2].copy())

    return T, joints


lengths = [1.0, 1.0]
angles = [np.deg2rad(0), np.deg2rad(90)]

T, joints = forward_kinematics(lengths, angles)

print("总变换矩阵:")
print(np.round(T, 3))
print()
print("末端位置:", np.round(T[:2, 2], 3))
print("各关节位置:")
for i, j in enumerate(joints):
    print(f"  关节{i}: {np.round(j, 3)}")
