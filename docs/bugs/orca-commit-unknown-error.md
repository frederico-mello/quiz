# Orca bug: AI commit message reports `UnknownError` while opencode succeeds

**Status:** Repro 100% on this machine. Working theory + evidence below.
**Reporter:** Frederico (user)
**Date:** 2026-08-21
**Orca version:** 1.4.186 (`C:\Users\Frederico\AppData\Local\Programs\orca\Orca.exe`)
**opencode version:** 1.18.20 (`%AppData%\npm\node_modules\opencode-ai`)
**Platform:** Windows 11, win32, PowerShell 5.1

---

## Summary

The Orca "Generate commit message" feature surfaces an `UnknownError` to the user every time, even though the underlying `opencode` process:

1. starts cleanly,
2. loads the right config,
3. uses the correct model,
4. successfully runs `git diff --cached --stat`,
5. produces a valid conventional commit message,
6. finishes with `finish: "stop"`.

The Orca UI replaces the actual success with a generic `UnknownError` JSON (`{ "name": "UnknownError", "data": { "message": "...", "ref": "..." } }`), making the issue look like an opencode/provider failure when it is an Orca-side parse/render bug.

---

## Repro steps

1. Stage some changes in a git repo.
2. Open the repo in Orca as a worktree.
3. In the Source Control panel, click "Generate commit message" (the AI commit message affordance).
4. Orca shows: `OpenCode CLI command failed with code 1: Error: { "name": "UnknownError", … }`.
5. Meanwhile, the opencode session actually completes successfully (see evidence below).

---

## Environment

`~/.config/opencode/opencode.json` (default model):

```json
{
  "model": "ollama-cloud/minimax-m3",
  "provider": { "ollama-cloud": { "apiKey": "{env:OLLAMA_API_KEY}", "baseURL": "https://ollama.com/v1", ... } },
  ...
}
```

Default model is `ollama-cloud/minimax-m3` (MiniMax M3 via Ollama Cloud). API key resolves correctly, model is reachable, the same model responds `OK` to a direct `opencode run` invocation outside Orca.

---

## Evidence the opencode side is healthy

### 1. Direct CLI works

```
$ opencode run "Reply with just the word OK."
> build ?? minimax-m3
OK
```

### 2. Successful AI commit message run exists in the opencode session DB

`opencode session list` shows a session titled `Git diff and conventional commit message` (id `ses_fdaff3a49ffebNkxlZJSJTsjQi`) created at 12:46. `opencode export ses_fdaff3a49ffebNkxlZJSJTsjQi` shows:

- `info.model`: `{ providerID: "ollama-cloud", modelID: "minimax-m3", variant: "default" }`
- `info.tokens`: `input: 24927, output: 181` (LLM was actually called and answered)
- `info.summary`: `additions: 0, deletions: 0, files: 0` (no files were modified, but the message was produced)
- user message: `"Run git diff --cached --stat. Then output only a conventional commit message."`
- assistant turn 1: `tool: bash`, command `rtk git diff --cached --stat`, `status: completed`, `exit: 0`
- assistant turn 2: `finish: "stop"`, with a `type: "text"` part containing the commit message:

  ```
  chore: sync OpenSpec skills and add emdash notifications plugin
  ```

This is the exact behavior the Orca AI commit message feature is supposed to drive. The opencode session finishes successfully and the message is present in the assistant text part.

### 3. Orca-spawned opencode runs complete silently

Looking at `~/.local/share/opencode/log/opencode.log`, fresh Orca triggers (e.g. `run=d6f86a43`, `run=7bf67d87` at 15:51:27 / 15:51:34) log:

- `creating instance`
- `bootstrapping`
- `loading path=".../config.json"` (all four layers)
- `all LSPs are disabled`
- `all formatters are disabled`
- `init`
- `created id=ses_…`
- `event connected`

…and then the run ends. **No `stream … providerID=…` line, no `step-start`, no error, no `step-finish`**. The opencode subprocess exits cleanly with no LLM call recorded and no error message. From the opencode point of view, the request never arrives. The Orca side, however, surfaces a `code: 1` `UnknownError` to the user.

This pattern is consistent with the Orca renderer killing the opencode child (or the ACP/stdio stream being closed) before the prompt is fully transmitted, while Orca's promise wrapper interprets the non-graceful exit as `code 1` and rethrows it as `UnknownError`.

---

## Working theory

- Orca spawns `opencode` (likely as the ACP server, not as the `run` CLI) and sends the commit message prompt over the ACP/stdio channel.
- The renderer or the prompt-routing layer in Orca loses, truncates, or mis-encodes the prompt, so opencode never receives it (hence no `stream` line in the log).
- The Orca side closes the child or the channel, opencode exits with no work done and a generic non-zero code, Orca's error wrapper formats the opencode exit as `{ "name": "UnknownError" }` and displays it to the user.
- Because the same model and config are working perfectly when invoked through the opencode CLI directly, the failure is isolated to Orca's opencode integration, not to the model or provider.

The earlier theory (provider `Insufficient Balance`, log growth, etc.) was a red herring: those were symptoms of a different opencode invocation in the same shell. Once the model was switched to `ollama-cloud/minimax-m3` and the log was truncated, the opencode side recovered fully — but the Orca commit message feature still fails with `UnknownError`.

---

## Diagnostic commands the Orca team can use

```
# Confirm opencode itself works:
opencode run --model ollama-cloud/minimax-m3 "Reply with just the word OK."

# Inspect what the latest Orca-spawned opencode run actually saw:
cat ~/.local/share/opencode/log/opencode.log | tail -200

# Inspect the Orca daemon log for the corresponding session lifecycle:
cat "$APPDATA/orca/logs/daemon.log" | tail -200
cat "$APPDATA/orca/logs/main.trace.ndjson" | tail -200

# Inspect the AI commit message session that Orca spawned (if it was actually created):
opencode session list
opencode export <session-id>
```

In our case, the Orca-spawned run never reaches the `stream` line, even though direct CLI invocations of the same model reach it within ~2 s.

---

## What we have ruled out

- ❌ Model/provider balance: `ollama-cloud/minimax-m3` works for direct `opencode run` calls.
- ❌ Wrong default model: `~/.config/opencode/opencode.json` line 3 is `"model": "ollama-cloud/minimax-m3"` and the running opencode process picks it up.
- ❌ Stale opencode process / cache: the log was truncated and the run still failed on the next attempt.
- ❌ Stale `model.json` recent list / variant pinnings: those don't override the config default for new runs.
- ❌ Network/auth: API key resolves (`{env:OLLAMA_API_KEY}`), model answers direct CLI prompts.
- ❌ Git hook or pre-commit script breaking the message: the opencode tool call returns `exit: 0` and a real diff in the successful session.

---

## Suggested fixes / asks for the Orca team

1. Don't blanket-map any non-zero opencode child exit to `UnknownError`. Surface the actual opencode stderr (or the ACP error code) to the user when the prompt was never streamed, so users can tell "opencode never got my prompt" apart from "the LLM rejected the request".
2. Add a log line on the Orca side when the AI commit message feature spawns opencode, including the full argv, working directory, and stdin bytes. Without this, users cannot distinguish "opencode is the problem" from "the Orca → opencode bridge is the problem".
3. Reproduce locally by pointing Orca at a default model that the user can also run successfully via `opencode run`, then click "Generate commit message" in a worktree with staged changes.
4. Check whether the renderer is closing the opencode child too early (e.g. timeout, navigation, prompt unmount) before the prompt is fully transmitted. The `event connected` log line in opencode without any subsequent `stream` is the smoking gun.

---

## Attachments available on request

- `~/.local/share/opencode/log/opencode.log` (last 200 lines, including the Orca-spawned runs `d6f86a43` and `7bf67d87`)
- `opencode export ses_fdaff3a49ffebNkxlZJSJTsjQi` (full transcript of a successful AI commit message run that Orca should have surfaced to the user)
- `~/.config/opencode/opencode.json` (sanitized)
- `$APPDATA/orca/logs/main.trace.ndjson` and `daemon.log` (last 200 lines, no `UnknownError` literal found — the error lives in the renderer process, not in the persisted trace)
