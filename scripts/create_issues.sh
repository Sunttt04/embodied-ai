#!/usr/bin/env bash
# 批量创建 32 个周任务 issue（需先安装 GitHub CLI 并 gh auth login）
# 用法：在仓库根目录执行  bash scripts/create_issues.sh
set -euo pipefail

command -v gh >/dev/null || { echo "未找到 gh，请先安装 GitHub CLI"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "请先执行 gh auth login"; exit 1; }

for l in "P0|0E8A16|阶段0：地基 W01-W13" "P1|1D76DB|阶段1：真机与模仿学习 W14-W32" "week|BFD4F2|周任务"; do
  IFS='|' read -r n c d <<< "$l"
  gh label create "$n" --color "$c" --description "$d" --force >/dev/null 2>&1 || true
done

n=0
while IFS=$'\t' read -r week phase title deliver; do
  [ -z "${week:-}" ] && continue
  body=$(printf '## 交付物\n%s\n\n## 验收\n- [ ] 交付物可复现（README / 脚本 / 视频任一形式）\n- [ ] 代码已提交，提交信息符合 feat / fix / docs 规范\n- [ ] 在 docs/roadmap.md 中打勾\n\n## 备注\n周计划见 docs/roadmap.md。\n' "$deliver")
  gh issue create --title "[$week] $title" --body "$body" --label "$phase" --label week >/dev/null
  echo "created [$week] $title"
  n=$((n+1))
done < issues.tsv

echo
echo "完成：共创建 $n 个 issue。"
