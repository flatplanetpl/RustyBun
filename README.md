# RustyBun

An experiment in migrating Bun from Zig to Rust: design the process and its contracts first, then run a measurable pilot using Codex under a subscription plan.

**Status: process preparation.** The roles, prompts and review protocol are a v0.1 candidate, not an approved multi-agent migration system. The operator reported a review blocked by extra project context; no completed independent design has been verified here. No full Bun architecture analysis, baseline compilation or migration has been completed. Run preparation and opening a client do not count as a completed review.

## Start here

- [START-HERE.md](START-HERE.md) — handoff instructions for the next model and the operator.
- [Independent review command](docs/independent-review-command.md) — one-command preparation/start, separate Codex profile, rationale and limitations.
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

## Start a new independent-design attempt

Use a normal operator terminal on Ubuntu/Linux, not an existing reviewer session. Requirements: Python 3.10+, Git and Codex CLI already installed for `--launch`. From an older checkout, first run `git pull --ff-only` once to obtain the new command.

With the existing `../RustyBun-review-01` input pack, run from the RustyBun checkout:

```bash
python3 scripts/independent-review.py --update --launch --allow-unverified-isolation
```

The command updates a clean checkout using `git pull --ff-only`, creates a unique run ID and new output directory, verifies the unchanged input pack, prepares the run record and prints the complete handoff. It then requests ChatGPT device-code login in a fresh temporary profile and opens an empty Codex CLI session in the output directory. **Select the model/settings, then paste only the text between `BEGIN REVIEWER PROMPT` and `END REVIEWER PROMPT`.** No manual `RUN_ID`, `--out` or `--show-handoff` step is needed.

The existing pack retains its original process SHA even if tooling is updated. Previous outputs, including blocked attempts, remain untouched. The expected report is `independent-design.md` in the newly printed output directory. Opening/exiting Codex is not proof that this report was completed.

**Why a separate profile?** A reviewer reported seeing unrelated instructions and memory before starting the task. A new folder or conversation alone did not prevent that. The launcher separates local home/config/state and requests disabled memory, app integrations and browsing. This is **not a container or a proof of isolation**; system policy and other readable files may remain accessible. Known excluded context still blocks work. [Details, sources and failure handling](docs/independent-review-command.md).

`--allow-unverified-isolation` is explicit authorization for an exploratory design-only task. It never sets `isolation_verified=true` or approves any gate. Same account, same limits; no API-key fallback or credit purchase. The temporary profile is removed on normal client exit; outputs are retained. Never publish auth caches or raw private client logs.

Preparation only, without Git/network, login or client launch:

```bash
python3 scripts/independent-review.py --allow-unverified-isolation
```

Omit `--update` to keep the current launcher checkout. Use `--pack PATH` for another existing pack; `--model` and `--reasoning` accept exact values supported by the installed client. Run `python3 scripts/independent-review.py --help` for all options. No model IDs or maximum-reasoning labels are guessed.

## Input export and low-level helpers

Only export when the input pack does not exist; do not replace an already reviewed pack:

```bash
python3 scripts/build-context-pack.py --kind independent-design --out ../RustyBun-review-01
```

The exporter creates `TASK.md`, `MANIFEST.json`, a run-record template and allowlisted inputs. It does not start a model or create a completed runtime record. The wrapper above uses the existing `prepare-review-run.py` helper, whose manual interface remains supported:

```bash
python3 scripts/prepare-review-run.py --pack ../RustyBun-review-01 --out ../NEW_OUTPUT_DIR --run-id NEW_RUN_ID --allow-unverified-isolation
# Redisplay only when that run is still PREPARED and has not started:
python3 scripts/prepare-review-run.py --show-handoff ../NEW_OUTPUT_DIR
```

The helper creates `RUN-RECORD.json` and `START-REVIEW.txt`, and prints exactly what to give the reviewer. It neither logs in nor launches Codex. `--show-handoff` does not create a missing record or restart a used run. [Preflight documentation](docs/preflight-start.md).

`PREPARED` is not `COMPLETE`. Actual timestamps, model/settings and measurements must come from execution; unchecked observations remain unknown. Missing inputs, mismatched hashes, unavailable outputs and known contamination remain blocking. Do not share the main repository, presentation journal or conversation history with the independent designer. Input permissions and effective sandbox controls still need operator verification.

## Validation and later source analysis

```bash
python3 -m unittest discover -s tests -v
```

[Launcher checks and limitations](results/tooling-launcher-20260908/report.md) · [Preflight checks](results/tooling-preflight-20260908/report.md) · [Handoff checks](results/tooling-handoff-20260908/report.md).

Only after the relevant gate permits source analysis (Linux/macOS/WSL/Git Bash):

```bash
bash scripts/bootstrap-bun-baseline.sh
```

`sources/` remains an archive; `agents/`, `prompts/`, `workflow/` and `templates/` describe our process; `results/` stores explicitly labelled results. Upstream licenses apply within their respective directories. No new repository-wide license is granted by this documentation change.
