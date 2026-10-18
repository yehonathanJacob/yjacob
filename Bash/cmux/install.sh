#!/bin/sh
# Reinstall cmux and restore my configuration. Safe to re-run.
set -e
here="$(cd "$(dirname "$0")" && pwd)"
stamp=$(date +%Y%m%d-%H%M%S)

# 1. Install cmux (skip if already installed; it auto-updates via Sparkle).
if [ ! -d /Applications/cmux.app ]; then
  brew tap manaflow-ai/cmux
  brew install --cask cmux
fi

# 2. Copy config files, backing up anything already there.
mkdir -p ~/.config/cmux ~/.config/ghostty
for f in ~/.config/cmux/cmux.json ~/.config/cmux/reveal-in-finder.sh ~/.config/ghostty/config; do
  [ -e "$f" ] && cp "$f" "$f.bak-$stamp"
done
# cmux.json holds an absolute path to the script, so point it at this user's home.
sed "s|/Users/yehonathanjacob|$HOME|g" "$here/cmux.json" > ~/.config/cmux/cmux.json
cp "$here/reveal-in-finder.sh" ~/.config/cmux/reveal-in-finder.sh
chmod +x ~/.config/cmux/reveal-in-finder.sh
cp "$here/ghostty/config" ~/.config/ghostty/config

# 3. The one setting cmux.json can't hold: enable the system-wide hotkey (Option+Space).
defaults write com.cmuxterm.app systemWideHotkey.enabled -bool true

echo "Done. Restart cmux (Cmd+Q, reopen) to pick everything up."
