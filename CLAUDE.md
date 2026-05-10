# Project Instructions

## Browser Testing — Mandatory

All testing and verification tasks **must** use the Chrome browser extension (`mcp__claude-in-chrome__*` tools).

### Rules
- Before any test or UI verification step, load the required Chrome tool via `ToolSearch` (e.g., `select:mcp__claude-in-chrome__tabs_context_mcp`) and then call it.
- This applies to sub-agents as well — every agent doing UI or end-to-end verification must use the Chrome tools.
- Do **not** skip Chrome verification and claim success based only on code review or type checking.

### If Chrome Extension Is Unavailable
If any `mcp__claude-in-chrome__*` call fails or the extension appears disconnected:
1. **Stop immediately** — do not proceed with the test.
2. Tell the user: "The Chrome extension is not reachable. Please reconnect it and let me know when it's ready."
3. Wait for user confirmation before retrying.

Do not substitute screenshot tools, headless approaches, or manual instructions as a replacement — always use the Chrome extension.
