# Independent design: one operator command

**v0.2 scope:** these commands prepare or display explicitly selected independent-design attempts. They do not resume the main pilot, reset its budget or authorize later gates. Pilot continuations use the checkpoint and cumulative accounting in [the shared contract](../agents/contract.md). New exports use the current run-record template; existing packs keep their original bytes and SHA. Unused pilot-related metadata stays null/empty during methodology preparation.

## Why this exists

On 2026-09-08, the operator reported a reviewer stopping because unrelated project instructions and memory were already visible. The reviewer reported saving a blocking report and closing its run record without starting the design or rechecking input hashes. We have the operator's message, not an independently inspected copy of that session or its files. The exact origin of the extra context remains unknown.

This was not a failure of the design task. The startup instruction explicitly requires a stop on known exposure to excluded content. The earlier advice to open a new conversation was insufficient: a new conversation can still be given the same user/project configuration. We should correct the launch environment, not tell the reviewer to ignore the stop condition.

The operator also requested that the sequence `git pull`, generating `RUN_ID`, choosing a fresh output directory and calling the preparation helper become a documented command. Both requests are implemented by `scripts/independent-review.py`.

## Command on Ubuntu

Run as the operator in a normal server terminal, not inside a reviewer session. Requirements: Python 3.10+, Git and an already installed Codex CLI for `--launch`. The existing input pack is reused; no export, dependency installation or model selection is silently performed.

Fetch the new command once from an older checkout:

```bash
git pull --ff-only
```

Then, from `~/RustyBun`, use this single command for a new attempt:

```bash
python3 scripts/independent-review.py --update --launch --allow-unverified-isolation
```

No manually composed `RUN_ID`, `--out` or follow-up `--show-handoff` is needed. Defaults are the existing `RustyBun-review-01` beside the RustyBun checkout and a new output directory beside it. Every invocation creates a new attempt; it never resumes a blocked run. A timestamp with microseconds and a random suffix makes accidental name collisions unlikely; any existing destination still causes a refusal, not an overwrite.

The command:

1. With `--update`, refuses a dirty checkout, runs `git pull --ff-only`, then re-executes the updated launcher. It never resets, stashes, rebases or force-pulls. A failed update stops the command. This updates tooling, **not the existing review pack or its process SHA**.
2. Verifies the existing pack using `prepare-review-run.py`, creates a new `RUN-RECORD.json` and `START-REVIEW.txt`, and prints the complete reviewer handoff.
3. With `--launch`, creates a private temporary Codex profile, asks for device-code login to the existing ChatGPT account, and opens a new, initially empty Codex CLI session in the output directory. It does not use `resume`, `fork`, an API key or automatic API fallback.
4. Prints the same handoff again after login. **Select the model and reasoning setting in the new client, then paste only the text between `BEGIN REVIEWER PROMPT` and `END REVIEWER PROMPT`.** `--no-alt-screen` keeps terminal scrollback available. A saved copy remains in `START-REVIEW.txt`; do not give the reviewer this documentation, the journal or the main checkout.

Device login requires opening the URL and entering the code shown by Codex; it may need enabling in account/workspace settings [4]. A fresh profile does not mean another account or a quota reset. Model interaction uses the existing account's allowance. Cancel on an unexpected billing/purchase prompt; the launcher neither verifies the remaining quota nor buys credits.

## Preparation without starting Codex

The default does not use Git/network, log in or invoke a client:

```bash
python3 scripts/independent-review.py --allow-unverified-isolation
```

Without the isolation flag, preparation is still possible but execution stays blocked. `--launch` requires the flag explicitly. This is the existing **exploratory, independent-design-only** authorization, not permission for a certified blind run or a later stage.

`--pack PATH` selects another existing independent-design pack. `--output-parent PATH` changes the parent of newly created output directories. `--run-id ID` optionally supplies an identifier, but is not needed normally. Input/output must remain outside the main checkout and separate from each other. Missing packs must be exported explicitly using the existing exporter; the wrapper does not guess or rebuild an experiment's inputs.

`--model EXACT_CLIENT_ID` and `--reasoning CLIENT_SUPPORTED_VALUE` are optional. Otherwise choose them in the opened client before pasting the task. We do not translate display labels into guessed API model IDs or invent a universal `max`/`Ultra` value. Unsupported settings cause a client error, not an automatic fallback. Actual model/settings must still be recorded from the running session.

## What the separate profile changes

Codex documents its local state under `CODEX_HOME`, global instruction discovery there, and additional project instruction discovery [1, 2]. `project_root_markers = []` makes the working directory the project root for discovery [2]. User skills can also be found under `$HOME/.agents/skills`; admin/system skills have other locations [5].

We therefore create a **new `HOME`, `CODEX_HOME` and XDG directory set per launched attempt**, outside both the main checkout and the output workspace. No existing instructions, skills, memory databases, credentials or transcripts are copied. A small environment allowlist avoids inheriting API keys, existing Codex state variables, IDE/session metadata and shell/Python/Node injection settings. Absolute PATH entries are retained so a user-installed CLI and its Node runtime remain usable. The installed executables themselves are trusted operator prerequisites, not sandboxed by this wrapper.

The generated config requests disabled memory injection/generation, app integrations, web search, subagents, shell snapshots and skill dependency installation. It restricts authentication to ChatGPT with file-based credential storage, uses `workspace-write`, disables sandboxed-command network access and extra temporary writable roots, and avoids user shell profile loading. These are documented configuration keys [3]; **requested settings are not proof they were enforced by the installed client**. The config hash and launcher/helper hashes are saved in the run record. The CLI's observed version is saved separately from the still-unknown actual model.

Proxy and custom CA environment settings are intentionally not inherited by the allowlist. A corporate proxy, wrapper binary or unusual shell setup may need an explicit operator-reviewed adaptation. Do not silently broaden the environment or fall back to the old profile when login fails.

## What this does NOT guarantee

This is a lighter, exploratory launch profile, **not a container, mount allowlist or a filesystem jail**. The process still has the same OS user identity. Other readable files may remain reachable; managed settings, system/admin skills and shell policy may still apply. Do not remove mandatory system controls or replace them with permissive settings. `workspace-write` is not a claim that only the two allowed directories are readable. Do not approve requests to access unrelated projects, weaken the sandbox or turn tools back on.

Network restrictions for sandboxed commands do not block Codex's own authentication and model transport. App integrations and web search are separate requested controls, not equivalent to a host-wide network firewall.

Consequently **`isolation_verified` remains false** and unchecked observations stay null. The report must retain `EXPLORATORY; INDEPENDENCE UNVERIFIED`. Known excluded context, missing inputs, inaccessible outputs or mismatched hashes still block the task. Preserve any blocked report and start a new attempt rather than reusing or editing it. If project content still appears, record its reported source name/path without searching unrelated directories. A stronger, separately audited environment is then needed; this wrapper must not certify independence.

Built-in model knowledge cannot be removed by clearing local state. The experiment controls supplied artifacts, not what a model might have encountered during training.

## Files, lifecycle and secrets

```text
RustyBun-review-01/                         unchanged, pinned input pack
phase0-independent-<UTC>-<suffix>-output/
    RUN-RECORD.json                         preflight and launcher observations
    START-REVIEW.txt                        exact saved startup instruction
    independent-design.md                  written only by the reviewer, if it runs
```

The launcher adds observations under `launcher` in `RUN-RECORD.json`. `CLIENT_EXITED` is a client-process observation, **not `COMPLETE` for the task**. It does not overwrite the reviewer's task status, limitations or gate decision. The reviewer records actual execution times and output hashes. A blocking report may use the expected report filename too: read its contents and status, not just its existence.

Normal completion or handled exceptions remove the temporary profile (including its file-based auth cache and local client logs); the output directory is kept. The usual user profile and parent shell environment are untouched. An uncatchable process kill or machine failure can leave a private `/tmp/rustybun-codex-*` directory behind. Inspect and remove only the exact abandoned profile as its owner; never commit auth caches or raw session data. This procedure intentionally does not archive private client transcripts. Audit paths/metadata and the actual report before publishing results.

The launcher is an operator convenience for the first design task, **not the multi-agent migration runner**. All existing gates and forbidden actions remain unchanged. `--update` and `--launch` are deliberate opt-ins; no service/model was run merely by adding this documentation.

## Evidence and references

[Launcher validation](../results/tooling-launcher-20260908/report.md) records fixture tests and their limits. The previous blocked attempt is currently known only from the operator's report.

Official documentation checked on 2026-09-08; an installed client may differ:

1. [Codex instruction discovery](https://developers.openai.com/codex/guides/agents-md)
2. [Config/state locations and project root detection](https://developers.openai.com/codex/config-advanced)
3. [Configuration keys](https://developers.openai.com/codex/config-reference)
4. [Authentication and device-code login](https://developers.openai.com/codex/auth)
5. [User, admin and system skill locations](https://developers.openai.com/codex/skills)
6. [CLI flags, including `--no-alt-screen`](https://developers.openai.com/codex/cli/reference)
