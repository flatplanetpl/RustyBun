# RustyBun

An experiment in AI-orchestrated migration of Bun from Zig to Rust using Codex and a deliberately designed migration harness.

The repository keeps upstream research artifacts under `sources/github.com/<owner>/<repo>/` so their provenance is explicit. Our own migration design and experiment notes will live outside `sources/`.

## Initial research sources

- `oven-sh/bun` — the original Bun Zig → Rust Phase-A porting guide and batch tooling.
- `anthropics/code-migration-kit-with-claude-code` — Anthropic's generalized migration workflow derived from large production migrations, including Bun.
- `Lumafy/sumner-method` — a community reconstruction of the implement → adversarial review → fix orchestration pattern.

## Goal

Reproduce and then improve on the original migration process with a staged architecture: analysis/architecture → planning → implementation → adversarial review → testing/fixing, while recording quality, throughput, limits and human intervention.

See `sources/` for mirrored upstream artifacts. Each source folder contains provenance information and preserves the upstream license where applicable.
