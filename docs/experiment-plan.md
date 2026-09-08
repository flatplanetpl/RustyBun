# RustyBun experiment plan

## Research question

Can a single developer using Codex under a subscription plan reproduce meaningful progress on Bun's Zig → Rust migration by engineering the migration process rather than manually steering individual code edits?

A second, more interesting question is whether we can improve on a purely mechanical translation by analysing architecture, dependencies, contracts and semantic gaps before fan-out.

## Core principles

1. **Evidence before implementation.** Decisions about migration order, ownership, dependencies and verification should come from repository evidence, not model intuition.
2. **The old implementation is the executable specification.** We need a parity judge that can exercise old and new implementations through the same external surface.
3. **Separate architecture from translation.** Before coding, decide where structure can be preserved and where a dependency should be replaced, reduced to a smaller contract or redesigned.
4. **Deterministic artifacts beat agent memory.** Dependency maps, manifests, inventories and rulebooks are files that every later agent consumes.
5. **Independent roles.** The intended production loop is Architect/Planner → Implementer → Reviewer A + Reviewer B → Fixer → compiler/tests/parity judge.
6. **Adversarial review is independent.** Reviewers should not inherit the implementer's reasoning and should assume the translation is wrong until evidence says otherwise.
7. **Human intervention changes the process first.** Prefer fixing the rulebook, inventory, decomposition or workflow over manually repairing individual translated lines.
8. **Every run is measurable and resumable.** Progress and failures live on disk, not only in model context.

## Phase 0 — freeze and measure the baseline

- Identify and pin the exact Bun commit immediately before the Rust migration work begins.
- Record the corresponding migration commit/PR as the reference result.
- Build Bun from the baseline and record build time, test time and environment.
- Record source-file counts, relevant Zig LOC and test counts.
- Create `migration/cost-log.tsv` and a deviation log.
- Record Codex quota/reset consumption separately from any hypothetical API-token equivalent.

**Gate:** baseline builds and tests successfully and can be reproduced.

## Phase 1 — feasibility and the parity judge

Use the Anthropic migration kit as a starting rubric, adapted to Codex and Bun:

- run the feasibility survey;
- classify tests as portable/public-surface versus language-internal;
- decide whether the existing test suite is sufficient as a cross-language judge;
- if not, build the judge before translation begins;
- validate the judge against the original implementation and deliberately injected faults.

This phase also produces the first explicit answer to:

> Which parts of Bun should be structure-preserving translations and which parts deserve redesign or dependency substitution?

**Gate:** we have a trustworthy mechanical definition of parity.

## Phase 2 — architecture, dependency graph and semantic-gap inventory

### 2.1 Deterministic dependency graph

Build a script that parses Zig imports/build relationships and produces:

- direct in-repo dependency edges;
- strongly connected components;
- topological migration order where possible;
- crate/module-level condensation;
- a machine-readable work manifest.

Review the generated map adversarially on independent samples. A confirmed miss fixes the parser and regenerates the entire map.

### 2.2 Architectural classification

For each subsystem or dependency boundary classify it as one of:

- **PORT 1:1** — preserve implementation/architecture;
- **ADAPT** — preserve behaviour but use a Rust-native implementation or crate;
- **MINIMAL CONTRACT** — Bun consumes only a small surface of a large dependency; implement that surface rather than cloning the dependency;
- **BRIDGE** — temporarily keep Zig/C/C++ behind FFI;
- **REDESIGN** — structure should change in Rust, with an explicit compatibility contract.

This is where our experiment intentionally differs from blindly translating files.

### 2.3 Semantic-gap inventory

Inventory cross-file decisions that implementers must not guess, especially:

- ownership and lifetimes;
- arenas and allocator semantics;
- FFI and JavaScriptCore rooting/lifetime rules;
- comptime/generics/reflection;
- bytes versus strings;
- error semantics;
- intrusive reference counting and pointer layouts;
- concurrency/thread affinity;
- event-loop and syscall boundaries;
- platform-specific code.

The original Bun `PORTING.md` is evidence and a baseline rulebook, not unquestionable policy.

**Gate:** dependency map, architecture decisions, gap inventory and first RustyBun rulebook are signed off.

## Phase 3 — stress-test the migration rules

Select a small set of intentionally difficult units. Prefer units that exercise several risky rules and dependency boundaries rather than easy files.

Run two approaches independently:

- **A — rulebook-faithful:** translate according to the current RustyBun rulebook;
- **B — native Rust baseline:** solve the same behavioural problem as an experienced Rust engineer without seeing the rulebook.

Then compare them with a separate inspector. In parallel run the intended production agent loop:

`Planner → Implementer → Reviewer A + Reviewer B → Fixer → referee`

Nothing from the bakeoff has to ship. Its main product is improved migration policy.

**Gate:** a second sample does not expose a repeated systemic rule failure.

## Phase 4 — controlled translation fan-out

Work from the manifest in dependency-aware batches.

For every unit:

1. planner reads the dependency/architecture decision and defines the contract;
2. implementer produces the Rust change;
3. two independent adversarial reviewers inspect source versus target and rule compliance;
4. disagreements are resolved by evidence, not majority vote;
5. fixer applies confirmed findings only;
6. unresolved issues become greppable `TODO(port)`, `PERF(port)` or `BUG(port)` artifacts;
7. completion is recorded mechanically on disk.

Start with small batches. Scale parallelism only after measured first-pass quality is stable.

## Phase 5 — compiler convergence

Compiler diagnostics become a machine queue rather than an invitation for free-form repair.

- Run a controlled survey build.
- Parse diagnostics by crate/module and dependency order.
- Give fixers diagnostics and source context.
- Review fixes independently.
- Re-run the compiler centrally per round.
- Repeated error classes indict the rulebook or shared abstraction; fix the systemic source and regenerate affected units where appropriate.

**Gate:** clean build across the target workspace.

## Phase 6 — behavioural convergence

- Run the parity judge continuously.
- Run the original Bun suite where portable.
- Exercise CLI/runtime/package-manager/networking/file-system scenarios through public interfaces.
- Track every behavioural divergence as a queue item with old/new outputs.
- Only call parity when the mechanical judge is green and the original baseline still passes its own suite.

## Phase 7 — post-parity quality and performance

Only after behavioural parity:

- burn down `TODO(port)`, `BUG(port)` and `PERF(port)` markers;
- benchmark old versus new implementations;
- audit unsafe code and FFI assumptions;
- remove temporary Zig bridges where justified;
- simplify architecture where the migration intentionally preserved awkward source shapes.

## Agent roles for RustyBun

### Architect

Owns subsystem boundaries, contracts, dependency strategy and preserve/adapt/redesign decisions. Does not write production translation code.

### Planner

Turns an architectural decision into a bounded unit of work: inputs, dependencies, expected outputs, invariants, tests and known gaps.

### Implementer

Writes the code according to the plan and rulebook. It does not review its own work.

### Reviewer A / Reviewer B

Independent adversarial contexts. They compare behaviour, contracts, memory/lifetime assumptions and rule compliance. They cite concrete evidence.

### Fixer

Applies only confirmed findings and records unresolved issues explicitly.

### Referee

Compiler, test suite and parity judge. The referee should be as deterministic as possible and should not be replaced by model judgment.

## What we measure

For each batch and for the experiment overall:

- source units and LOC attempted/completed;
- wall-clock time;
- human active-attention minutes;
- Codex quota/reset consumption;
- first-pass compile success;
- compiler errors per translated unit;
- reviewer findings per unit and confirmed-finding rate;
- parity regressions introduced and fixed;
- unresolved marker count;
- number of rulebook/inventory amendments;
- number of manual code edits by the human;
- throughput before and after process amendments.

The most interesting metric is not raw LOC generated. It is **how much correct, reviewable, parity-preserving migration progress we get per unit of human attention and subscription quota**.

## First concrete milestone

Do not attempt the million-line port first. The first milestone is complete when we have:

1. the exact pre-migration Bun baseline pinned;
2. a reproducible build/test baseline;
3. a dependency-map prototype;
4. a parity-judge decision;
5. a first architecture/gap report;
6. three deliberately difficult migration units run through the complete RustyBun workflow;
7. enough measurements to decide whether scaling the experiment is justified.
