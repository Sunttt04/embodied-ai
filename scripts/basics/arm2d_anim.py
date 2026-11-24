"""二连杆机械臂动画：看关节角怎么决定末端位置。

运行：
    python arm2d_anim.py
生成：
    arm_anim.gif
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

L1, L2 = 1.0, 1.0
N_FRAMES = 120
FPS = 20


def forward_kinematics(theta1, theta2):
    """返回三个点：基座、关节2、末端。"""
    base = np.array([0.0, 0.0])
    joint2 = base + L1 * np.array([np.cos(theta1), np.sin(theta1)])
    end = joint2 + L2 * np.array(
        [np.cos(theta1 + theta2), np.sin(theta1 + theta2)]
    )
    return np.array([base, joint2, end])


t = np.linspace(0, 2 * np.pi, N_FRAMES)
angles = [(1.2 * np.sin(x), 1.2 * np.sin(2 * x)) for x in t]

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2.4, 2.4)
ax.set_ylim(-2.4, 2.4)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.axhline(0, color="gray", lw=0.6)
ax.axvline(0, color="gray", lw=0.6)
ax.set_title("2-link arm  (L1 = L2 = 1)")

arm_line, = ax.plot([], [], "o-", lw=4, ms=9, color="#1f77b4", zorder=3)
trace_line, = ax.plot([], [], "-", lw=1.2, alpha=0.7, color="#d62728", zorder=2)
info = ax.text(
    0.02, 0.97, "", transform=ax.transAxes, va="top",
    fontsize=10, family="monospace",
)

trace = []


def update(i):
    t1, t2 = angles[i]
    pts = forward_kinematics(t1, t2)

    arm_line.set_data(pts[:, 0], pts[:, 1])

    trace.append(pts[2].copy())
    if len(trace) > 400:
        trace.pop(0)
    tr = np.array(trace)
    trace_line.set_data(tr[:, 0], tr[:, 1])

    info.set_text(
        f"theta1 = {np.degrees(t1):6.1f} deg\n"
        f"theta2 = {np.degrees(t2):6.1f} deg\n"
        f"end    = ({pts[2, 0]:5.2f}, {pts[2, 1]:5.2f})"
    )
    return arm_line, trace_line, info


anim = FuncAnimation(fig, update, frames=N_FRAMES, interval=1000 / FPS, blit=False)
anim.save("arm_anim.gif", writer=PillowWriter(fps=FPS))
print("已生成 arm_anim.gif")
