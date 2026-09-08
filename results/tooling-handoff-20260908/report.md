# Reviewer handoff regression report — 2026-09-08

## Request and change

The operator requested that "what to give the reviewer" be part of the script rather than a separate chat instruction. At process commit 699d8adc30037bd09f09a87eb858ae3852cc3006, the helper wrote START-REVIEW.txt but printed only its path.

The helper now prints the complete handoff after preparation: input/output directories with intended permissions, the exact saved startup instruction between explicit copy/paste markers, and the expected report location. --show-handoff OUTPUT_DIR redisplays a still-unused PREPARED handoff read-only, after rechecking its pack and record. It does not refresh timestamps or authorize/restart a run. Used records, stale paths, changed inputs or inconsistent startup text are rejected.

The startup instruction itself is unchanged; its generation was extracted into a single function shared by writing and verification. Existing packs need not be exported again. TASK, brief, exporter and gates are untouched. Displaying permissions does not enforce them or create a sandbox.

## Executed validation

Python 3.13.5, Linux. In the local validation workspace containing the preflight module:

`python3 -m unittest discover -s tests -v`

**22/22 PASS:** the previous 15 preflight tests plus 7 handoff tests. Raw output: [test-output.txt](test-output.txt). Checks cover exact terminal/file instruction equality, directory permissions in the handoff, no output report fabricated, read-only redisplay, continued blocking without authorization, stale inputs/instruction/record rejection, used-run rejection, CLI validation and Unicode paths.

An additional local probe used the original helper from the previous turn (SHA-256 bce93746d70d6ef3018f40c8e9ca2216bc301c77340625eb02290af3e6871be1) to create a fixture run. The new helper displayed it successfully, without any input/output byte changing. [Probe receipt](legacy-compatibility.txt).

Tested file SHA-256 values:

- scripts/prepare-review-run.py: 32aa70774f6448dbf07d547fb92eee93618ae035eb9d46b359e1f2c1bbdc91e5
- tests/test_prepare_review_run.py: 5e402bfb0ae2c1fdebd0f749de9e2af5464dad9fe9d8a5655b6705376e559d9e

Uploaded Git blobs match the tested files: b72b6883c2031cbb7a6ae74bd8100f0e560e2031 and 1a5946354ca39ef789da0021c46ad53b93729f26, respectively.

## Limitations

This is fixture/CLI validation, not execution in Damian's environment. No model, Bun build, migration or paid API was invoked. No Windows/macOS runtime test was performed; Unicode paths were tested on Linux. The unchanged exporter suite was not rerun here. The first development run accidentally discovered the original test class twice; discovery was corrected before the final 22-test run. No duplicate tests are counted in the reported result. The helper does not prove isolation or authenticate operator metadata against malicious tampering. Read-only redisplay refuses records showing execution rather than pretending it can resume or restart safely.
