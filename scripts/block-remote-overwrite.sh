#!/bin/sh
# 本地 docs 为真源：默认禁止 pull / merge / rebase，避免被远程覆盖。
# 紧急确需用远程覆盖本地时：
#   ALLOW_PULL=1 git pull
# 或：git fetch origin && git reset --hard origin/main

if [ "$ALLOW_PULL" = "1" ]; then
  exit 0
fi

cat <<'EOF'
[blocked] 本地 c:\work\projects\wchat\docs 为真源，已禁止会覆盖本地的拉取/合并/变基。

日常请只：
  git add -A
  git commit -m "..."
  git push origin main

若确认要用远程覆盖本地，再执行：
  ALLOW_PULL=1 git pull
  # 或 PowerShell:  $env:ALLOW_PULL=1; git pull
EOF
exit 1
