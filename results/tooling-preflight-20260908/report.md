# Review preflight regression report — 2026-09-08

## Scope and finding

The operator reported an independent-design attempt stopping before work because only RUN-RECORD.template.json was supplied, with no actual record/output_root. In process commit fbf1b25115cd2455664d78523f127101bed66516, scripts/build-context-pack.py emits exactly that template and requires the operator to supply a completed preflight record. The abbreviated chat startup instruction omitted this step. This was an operational handoff defect, not a failed design review.

## Change

Added scripts/prepare-review-run.py for existing independent-design packs. It checks manifest files, prepares a PREPARED record and a startup instruction in a separate output directory, and never edits pack inputs. Unknown runtime/isolation metadata is not fabricated. The operator can explicitly permit a design-only exploratory run with unverified isolation; default preparation alone does not authorize it. No gate is approved and known input/context failures remain blocking. README is now English and includes the missing setup step. TASK prompts and the exporter are unchanged.

## Executed validation

Command: `python3 -m unittest discover -s tests -p 'test_prepare_review_run.py' -v` (equivalent local discovery contained only the newly added regression module).

Result: **15/15 PASS**, Python 3.13.5, Linux. Raw output: [test-output.txt](test-output.txt).

Coverage includes v0.1-shaped pack compatibility, exact manifest hash, absolute output_root, untouched inputs, no invented model/isolation observations, no implicit waiver, missing/tampered/unlisted inputs, symlinks/control directories, unsafe paths and duplicate entries, overlapping/existing output paths, rejection of other stages/source snapshots, and actual CLI invocation without model execution. Uploaded helper/test Git blob IDs match the exact local files tested.

Tested SHA-256:

- scripts/prepare-review-run.py: `bce93746d70d6ef3018f40c8e9ca2216bc301c77340625eb02290af3e6871be1`
- tests/test_prepare_review_run.py: `ebe5b4956c822b2a9fea81b01116466ea0a0602d893c917aaa099ef20dbb9906`

## Limitations

These are local fixture/CLI tests, not an execution in Damian's review environment. His actual local pack, filesystem paths and session were not accessible here. The original exporter test module was not rerun in this fix; its prior 8-test result remains separately recorded. No Windows/macOS execution or Python 3.10 execution was performed. Direct Git clone again failed DNS resolution; GitHub connector reads/writes succeeded. No Bun build, model review, quota consumption, paid API call or migration was performed. The helper does not establish a sandbox, authenticate a manifest against malicious replacement, or prove context isolation. Preparation must not be reported as a completed independent-design result.
