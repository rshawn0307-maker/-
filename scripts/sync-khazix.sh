#!/usr/bin/env bash
#
# 一键同步源自 khazix-skills 的 skill 到本仓库。
#
# 用法：
#   bash scripts/sync-khazix.sh            仅更新工作区文件并打印变更摘要
#   bash scripts/sync-khazix.sh --push     更新并自动 commit + push
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_REPO="https://github.com/KKKKhazix/khazix-skills.git"
SKILLS=(neat-freak storage-analyzer leader human-writing)
ORIGIN_URL="https://github.com/KKKKhazix/khazix-skills"
ATTRIBUTION='> **来源声明**：本 skill 收录自 [khazix-skills](https://github.com/KKKKhazix/khazix-skills)（作者：KKKKhazix），保留原作者内容，感谢原作者。上游更新可用仓库根目录 `scripts/sync-khazix.sh` 一键同步。'

ORIGIN_MD="# 出处 / Origin

本 skill 收录自 [khazix-skills]($ORIGIN_URL)（作者：KKKKhazix），保留原作者内容，感谢原作者。

上游更新后，在 rshawn-skills 仓库根目录运行一条命令即可同步：

\`\`\`bash
bash scripts/sync-khazix.sh
\`\`\`
"

ensure_attribution() {
  local f="$1"
  [ -f "$f" ] || return 0
  grep -q "来源声明" "$f" && return 0
  local line
  line="$(grep -n '^# ' "$f" | head -1 | cut -d: -f1)"
  [ -n "$line" ] || return 0
  awk -v n="$line" -v note="$ATTRIBUTION" 'NR==n { print; print ""; print note; next } { print }' "$f" > "$f.tmp"
  mv "$f.tmp" "$f"
}

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "==> 拉取上游 khazix-skills..."
if ! git clone --depth 1 "$UPSTREAM_REPO" "$TMP_DIR/khazix" >/dev/null 2>&1; then
  echo "❌ 拉取上游失败，请检查网络后重试"
  exit 1
fi

for s in "${SKILLS[@]}"; do
  src="$TMP_DIR/khazix/$s"
  dst="$REPO_ROOT/skills/$s"
  if [ ! -d "$src" ]; then
    echo "⚠️  上游没有 $s/（可能已改名或删除），跳过"
    continue
  fi
  mkdir -p "$dst"
  cp -R "$src/." "$dst/"
  printf '%s' "$ORIGIN_MD" > "$dst/ORIGIN.md"
  ensure_attribution "$dst/SKILL.md"
  echo "✅ 已同步 $s"
done

echo
echo "==> 变更摘要："
git -C "$REPO_ROOT" status --short -- skills/neat-freak skills/storage-analyzer skills/leader skills/human-writing

if [ "${1:-}" = "--push" ]; then
  git -C "$REPO_ROOT" add skills/neat-freak skills/storage-analyzer skills/leader skills/human-writing
  if git -C "$REPO_ROOT" diff --cached --quiet; then
    echo "（无变更可提交）"
  else
    git -C "$REPO_ROOT" commit -m "sync: 同步 khazix-skills 上游更新"
    git -C "$REPO_ROOT" push
  fi
fi
