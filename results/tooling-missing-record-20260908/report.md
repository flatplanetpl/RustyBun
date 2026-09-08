# Missing run record diagnostic — 2026-09-08

## Reported failure

The operator ran `python3 scripts/prepare-review-run.py --show-handoff ../RustyBun-review-01-output` and received `ERROR: Missing or non-regular input: RUN-RECORD.json`.

The error does not prove that preparation never happened: the directory could be wrong, absent, incomplete, or contain a non-regular entry. In process commit `1c1dc06128bf3df2b290569fdfa9bc687e9ff20f`, `show_handoff` only reads a prepared run; it cannot create a record. The earlier chat answer led with redisplay rather than the full preparation command.

## Fix

For a missing record, show the absolute expected path, explain that redisplay does not prepare a run, suggest checking the output path, and display the preparation command syntax. Never silently create a run, infer authorization, overwrite outputs or copy the NOT_RUN template as an actual record. Symlink/non-regular-entry errors remain distinct. Successful preparation already prints the complete reviewer prompt; no second redisplay command is needed.

The code change only affects the missing-record diagnostic. TASK, brief, startup_instruction, input hashes, authorization and stage gates are unchanged.

## Operator recovery (Bash, from the RustyBun checkout)

For a new preparation using the existing input pack, choose a new output path rather than overwriting the previous one:

```bash
RUN_ID="phase0-independent-$(date -u +%Y%m%dT%H%M%SZ)"
python3 scripts/prepare-review-run.py --pack ../RustyBun-review-01 --out "../${RUN_ID}-output" --run-id "$RUN_ID" --allow-unverified-isolation
```

This flag explicitly permits only an exploratory design task while independence remains unverified. It does not establish isolation. If a valid run already exists elsewhere, use its actual output directory for redisplay instead. Preserve any existing results.

## Executed checks

Reproduced the old diagnostic with the exact previous helper (Git blob `b72b6883c2031cbb7a6ae74bd8100f0e560e2031`). Ran `python3 -m unittest discover -s tests -p 'test_missing_handoff.py' -v`: **8/8 PASS**, Python 3.13.5 on Linux. Raw output is in [test-output.txt](test-output.txt).

Coverage: absent/empty output directories; preservation of partial results; accidental input-pack path; dangling record symlink; a directory named RUN-RECORD.json; successful create/redisplay with exact prompt equality; and continued blocking without authorization.

Tested SHA-256:

- `scripts/prepare-review-run.py`: `2a7e53fffb8f1da7edb60bf3c4f26a244e13093d1736eedb2f3fe2e6bb6a81aa`
- `tests/test_missing_handoff.py`: `a657095fae08b7164be871457fe301c2fe06b4d23994cd946e7db73c40ed052b`

## Limits

Only the new eight-test regression module was run for this fix, not the entire repository suite. These are local fixtures, not an inspection of the operator's machine. No model, migration, Bun build or paid API was invoked. No Windows/macOS validation. Public raw downloads failed DNS in the preparation environment; the GitHub connector was used for repository reads and writes.
