# Design review: compare the two process proposals

**v0.2 preparation:** this command is retained for a deliberately selected new methodology review, not the next automatic task. The closed second round remains archived. New packs include D01–D08 as explicit operator constraints and the current process; the required comparative review remains a separate step before G1. Main pilot responsibilities do not require new sessions. See [handoff](../START-HERE.md).

## Which round is this?

`independent-design` produced an alternative process from the neutral brief, without our proposal. **`design-review` now critiques our committed process and that frozen alternative together.** A later `comparative-review` can introduce historical migration materials. They are different tasks, not repeated attempts to obtain a preferred verdict.

On 2026-09-08 the operator supplied the first design as pasted terminal output and requested this next round. That report labels itself `EXPLORATORY; INDEPENDENCE UNVERIFIED`, describes a sandbox failure followed by approved outside-sandbox file operations, and discloses one internal subagent. These are the report's statements, not an independent audit of the server. The original `RUN-RECORD.json` was not available during development. The new command checks it locally at preparation time; it does not manufacture it from the pasted transcript.

The reviewer assesses evidence without assuming that fewer agents improve quality. D01–D08 explicitly select the scope of the prepared pilot; a recommendation to change those decisions must be labelled for the operator, not silently applied. It should identify what to keep, change, defer or reject, and propose the smallest credible pilot process without weakening evidence. Its recommendation is **not** Damian's G1 approval.

## One command on the server

Requirements: Python 3.10+, Git, a clean RustyBun checkout; for `--launch`, an installed Codex CLI and a Linux interactive terminal. Run as the operator, not in a reviewer session. From an older checkout, obtain the new command once:

```bash
git pull --ff-only
```

Then run from `~/RustyBun`:

```bash
python3 scripts/design-review.py --update --launch --allow-unverified-isolation
```

The default prior run is **explicitly selected**, not discovered by taking the newest folder:

```text
../phase0-independent-20260908T154456Z-output
```

This is the completed run identified by the operator. To select a different completed run, add `--prior-run PATH`. The command does not search the home directory or inspect other runs. No manual run ID, output path or prompt copying is needed.

With `--launch`, device login uses the existing ChatGPT account in a fresh temporary profile. **After login the saved startup prompt is submitted automatically** as the CLI's initial user prompt. There is no empty-session/paste step in this command. This differs intentionally from `independent-review.py`.

Use `--model EXACT_CLIENT_ID` and optionally `--reasoning CLIENT_SUPPORTED_VALUE` to select known settings before submission. Omitted model/effort means the installed client's defaults, not automatically the strongest available model; the actual values must be recorded from execution. Unsupported values must fail, not fall back to another model or billing mode. There is no copied login cache, API-key fallback, installation or purchase; account limits remain the same.

## What is frozen and checked

The command reads only the selected `independent-design.md` and `RUN-RECORD.json`. It requires a closed `method-independent` / `independent-designer` record, with status `COMPLETE` (also accepts `COMPLETED`), start/end timestamps, process SHA, original input-manifest hash, run ID and original output path. It checks the report against the SHA-256 already recorded at completion.

Supported output-artifact forms are a list of objects with `path` and `sha256`, or a map from filename to digest/object. `file` and `filename` are accepted path aliases. A matching absolute original output path is also accepted when a closed run was moved. Ambiguous entries, absent hashes, mismatches and BLOCKED/PREPARED attempts fail before a new pack is published. Do not edit the old record or hash just to pass a check. A different record layout requires an explicit, reviewed adapter, not silent guessing.

The existing exporter freezes the `design-review` allowlist from one committed `HEAD`, including the current process and D01–D08 as explicitly authorized constraints. The journal and conversation transcript remain excluded. The command adds a byte-for-byte report copy and a minimal provenance JSON before finalizing a **new** manifest. The raw old record, terminal transcript, session IDs and additional coordinator commentary are not copied; D01–D08 is the explicit decision input described above. The source report itself is not redacted or rewritten. Review its contents before any public sharing.

The provenance preserves the old process/manifest identifiers, completion claim, report/record hashes and reported isolation/model metadata. It explicitly states that the previous input manifest and session were **not** re-audited. Hash agreement proves the copied bytes agree with the supplied record, not that the record is signed, authentic, or the session was independent. The old `RustyBun-review-01` pack, its SHA and all earlier results remain untouched. `--update` changes tooling/current proposal only, not the earlier experiment.

## Result layout

Every attempt creates a unique sibling directory:

```text
phase0-design-review-<timestamp>-<suffix>/
├── input/                       # New frozen context pack
│   ├── TASK.md
│   ├── AGENTS.md
│   ├── MANIFEST.json
│   ├── RUN-RECORD.template.json
│   └── input/
│       ├── docs/, agents/, ...  # Allowlisted committed proposal
│       └── prior/
│           ├── independent-design.md
│           └── provenance.json
└── output/                      # output_root / Codex working directory
    ├── RUN-RECORD.json           # PREPARED before execution
    ├── START-REVIEW.txt          # Automatically submitted with --launch
    ├── PROFILE.toml             # Requested settings, no credentials
    ├── design-review.md         # Created by reviewer, not preparation
    └── process-proposal.md      # Proposed correction of assessed v0.2, not automatically applied
```

New input files receive read-only permission bits; old files' permissions are not changed. Their owner can still change permissions, so this is not an immutable mount or a security boundary. The launcher rechecks input integrity before launch, after login and after client exit. COMPLETE requires both reports, their matching recorded hashes and execution timestamps. Client exit alone returns a non-success result (code 3 when the client itself exited zero without a completed review). The script never changes the reviewer's task status to COMPLETE or approves a gate.

## Sandbox and scope

This round reuses the existing profile/environment helpers: a new HOME/CODEX_HOME/XDG set, restricted inherited environment, requested disabled memory, app integrations, browsing and subagents. The main repo and coordinator history are not supplied as task inputs. The new command additionally requests **`workspace-write` with approval policy `never`**: no escalation outside the sandbox when it fails. It does not use a bypass flag. A sandbox failure is a blocker, not permission to repeat file operations without it.

A fresh profile and file modes do not enforce a complete read allowlist. System/admin policy and readable external files may still exist. Keep `isolation_verified=false`; preserve the exploratory label. General platform instructions still apply. Both supplied proposals and D01–D08 are intentionally allowed in new packs for this round; other project histories/instructions remain excluded. Do not ask the reviewer to ignore known exposure. Do not treat a failed sandbox as fixed merely because the launcher exists.

`--allow-unverified-isolation` here authorizes **design-review only**, separately from the earlier independent-design authorization. It does not authorize migration, extra agents, paid API, gate approval or modifying either proposal. Without it, preparation is possible but review execution is blocked.

## Other modes and recovery

Offline preparation only:

```bash
python3 scripts/design-review.py --allow-unverified-isolation
```

This creates a new prepared attempt and prints the exact prompt, but starts no client. For a read-only redisplay of an unused attempt, pass the printed **run directory**, not its input or output child:

```bash
python3 scripts/design-review.py --show-handoff ../phase0-design-review-<id>
```

`--output-parent PATH` and `--run-id ID` are optional. Existing destinations are never overwritten. Dirty checkouts, failed fast-forward updates, missing earlier records, bad hashes and incompatible clients stop the command. A login attempt or started/closed review is not restarted with redisplay. Another normal invocation creates another attempt; preserve failures. No automatic resume, sandbox relaxation or API fallback occurs.

Exporter/preflight/independent-launcher CLI and profile behavior remain unchanged. New configuration/templates use schema_version 0.2; the exporter manifest format remains 0.1. Existing packs retain their original template and process SHA. Exporting `--kind design-review` alone is not sufficient for this second-round prompt: it also requires the frozen prior result. Use this wrapper for the complete step. No gate state in `workflow/pipeline.json` is changed.

## Documentation basis and validation

Official references checked on 2026-09-08: [configuration](https://developers.openai.com/codex/config-reference), [CLI source: initial prompt and approval flag](https://github.com/openai/codex/blob/main/codex-rs/tui/src/cli.rs), and the existing [profile rationale](independent-review-command.md). The installed client may differ; requested settings are not evidence that it enforced them. No model ID or universal maximum reasoning label is assumed.

See [test report](../results/tooling-design-review-20260908/report.md). Tests use real local Git/export/preflight functions and explicitly simulated Codex calls. They do not verify real login, effective sandbox isolation or the operator's actual prior record.
