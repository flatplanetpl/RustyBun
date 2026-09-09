# RustyBun

An experiment in migrating Bun from Zig to Rust: prepare the process and its contracts, then run a measurable pilot using Codex under a subscription plan.

**Status: process v0.2 prepared; operator review and G1–G5 remain PENDING.** The active plan, roles, prompts, templates and pipeline now implement [D01–D08](docs/decisions/2026-09-09-pilot-v0.2.md): one bounded slice, one main sequential working session and one active writer. This preparation does not select a Bun slice, approve a budget or authorize migration.

The original must run and the verifier must pass positive and negative controls before G3 and implementation. Review is mandatory; two separate reviewers are not the default. Its kind and scope are agreed before implementation, self-review is disclosed, and Damian assesses evidence and accepts the result. Difficult boundaries require competent additional review or a narrower/different slice.

## Start here

[Operator handoff](START-HERE.md) · [Agreed decisions](docs/decisions/2026-09-09-pilot-v0.2.md) · [Project brief](docs/project-brief.md) · [Experiment plan](docs/experiment-plan.md) · [Roles](agents/roles.md) · [Shared contract and record fields](agents/contract.md) · [Prompts](prompts/) · [Presentation journal](docs/presentation-journal.md)

## Prepared process and next steps

The [pipeline](workflow/pipeline.json) describes prerequisites; `executable_runner=false`. The operator checks evidence and approvals. The migration-unit template separates resource limits from verification reserves; the run record tracks usage, human/model edits and checkpoints. Unknown values remain null. Any candidate edit requires fresh review and parity for the new hash. A continuation preserves consumed resources and fix rounds; it does not restart the budget.

Review this preparatory change with Damian. Then separately prepare the required **comparative review** with historical materials, explicit inputs/hashes, frozen reports and proposal, a run record and execution conditions. That round has not been performed or waived. G1 still requires Damian's decision on a concrete process version and budget. Slice selection, environment, model/settings, numeric limits/reserves and the slice's review plan remain open.

[Preparation checks and D01–D08 mapping](results/tooling-process-v02-20260909T174417Z/report.md) record tooling evidence. They do not establish Bun build readiness, verifier effectiveness, migration parity or human acceptance. No new review agent or orchestration platform was used to prepare v0.2.

## Frozen methodology results

[Archive and verification report](results/phase0-design-review-20260909T140149029117Z-9adbe645/report.md) · [Design review](results/phase0-design-review-20260909T140149029117Z-9adbe645/design-review.md) · [Reviewer's candidate v0.2](results/phase0-design-review-20260909T140149029117Z-9adbe645/process-proposal.md) · [Original run record](results/phase0-design-review-20260909T140149029117Z-9adbe645/RUN-RECORD.json)

The second-round archive preserves 40 input/output files byte for byte, including the first design and its supplied provenance. Verdict **REVISE_PROCESS**, role status `COMPLETE`, launcher status `LAUNCH_ERROR` and **EXPLORATORY; INDEPENDENCE UNVERIFIED** remain unchanged. The launcher's error cause, actual model/settings, quota and independence remain unknown. Original paths are historical metadata, not instructions to resume the closed run.

The adopted decisions select the scope of this preparation; the reviewer's full proposal is not automatically accepted. Earlier reports and the decision record retain their historical meaning.

## Methodology review commands

The three rounds remain **independent design → design review of our process and the frozen alternative → comparative review with historical migration materials**. They have separate context rules. This does not impose separate Architect/Planner/Fixer sessions on the pilot. A fresh independent-design export still receives only the neutral brief and administrative template, without the adopted method.

Repeating a completed round would be a new, explicitly selected attempt; it is not the next step. [Independent-design guide](docs/independent-review-command.md) · [Design-review guide](docs/design-review-command.md) · [Preflight and handoff](docs/preflight-start.md). The raw design-review exporter does not add the required prior report; its existing wrapper does. No comparative-review launcher is added here, and no operational comparative pack is prepared by this commit.

## Isolation and evidence

A separate profile is not a container or proof of isolation. The existing design-review launcher requests `workspace-write` with approval policy `never`, without an outside-sandbox retry. `isolation_verified` stays false. Known excluded context, inaccessible outputs, missing files and hash mismatches remain blocking. Both proposals and the decision record are deliberately authorized inputs of new design-review packs; the journal and conversation history remain excluded.

`--allow-unverified-isolation` authorizes only the explicitly selected exploratory methodology task. It does not approve migration, gates, paid API, credit purchases or quota resets. Never publish authentication caches or raw private sessions. `PREPARED`, `COMPLETE`, mechanical verification and operator acceptance mean different things.

## Baseline and archived sources

Pinned source: `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`.
Reference guide commit: `46d3bc29f270fa881dd5730ef1549e88407701a5`.
The latter adds `docs/PORTING.md` and `scripts/port-batch.ts` without changing Bun's implementation. It is a reproducible Phase A boundary, not proof of the first private session's exact state.

[Baseline analysis](docs/upstream-baseline-analysis.md) · [Pinned SHAs](upstream/bun-baseline.env) · [Sources](sources/README.md) · [Context protocol](docs/clean-context-review.md)

`sources/` is an archive. Our process lives in `agents/`, `prompts/`, `workflow/` and `templates/`; `results/` stores labelled evidence. Upstream licences apply in their respective directories. This preparation grants no new repository-wide licence. No Bun source analysis, baseline compilation or migration is claimed.

## Local validation

```bash
python3 -m unittest discover -s tests -v
```

The tests exercise real local Git/export/preflight and simulated client calls; they do not run models or Bun. CLI and exporter manifest format remain unchanged; new process configuration/templates use version 0.2. Old packs are never rewritten to match new templates.

Only after the relevant gate and source-access authorization:

```bash
bash scripts/bootstrap-bun-baseline.sh
```
