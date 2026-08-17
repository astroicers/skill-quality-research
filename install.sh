#!/usr/bin/env bash
#
# skill-reviewer 安裝腳本（macOS / Linux）
# 用法：./install.sh [--force] [--symlink]（也可 sh install.sh，全腳本為 POSIX 相容）
#   --force    目標已存在時直接覆蓋，不詢問
#   --symlink  以符號連結安裝（repo 更新自動生效；預設為複製）

# 不用 pipefail：本腳本無管線，且 pipefail 非 POSIX（dash 的 sh 會直接報錯）
set -eu

FORCE=0
SYMLINK=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --symlink) SYMLINK=1 ;;
    *) echo "未知參數：$arg（可用：--force / --symlink）" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$SCRIPT_DIR/skill-reviewer"
SKILLS_DIR="$HOME/.claude/skills"
DEST_DIR="$SKILLS_DIR/skill-reviewer"

if [ ! -f "$SRC_DIR/SKILL.md" ]; then
  echo "錯誤：找不到 $SRC_DIR/SKILL.md，請在 repo 根目錄執行本腳本。" >&2
  exit 1
fi

if [ ! -d "$HOME/.claude" ]; then
  echo "錯誤：找不到 ~/.claude/，請先安裝並執行過 Claude Code。" >&2
  exit 1
fi

# lint 只需 python3 stdlib，零第三方依賴——先確認它在
if ! command -v python3 >/dev/null 2>&1; then
  echo "錯誤：找不到 python3（lint_skill.py 需要，僅用 stdlib）。" >&2
  exit 1
fi

mkdir -p "$SKILLS_DIR"

# -e 抓不到 dangling symlink，要多檢查 -L（否則殘留的壞連結會讓後面 mkdir 失敗）
if [ -e "$DEST_DIR" ] || [ -L "$DEST_DIR" ]; then
  if [ "$FORCE" -eq 1 ]; then
    echo "偵測到既有安裝（$DEST_DIR），--force 已指定，直接覆蓋。"
  else
    if [ ! -t 0 ]; then
      echo "錯誤：$DEST_DIR 已存在，且目前為非互動環境無法詢問，請改用 --force 覆蓋。" >&2
      exit 1
    fi
    printf '%s 已存在，要覆蓋嗎？ [y/N] ' "$DEST_DIR"
    read -r answer
    case "$answer" in
      y | Y | yes | YES) ;;
      *)
        echo "已取消安裝。"
        exit 0
        ;;
    esac
  fi
  # 路徑刻意不加結尾斜線：若 DEST 是 symlink，只移除連結本身、不動連結目標
  rm -rf "$DEST_DIR"
fi

if [ "$SYMLINK" -eq 1 ]; then
  ln -s "$SRC_DIR" "$DEST_DIR"
  echo ""
  echo "✅ 已以 symlink 安裝：$DEST_DIR → $SRC_DIR"
  echo "   （repo 更新後自動生效；移動或刪除 repo 會斷鏈）"
else
  mkdir -p "$DEST_DIR"
  cp -R "$SRC_DIR/." "$DEST_DIR/"
  echo ""
  echo "✅ 已安裝到 $DEST_DIR"
fi

# 安裝後自我驗證：跑 selftest 確認真的能用（而非只是檔案複製成功）
if python3 "$DEST_DIR/scripts/lint_skill.py" --selftest >/dev/null 2>&1; then
  echo "✅ selftest 通過"
else
  echo "⚠️  selftest 未通過——安裝檔案已就位，但 lint 可能無法正常運作。" >&2
  echo "   請執行以下指令看詳細錯誤：" >&2
  echo "   python3 $DEST_DIR/scripts/lint_skill.py --selftest" >&2
  exit 1
fi

echo ""
echo "試跑（審查任一個 skill repo）："
echo "  python3 ~/.claude/skills/skill-reviewer/scripts/lint_skill.py <repo 目錄>"
echo ""
echo "完整審查（含 LLM craft 判讀）：在 Claude Code 對話中說"
echo "  「用 skill-reviewer 審查 <repo>」"
