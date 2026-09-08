# RustyBun

An experiment in migrating Bun from Zig to Rust: design the process and its contracts first, then run a measurable pilot using Codex under a subscription plan.

**Status: process preparation.** The roles, prompts and review protocol are a v0.1 candidate, not an approved or running multi-agent system. No full Bun architecture analysis, baseline compilation or migration has been completed. Run preparation does not count as a completed review.

## Start here

- [START-HERE.md](START-HERE.md) — handoff instructions for the next model and the operator.
- [Neutral project brief](docs/project-brief.md) — goals, constraints and unknowns without prescribing an agent topology.
- [Execution plan](docs/experiment-plan.md) — stages, deliverables and approval gates.
- [Roles](agents/roles.md) and [shared contract](agents/contract.md) — responsibilities and permission boundaries.
- [Prompts](prompts/) — separate tasks for each role and independent reviewers.
- [Clean-context review](docs/clean-context-review.md) — exactly what the reviewer receives.
- [Presentation journal](docs/presentation-journal.md) — decisions, corrections, hypotheses and narrative material.

## Baseline and sources

Source snapshot for independent analysis: `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`.
Reference commit containing the migration guide: `46d3bc29f270fa881dd5730ef1549e88407701a5`.
The latter adds `docs/PORTING.md` and `scripts/port-batch.ts` without changing Bun's implementation. This is a reproducible Phase A boundary, not proof of the exact state of the author's first private session.

[Baseline analysis](docs/upstream-baseline-analysis.md) · [Pinned SHAs](upstream/bun-baseline.env) · [Source index](sources/README.md).

## Prepare the first review

Run these commands from the RustyBun checkout. Python 3.10+ and Git are required. On systems where Python is named `python`, use that command instead of `python3`.

```bash
python3 -m unittest discover -s tests -v
# Skip this export command if RustyBun-review-01 already exists.
python3 scripts/build-context-pack.py --kind independent-design --out ../RustyBun-review-01
# Prepare metadata and print the complete reviewer handoff in the terminal.
python3 scripts/prepare-review-run.py --pack ../RustyBun-review-01 --out ../RustyBun-review-01-output --run-id phase0-independent-20260908-01 --allow-unverified-isolation
```

The last flag is an **explicit authorization for an exploratory, design-only run while isolation is unverified**. It is not a claim of verified independence. Without the flag, the helper prepares metadata but leaves execution blocked pending operator checks/authorization. It supports `independent-design` only and does not approve any later stage or gate.

The input pack contains `TASK.md`, `MANIFEST.json`, a run-record template and allowlisted inputs. The preparation helper verifies file hashes and creates a **separate output directory** containing:

- `RUN-RECORD.json` — a `PREPARED` record with the run ID, role, stage, process SHA, manifest hash and absolute input/output paths.
- `START-REVIEW.txt` — the operator instruction. Its complete text is also printed automatically, between `BEGIN REVIEWER PROMPT` and `END REVIEWER PROMPT` markers.

**Follow the handoff printed by the script.** It lists the input directory to expose read-only, the output directory to expose read/write, the exact prompt to paste, and where the design report should appear. You do not need to open a separate file or reconstruct instructions from this README. Paste only the text between the markers. `START-REVIEW.txt` remains the saved copy for auditing.

Already prepared the output directory, but have not started the task? Reprint its handoff without overwriting anything:

```bash
python3 scripts/prepare-review-run.py --show-handoff ../RustyBun-review-01-output
```

This read-only mode rechecks the pack, record and saved instruction. It does not create a new run, refresh timestamps, change authorization or restart a used run. It refuses stale inputs/paths/instructions and a record indicating task execution. Existing records from the previous helper are supported when still PREPARED and unchanged.

Give the reviewer access only to the pack and its output directory. Do not attach the main repository or this journal. Paths in the record must be reachable in the agent's environment; remap them and the saved instruction explicitly when using different container mount paths. Known exposure to other proposals or conversation history requires a fresh run. Printing or pasting a prompt does not configure filesystem mounts or a sandbox.

`PREPARED` is not `COMPLETE`: start/end times and measurements remain empty until execution. Unobservable model/client/settings remain `unknown`; unchecked isolation observations remain `null`, and `isolation_verified` stays `false`. The exploratory report must disclose that independence is unverified. Do not change this flag to `true` merely to bypass preflight. Missing inputs, mismatched hashes, inaccessible output and known contamination remain blocking.

Neither script starts a model, signs in to a service or calls a paid API. The operator is responsible for the actual fresh context, filesystem permissions and disabled extra tools. Exporting a folder is not a sandbox or proof of isolation. See the [preflight regression report](results/tooling-preflight-20260908/report.md) and [handoff regression report](results/tooling-handoff-20260908/report.md).

## Later source analysis

Only when the relevant gate allows it, prepare the source checkout for further analysis (Linux/macOS/WSL/Git Bash):

```bash
bash scripts/bootstrap-bun-baseline.sh
```

`sources/` remains an archive; `agents/`, `prompts/`, `workflow/` and `templates/` describe our process; `results/` stores explicitly labelled results. Upstream licenses apply within their respective directories. No new repository-wide license is granted by this documentation change.
