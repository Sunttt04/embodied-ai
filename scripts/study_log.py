#!/usr/bin/env python3
"""学习打卡与经验值系统。

用法：
    python study_log.py add "搞定 stats.py 的异常处理" -t demo
    python study_log.py stats
    python study_log.py list
    python study_log.py report      # 生成 HTML 报告
"""

import argparse
import json
from datetime import date, datetime, timedelta
from pathlib import Path

DATA_FILE = Path.home() / "study_data.json"

# 行为 -> (名称, 经验值)
ACTIONS = {
    "task":    ("完成一个任务", 20),
    "algo":    ("独立实现算法", 50),
    "demo":    ("完成小 Demo", 100),
    "project": ("完成完整项目", 200),
    "paper":   ("复现一篇论文", 100),
    "share":   ("技术分享", 50),
    "note":    ("单纯记录", 5),
}

LEVEL_STEP = 300
TITLES = [
    "学徒", "见习工程师", "初级工程师", "中级工程师",
    "高级工程师", "资深工程师", "专家",
]


# ---------- 数据读写 ----------

def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"records": []}


def save(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------- 计算 ----------

def total_xp(data):
    return sum(r["xp"] for r in data["records"])


def day_list(data):
    return sorted({r["date"] for r in data["records"]})


def streak(data):
    days = day_list(data)
    if not days:
        return 0
    day_set = set(days)
    cur = date.fromisoformat(days[-1])
    n = 1
    while (cur - timedelta(days=1)).isoformat() in day_set:
        cur -= timedelta(days=1)
        n += 1
    return n


def level_of(xp):
    lv = xp // LEVEL_STEP + 1
    return lv, TITLES[min(lv - 1, len(TITLES) - 1)]


def progress_bar(cur, total, width=22):
    filled = int(width * cur / total)
    return "█" * filled + "░" * (width - filled)


def xp_by_date(data, n_days=14):
    today = date.today()
    out = {}
    for i in range(n_days - 1, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        out[d] = 0
    for r in data["records"]:
        if r["date"] in out:
            out[r["date"]] += r["xp"]
    return out


# ---------- 命令 ----------

def cmd_add(args):
    data = load()
    name, base_xp = ACTIONS[args.type]
    xp = base_xp if args.xp is None else args.xp

    record = {
        "date": args.date or date.today().isoformat(),
        "note": args.note,
        "type": args.type,
        "xp": xp,
    }
    data["records"].append(record)
    save(data)

    before = total_xp(data) - xp
    after = total_xp(data)
    lv_before, _ = level_of(before)
    lv_after, title = level_of(after)

    print(f"✅ +{xp} XP   累计 {after} XP   Lv.{lv_after} {title}")
    if lv_after > lv_before:
        print(f"🎉 升级！Lv.{lv_before} -> Lv.{lv_after} {title}")
    st = streak(data)
    if st > 1:
        print(f"🔥 连续学习 {st} 天")
    print(f"   距离下一级还差 {LEVEL_STEP - after % LEVEL_STEP} XP")


def cmd_stats(args):
    data = load()
    xp = total_xp(data)
    lv, title = level_of(xp)
    st = streak(data)
    days = day_list(data)
    in_level = xp % LEVEL_STEP

    print("=" * 46)
    print(f"  等级   Lv.{lv}  {title}")
    print(f"  经验   {xp} XP   （本级 {in_level}/{LEVEL_STEP}）")
    print(f"  {progress_bar(in_level, LEVEL_STEP)}")
    print(f"  打卡   {len(days)} 天   记录 {len(data['records'])} 条")
    print(f"  连续   {st} 天")
    print("=" * 46)

    if days:
        print(f"  首次打卡 {days[0]}")
        print(f"  最近打卡 {days[-1]}")


def cmd_list(args):
    data = load()
    if not data["records"]:
        print("还没有记录。用 add 命令记一条吧。")
        return
    for r in data["records"][-args.n:]:
        name = ACTIONS.get(r["type"], ("记录", 0))[0]
        print(f"{r['date']}  +{r['xp']:>4} XP  [{name}]  {r['note']}")


def cmd_undo(args):
    data = load()
    if not data["records"]:
        print("没有可撤销的记录。")
        return
    r = data["records"].pop()
    save(data)
    print(f"已删除最后一条：{r['date']}  {r['note']}  (-{r['xp']} XP)")


def cmd_report(args):
    data = load()
    xp = total_xp(data)
    lv, title = level_of(xp)
    st = streak(data)
    days = day_list(data)
    by_date = xp_by_date(data, 14)
    max_xp = max(by_date.values()) or 1

    bars = []
    for d, v in by_date.items():
        h = int(120 * v / max_xp)
        label = d[5:]
        bars.append(
            f'<div class="col"><div class="bar" style="height:{max(h,2)}px" '
            f'title="{d}: {v} XP"></div><div class="lbl">{label}</div></div>'
        )

    recent = "".join(
        f"<tr><td>{r['date']}</td><td class='xp'>+{r['xp']}</td>"
        f"<td>{ACTIONS.get(r['type'], ('-', 0))[0]}</td><td>{r['note']}</td></tr>"
        for r in data["records"][-15:][::-1]
    )

    html = f"""<!doctype html>
<html lang="zh"><meta charset="utf-8">
<title>学习进度</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ background:#0f1115; color:#e6e6e6; font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
         max-width:820px; margin:40px auto; padding:0 20px; }}
  h1 {{ font-size:20px; font-weight:600; }}
  .card {{ background:#171a21; border:1px solid #262b36; border-radius:14px;
           padding:20px 22px; margin-bottom:18px; }}
  .lv {{ font-size:34px; font-weight:700; }}
  .sub {{ color:#8b93a7; font-size:13px; margin-top:6px; }}
  .bar2 {{ height:10px; background:#262b36; border-radius:6px; overflow:hidden; margin-top:14px; }}
  .bar2 > div {{ height:100%; background:linear-gradient(90deg,#3b82f6,#22d3ee); }}
  .chart {{ display:flex; align-items:flex-end; gap:6px; height:140px; margin-top:8px; }}
  .col {{ flex:1; display:flex; flex-direction:column; justify-content:flex-end; align-items:center; }}
  .bar {{ width:100%; background:#3b82f6; border-radius:3px 3px 0 0; }}
  .lbl {{ font-size:9px; color:#6b7280; margin-top:4px; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th,td {{ text-align:left; padding:6px 8px; border-bottom:1px solid #232833; }}
  th {{ color:#8b93a7; font-weight:500; }}
  .xp {{ color:#22d3ee; font-variant-numeric:tabular-nums; }}
</style>
<h1>具身智能 · 学习进度</h1>
<div class="card">
  <div class="lv">Lv.{lv} <span style="font-size:18px;color:#8b93a7">{title}</span></div>
  <div class="sub">{xp} XP · 已打卡 {len(days)} 天 · 连续 {st} 天</div>
  <div class="bar2"><div style="width:{in_level_pct(xp)}%"></div></div>
  <div class="sub">距离下一级还差 {LEVEL_STEP - xp % LEVEL_STEP} XP</div>
</div>
<div class="card">
  <div class="sub">最近 14 天</div>
  <div class="chart">{''.join(bars)}</div>
</div>
<div class="card">
  <table><tr><th>日期</th><th>XP</th><th>类型</th><th>内容</th></tr>{recent}</table>
</div>
</html>"""

    out = Path(args.out)
    out.write_text(html, encoding="utf-8")
    print(f"已生成 {out.resolve()}")


def in_level_pct(xp):
    return round((xp % LEVEL_STEP) / LEVEL_STEP * 100, 1)


# ---------- 入口 ----------

def main():
    p = argparse.ArgumentParser(description="学习打卡与经验值")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="添加一条记录")
    a.add_argument("note", help="做了什么")
    a.add_argument("-t", "--type", default="task", choices=sorted(ACTIONS),
                   help="记录类型，决定基础经验值")
    a.add_argument("-x", "--xp", type=int, default=None, help="手动指定经验值")
    a.add_argument("-d", "--date", default=None, help="日期 YYYY-MM-DD，默认今天")
    a.set_defaults(func=cmd_add)

    s = sub.add_parser("stats", help="查看总进度")
    s.set_defaults(func=cmd_stats)

    l = sub.add_parser("list", help="查看最近记录")
    l.add_argument("-n", type=int, default=10)
    l.set_defaults(func=cmd_list)

    u = sub.add_parser("undo", help="撤销最后一条")
    u.set_defaults(func=cmd_undo)

    r = sub.add_parser("report", help="生成 HTML 报告")
    r.add_argument("-o", "--out", default=str(Path.home() / "study_report.html"))
    r.set_defaults(func=cmd_report)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
