# RustyBun

An experiment in AI-orchestrated migration of Bun from Zig to Rust using Codex and a deliberately designed migration harness.

The repository keeps upstream research artifacts under `sources/github.com/<owner>/<repo>/` so their provenance is explicit. Our own migration design and experiment notes live outside `sources/`.

## Pinned Run A baseline

The first controlled run is pinned to Bun commit:

`46d3bc29f270fa881dd5730ef1549e88407701a5`

This is the Phase-A guide commit. Its parent, `0a7bed5873ad9cc8c2c9203ecf05c1e8754dc49f`, is the identical Bun source tree immediately before `docs/PORTING.md` and `scripts/port-batch.ts` were added.

See:

- `docs/upstream-baseline-analysis.md` — why this is the best reproducible original migration boundary.
- `upstream/bun-baseline.env` — pinned SHAs.
- `scripts/bootstrap-bun-baseline.sh` — reproducible checkout into `work/bun`.

## Initial research sources

- `oven-sh/bun` — the original Bun Zig → Rust Phase-A porting guide and batch tooling.
- `anthropics/code-migration-kit-with-claude-code` — Anthropic's generalized migration workflow derived from large production migrations, including Bun.
- `Lumafy/sumner-method` — a community reconstruction of the implement → adversarial review → fix orchestration pattern.

## Goal

Reproduce and then improve on the original migration process with a staged architecture: analysis/architecture → planning → implementation → adversarial review → testing/fixing, while recording quality, throughput, limits and human intervention.

See `sources/` for mirrored upstream artifacts. Each source folder contains provenance information and preserves the upstream license where applicable.
