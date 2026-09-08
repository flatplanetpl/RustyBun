# RustyBun

An experiment in migrating Bun from Zig to Rust: design the process and its contracts first, then run a measurable pilot using Codex under a subscription plan.

**Status: process design, before migration.** The operator supplied a first alternative design, labelled `EXPLORATORY; INDEPENDENCE UNVERIFIED`. Its on-server completion record has not been independently inspected here. The next step is a design review of our committed process together with that frozen alternative. No full Bun architecture analysis, baseline compilation, migration or G1 approval is claimed.

## Start here

[Operator handoff](START-HERE.md) · [Project brief](docs/project-brief.md) · [Experiment plan](docs/experiment-plan.md) · [Roles](agents/roles.md) · [Shared contract](agents/contract.md) · [Prompts](prompts/) · [Presentation journal](docs/presentation-journal.md)

## Next step: review both process proposals

From an older checkout, first fetch the new command:

```bash
git pull --ff-only
```

Then, in the normal Ubuntu operator terminal at `~/RustyBun`:

```bash
python3 scripts/design-review.py --update --launch --allow-unverified-isolation
```

This selects the previously identified run `../phase0-independent-20260908T154456Z-output`, checks its completion record and report hash, freezes our committed proposal plus that report in a new context pack, and prepares a separate output directory. It opens Codex in a fresh profile and **automatically submits the saved prompt after device login**. No manual run ID, output path or prompt copying is needed. A different prior run must be selected explicitly with `--prior-run PATH`; the command never guesses the latest run.

Expected outputs are `design-review.md` and `process-proposal.md` in the printed `output_root`. The reviewer must explain what to keep, change, defer or reject in each proposal, and recommend a minimal pilot process without weakening evidence. Its recommendation does not approve G1 or begin migration.

Use `--model EXACT_CLIENT_ID` and optionally `--reasoning CLIENT_SUPPORTED_VALUE` before launch for a specific model. Without them the installed client's defaults are used, **not necessarily the strongest model**. No model IDs or reasoning labels are guessed. Requirements: Python 3.10+, Git, and an installed Codex CLI in a Linux interactive terminal for launch.

Preparation only, no login/model/network:

```bash
python3 scripts/design-review.py --allow-unverified-isolation
```

**Read [the design-review command guide](docs/design-review-command.md)** for record formats, paths, permissions, redisplay, failure handling and the difference between this round and the first one. `--update` fast-forwards only a clean checkout and re-executes updated tooling; it never changes the old pack or results.

## Independent design is a different task

The first round designs an alternative from the brief **without** our proposal. To repeat that experiment deliberately on its existing pack:

```bash
python3 scripts/independent-review.py --update --launch --allow-unverified-isolation
```

Unlike the new design-review command, this older command opens an empty session: select model/settings, then paste the printed prompt between its markers. It preserves the original pack SHA. See [independent-review instructions](docs/independent-review-command.md).

The three rounds are: **independent design → design review of our process and the alternative → later comparison with historical migration materials**. They do not overwrite one another, and a completed report is not a gate approval.

## Isolation and evidence

A separate profile prevents intentional reuse of the old local client state, but is **not a container or proof of isolation**. System policy and other readable files may remain accessible. `isolation_verified` stays false. The first report disclosed a sandbox failure; the new design-review launcher uses `workspace-write` with approval policy `never` and provides no outside-sandbox retry. Known excluded context, inaccessible outputs, missing files or hash mismatches remain blocking. Both proposals are intentionally authorized inputs in the second round.

`--allow-unverified-isolation` is a separate, explicit authorization only for the selected exploratory design task. No migration, gate approval, API-key fallback, credit purchase or quota reset is authorized. Temporary client profiles are removed on normal exit; outputs remain. Never publish authentication caches or raw private session logs.

`PREPARED` is not `COMPLETE`. Actual timestamps, model/settings and measurements must come from execution. The new command verifies the expected output files/hashes after client exit, but does not turn missing results into success.

## Baseline and archived sources

Source for independent analysis: `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`.
Reference guide commit: `46d3bc29f270fa881dd5730ef1549e88407701a5`.
The latter adds `docs/PORTING.md` and `scripts/port-batch.ts` without changing Bun's implementation. It is a reproducible Phase A boundary, not proof of the first private session's exact state.

[Baseline analysis](docs/upstream-baseline-analysis.md) · [Pinned SHAs](upstream/bun-baseline.env) · [Sources](sources/README.md) · [Clean-context protocol](docs/clean-context-review.md)

`sources/` is an archive; our process lives in `agents/`, `prompts/`, `workflow/` and `templates/`; `results/` stores explicitly labelled evidence. Upstream licences apply in their respective directories. This change grants no new repository-wide licence.

## Low-level tools and validation

The existing exporter and preparation helper remain supported; see [preflight instructions](docs/preflight-start.md). Do not re-export an existing first-round pack to repair a run. The second-round wrapper adds the prior report before freezing a new pack; the raw exporter alone is not the complete second-round command.

```bash
python3 -m unittest discover -s tests -v
```

[Design-review tests](results/tooling-design-review-20260908/report.md) · [Independent launcher tests](results/tooling-launcher-20260908/report.md) · [Preflight tests](results/tooling-preflight-20260908/report.md) · [Handoff tests](results/tooling-handoff-20260908/report.md)

Only after the relevant gate permits source analysis:

```bash
bash scripts/bootstrap-bun-baseline.sh
```
