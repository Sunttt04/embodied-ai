# 批量创建 32 个周任务 issue（需先安装 GitHub CLI 并 gh auth login）
# 用法：在仓库根目录执行
#   pwsh -File scripts/create_issues.ps1

$ErrorActionPreference = 'Stop'

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "未找到 gh。请先安装 GitHub CLI：https://cli.github.com/ 或 winget install GitHub.cli"
}

gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw "尚未登录，请先执行：gh auth login" }

# 1) 建标签（--force 已存在则更新）
$labels = @(
    @{ n = 'P0';   c = '0E8A16'; d = '阶段0：地基 W01-W13' },
    @{ n = 'P1';   c = '1D76DB'; d = '阶段1：真机与模仿学习 W14-W32' },
    @{ n = 'week'; c = 'BFD4F2'; d = '周任务' }
)
foreach ($l in $labels) {
    gh label create $l.n --color $l.c --description $l.d --force *> $null
}

# 2) 读取 issues.tsv 并逐条创建
$tsv = Join-Path $PSScriptRoot '..\issues.tsv'
$rows = Get-Content $tsv -Encoding UTF8 | Where-Object { $_.Trim() -ne '' }

$n = 0
foreach ($row in $rows) {
    $f = $row -split "`t"
    if ($f.Count -lt 4) { continue }
    $week = $f[0].Trim(); $phase = $f[1].Trim(); $title = $f[2].Trim(); $deliver = $f[3].Trim()

    $body = @"
## 交付物
$deliver

## 验收
- [ ] 交付物可复现（README / 脚本 / 视频任一形式）
- [ ] 代码已提交，提交信息符合 feat / fix / docs 规范
- [ ] 在 docs/roadmap.md 中打勾

## 备注
周计划见 docs/roadmap.md。
"@
    gh issue create --title "[$week] $title" --body $body --label $phase --label 'week' | Out-Null
    $n++
    Write-Host "created [$week] $title"
}

Write-Host "`n完成：共创建 $n 个 issue。"
