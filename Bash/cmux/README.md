# cmux setup

My [cmux](https://github.com/manaflow-ai/cmux) terminal configuration and how to reinstall it.

## Reinstall

```sh
./install.sh
```

Then quit cmux (Cmd+Q) and reopen it. The script:

1. Installs cmux with Homebrew if `/Applications/cmux.app` is missing
   (`brew tap manaflow-ai/cmux && brew install --cask cmux`).
   Alternative: download the [DMG](https://github.com/manaflow-ai/cmux/releases/latest/download/cmux-macos.dmg) and drag it to Applications.
2. Copies the files below into place, backing up existing ones as `*.bak-<timestamp>`.
3. Turns on the system-wide hotkey (the only setting `cmux.json` can't hold).

Needs cmux 0.65.0 or newer (for the Cmd+right-click link menu).

## Files

| File | Goes to | What it does |
|---|---|---|
| `cmux.json` | `~/.config/cmux/cmux.json` | Main cmux settings |
| `reveal-in-finder.sh` | `~/.config/cmux/reveal-in-finder.sh` | Handles Cmd-clicked file paths (set as cmux's "preferred editor") |
| `ghostty/config` | `~/.config/ghostty/config` | Terminal background transparency (cmux reads the Ghostty config) |

## What the settings do

- **Option+Space** shows/hides all cmux windows (system-wide hotkey).
- Dark appearance, no quit confirmation, no "warn before quit" prompt.
- Link clicks open outside cmux by default:

```
Cmd-click           web link       -> default browser
Cmd + right-click   web link       -> menu: Open Link in cmux Browser / Default Browser / Copy Link
Cmd-click           file or folder -> Finder, item selected
Cmd-Shift-click     file           -> cmux preview split on the right
Cmd-Shift-click     folder         -> terminal split in that folder + right sidebar > Files
```

The relevant `cmux.json` keys:
`browser.openTerminalLinksInCmuxBrowser: false`, `app.openSupportedFilesInCmux: false`,
`app.openMarkdownInCmuxViewer: false`, `app.preferredEditor: <path to reveal-in-finder.sh>`.

## Notes

- cmux doesn't tell the script which modifier keys were held, so `reveal-in-finder.sh` checks
  whether Shift is still down ~0.1s after the click. Release Shift too fast and you get Finder.
- Because the script is cmux's "preferred editor", other cmux "open in editor" actions
  (e.g. opening the settings file) also reveal in Finder.
- The Files sidebar always shows the focused pane's folder; that's why a folder opens a new
  terminal split there instead of just switching the sidebar.
- To refresh this backup after changing settings, copy `~/.config/cmux/*` and
  `~/.config/ghostty/config` back here (keep the extra `appearance`/`confirmQuit`/`warnBeforeQuit`
  keys in `cmux.json`; they're set in the Settings UI and don't appear in the live file).
