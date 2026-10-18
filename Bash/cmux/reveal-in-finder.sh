#!/bin/sh
# cmux "preferred editor" for Cmd-clicked paths:
#   Cmd-click       -> reveal in Finder
#   Cmd-Shift-click -> file:   open in a cmux preview split on the right
#                      folder: open a terminal split there and show it in the Files sidebar
# cmux may pass "path:line" or "path:line:col", so strip those suffixes.
p="$1"
[ -e "$p" ] || p="${p%:*}"
[ -e "$p" ] || p="${p%:*}"

# cmux doesn't pass the modifiers, so check whether Shift is still held.
shift=$(osascript -l JavaScript -e 'ObjC.import("AppKit"); ($.NSEvent.modifierFlags & 0x20000) ? 1 : 0')
[ "$shift" = 1 ] || exec open -R "$p"

cmux=/Applications/cmux.app/Contents/Resources/bin/cmux
if [ -d "$p" ]; then
  # The Files sidebar follows the focused pane's folder.
  "$cmux" new-split right --focus true --command "cd '$p' && clear"
  "$cmux" right-sidebar set files --no-focus
  exit 0
fi
split=$("$cmux" --json new-split right)
new=$(echo "$split" | sed -n 's/.*"surface_ref" : "\(.*\)".*/\1/p')
ws=$(echo "$split" | sed -n 's/.*"workspace_ref" : "\(.*\)".*/\1/p')
"$cmux" open "$p" --surface "$new" && "$cmux" close-surface --force --surface "$new" --workspace "$ws"
exit 0
