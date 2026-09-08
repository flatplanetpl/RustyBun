# Design-review command validation — 2026-09-08

## Scope

Added a second-round operator command, `scripts/design-review.py`, and expanded `prompts/08-design-review.md` to compare our committed process with the frozen alternative. The design-review allowlist includes the new command/test and existing launcher; pipeline metadata describes the command and additional proposed-process report. Gate states, experiment scope, first-round prompt, original exporter, preflight helper and independent launcher are unchanged. README/START-HERE explain the next step, and journal J029–J032 preserve the distinction between a supplied exploratory design and verified independence.

The operator supplied the first design in a pasted transcript, not its original run-record file. The command reads the actual report and record on the operator's server at preparation time. No replacement record or claimed source-report hash was invented here. No private transcript or raw credentials were committed.

## Executed validation

`python3 -m unittest discover -s tests -p 'test_design_review.py' -v` — **34/34 PASS**, Python 3.13.5, Linux, Git 2.47.3. Raw output: [test-output.txt](test-output.txt). Syntax compilation of the new script and test module passed. Workflow JSON parsing passed; all G1–G5 gate objects remain byte-equivalent in content to the previous configuration. The original workflow JSON and journal were reconstructed from connector reads and checked against their exact Git blob IDs before modifying them; the journal is append-only.

Tests exercise the real existing exporter and preflight helper on small local repositories, closed earlier-run records and UTF-8 reports. Coverage includes exact copying and hash provenance, explicit prior-run selection, no raw-record/session leakage into inputs, failed/missing/ambiguous completion records, moved runs, unchanged original inputs, new read-only mode bits, forbidden symlinks and local edits, separate unique run paths, stale handoff/profile detection, no implicit authorization, read-only redisplay, no restart, and CLI validation.

Codex version/login/interactive subprocesses are **simulated**: tests verify environment separation, exact automatic initial-prompt submission, no outside-sandbox fallback, cleanup, validation after login, preservation of task/gate status, both required output hashes, and non-success on a client exit without a completed review. The sandbox-failure case is simulated; it does not establish a working sandbox on the operator's host.

One test uses a real local bare Git remote and cloned checkout. `--update` performs a fast-forward, re-executes the current command, creates exactly one new review attempt, and preserves the previous report and old input-pack bytes. No network remote or model is used.

## Reused files

The unchanged files used locally match these existing Git blobs:

- `scripts/build-context-pack.py`: `e5b57587e7d93b4f52a11e5588f837b4f9f7e764`.
- `scripts/prepare-review-run.py`: `9f4700ae0b8d49da7cff0747894c3d55be7dd2d7`.
- `scripts/independent-review.py`: `dfdbfe66344476e9c09a99710dbe7a32d7b559df`.

Changed-file SHA-256 and Git blob receipts: [file-hashes.json](file-hashes.json). They describe the exact local files tested/prepared, not the operator's runtime settings.

## Limits

The earlier repository test modules were not rerun; the result above is the **new 34-test module**, not the whole historical suite. It uses small fixture allowlists rather than the entire upstream source archive. Python 3.10, Windows and macOS were not executed. The optional TOML-parser test skips on Python 3.10, where the launcher itself does not require tomllib.

No actual Codex binary enforcement, device login, model/effort choice, memory isolation, read allowlist, token/quota measurement, prior server run record, full Bun build or migration was validated. `isolation_verified=false`; no gate is approved. A hash agreement is not an authenticated signature. A profile is not a filesystem jail, and read-only permission bits can be changed by their owner. The second-round script refuses escalation instead of silently working around the sandbox failure described in the earlier report.

Direct Git clone failed DNS resolution in this workspace. Repository reads and publication use the GitHub connector. The official configuration reference and current Codex CLI source were checked for the approval/initial-prompt interfaces; that does not guarantee the operator's installed client version. Real runtime validation remains a separate operator-run attempt.
