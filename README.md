# RustyBun

An experiment in migrating Bun from Zig to Rust: design the process and its contracts first, then run a measurable pilot using Codex under a subscription plan.

**Status: design-review results archived; process revision pending.** The second round recommends **REVISE_PROCESS** and supplies a candidate v0.2. Both reports and all 34 input hashes were checked. The original record retains role status `COMPLETE` and launcher status `LAUNCH_ERROR`; the launcher's error cause remains unknown. **EXPLORATORY; INDEPENDENCE UNVERIFIED.** G1 is pending; no Bun architecture analysis, baseline compilation or migration is claimed.

## Start here

[Operator handoff](START-HERE.md) · [Project brief](docs/project-brief.md) · [Experiment plan](docs/experiment-plan.md) · [Roles](agents/roles.md) · [Shared contract](agents/contract.md) · [Prompts](prompts/) · [Presentation journal](docs/presentation-journal.md)

## Read the second-round results

[Archive and verification report](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md) · [Design review](results/phase0-design-review-20260909T140149029117Z-9adbe645/design-review.md) · [Candidate v0.2](results/phase0-design-review-20260909T140149029117Z-9adbe645/process-proposal.md) · [Original run record](results/phase0-design-review-20260909T140149029117Z-9adbe645/RUN-RECORD.json)

The archive preserves 40 input/output files byte for byte, including the frozen first design and its supplied provenance. Its root `MANIFEST.json` records the archive mapping; `input/MANIFEST.json` is the original input manifest. Original absolute paths and the launcher error remain historical evidence. This is a closed run, not a workspace to restart.

The review identifies gaps in baseline/judge ownership, verification reserves and accountable checkpoints, and recommends retaining negative judge controls. Reducing architecture scope or default review sessions is a proposal for Damian to decide; the current process remains in force.

## Next step: comparative review, then G1 decision

The existing plan requires a separate comparative review with explicitly selected historical materials and frozen current reports/candidate. Its package and execution have not been prepared or started as part of archiving. After that round, Damian decides which concrete process version and budget to approve. Archiving reports does not approve a gate or authorize a new run.

[Operator handoff](START-HERE.md) describes the current state and evidence limits. To deliberately run another design review, use [the command guide](docs/design-review-command.md); rerunning the second round is not the current next step.

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
