# Bun upstream baseline analysis

## Decision

For the first RustyBun run we will use **`oven-sh/bun@46d3bc29f270fa881dd5730ef1549e88407701a5`** as the execution baseline.

This is the strongest reproducible candidate for the state from which Bun's Zig → Rust Phase A started.

## Why this commit

On **2026-05-04 13:20:04 UTC**, commit `46d3bc29f270fa881dd5730ef1549e88407701a5` was created with message:

> `docs: add Phase-A porting guide`

That commit added exactly two migration artifacts:

- `docs/PORTING.md` — 576-line Zig → Rust rulebook
- `scripts/port-batch.ts` — Phase-A batch selector

It did **not** change Bun application/source implementation. Its parent is:

- `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`
- timestamp: 2026-05-04 10:20:16 UTC

Therefore:

- **raw source snapshot** = `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`
- **execution snapshot** = `46d3bc29f270fa881dd5730ef1549e88407701a5`

The source code is the same in both snapshots; the latter additionally contains the Phase-A rulebook and batching script.

## Evidence that this belongs to the actual rewrite lineage

The merged rewrite PR is `oven-sh/bun#30412` (`Rewrite Bun in Rust`).

The public PR metadata shows:

- head branch: `claude/phase-a-port`
- merged: 2026-05-14
- 2,188 changed files
- 1,009,257 additions
- 6,755 commits reported by the PR metadata

A lineage comparison from `46d3bc29...` to an early commit currently exposed by the PR (`6033d710...`) reports `46d3bc29...` as the merge-base and the PR commit as **6,475 commits ahead**. In that interval the repository gained the migration machinery (`.claude/workflows/*`), `docs/LIFETIMES.tsv`, Cargo workspace files, Rust source files, and many later migration documents.

That makes `46d3bc29...` a clean boundary: the rulebook exists, but the large-scale generated Rust migration machinery has not yet accumulated.

## Why not use the PR base SHA

PR #30412 currently records base SHA:

`0d9b296af33f2b851fcbf4df3e9ec89751734ba4`

That commit is **25 commits ahead** of the parent of the Phase-A guide (`0a7bed...`). Those 25 commits include unrelated ongoing Bun development, including changes under `src/http`, `src/sys`, `src/runtime`, tests, docs and build files.

Using that later base would make the experiment less controlled: we would no longer be comparing Codex against the same source snapshot for which the original Phase-A rulebook was authored.

## Experimental strategy

### Run A — reproduction

Use exactly:

```text
repo:        https://github.com/oven-sh/bun
run SHA:     46d3bc29f270fa881dd5730ef1549e88407701a5
source SHA:  0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f
rulebook:    docs/PORTING.md from 46d3bc29
batch tool:  scripts/port-batch.ts from 46d3bc29
```

Goal: maximize comparability with the original experiment.

### Run B — robustness experiment (later)

Only after Run A, repeat the methodology on another **pre-Rust-rewrite** Bun snapshot. This tests whether our architecture/planner layer generalizes instead of merely exploiting the exact snapshot for which the original rulebook was written.

Do not use current Bun `main` for this comparison: after the Rust rewrite it is no longer an independent Zig → Rust migration target.

## Important methodological distinction

We should preserve two baselines:

1. **Original/Sumner baseline** — structure-preserving translation following the upstream rulebook.
2. **RustyBun baseline** — Architect → Planner → Implementer → 2× Reviewer → Fixer → Referee, with dependency/contract analysis allowed before implementation.

Both must start from the same upstream source SHA. Otherwise a quality/cost comparison is not meaningful.

## Confidence

**High** that `46d3bc29...` is the correct reproducible Phase-A starting boundary.

Public history cannot prove the exact filesystem state at the instant the first agent process was launched, but the evidence is unusually strong: the Phase-A rulebook commit is an ancestor of the rewrite lineage, its parent is known, and that commit changes only the two migration-control artifacts.
