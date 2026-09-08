# Independent review command: validation — 2026-09-08

## Scope and reason

The operator reported an independent designer stopping on visible unrelated project instructions/memory. The saved blocking artifacts were not available to inspect. The exact injection source is unknown. The proposed remedy is fresh per-run client state, not an instruction to ignore known contamination. The operator also requested one documented command instead of composing Git, run IDs and output paths manually.

Added `scripts/independent-review.py` as a convenience wrapper around the unchanged preflight helper. Updated the English README, START-HERE and presentation journal, and added the rationale/usage document. Existing review TASK/brief, helper, exporter, input allowlists and approval gates were not changed. This launcher is not a multi-agent migration runner.

## Executed checks

`python3 -m unittest discover -s tests -p 'test_independent_review.py' -v`: **20/20 PASS**. Raw output: [test-output.txt](test-output.txt).

Environment: Python 3.13.5, Linux. Syntax compilation of the new launcher and test module passed. TOML parsing was checked using the local Python parser.

The tests exercise automatic unique identifiers, unchanged pinned inputs, no output overwrite, tampered/missing input rejection, outside-checkout paths, environment allowlisting, no implicit isolation waiver, optional model/config encoding, simulated version/login/client sequence, private-profile cleanup, failed login, changed inputs during login, no reuse of used runs, preservation of reviewer task status, CLI preparation, interactive-launch prerequisites, and clean-checkout/ff-only/re-exec behavior.

Codex subprocesses in these tests were **simulated**, not actual Codex sessions. The helper used by the integration tests matches the existing upstream Git blob listed below; it was not replaced by a stub.

A separate end-to-end probe created a local Git source, bare remote and checkout. An upstream commit was added, then the real launcher was invoked with `--update` and preparation-only flags. The local fast-forward completed, the updated launcher re-executed, exactly one output run was created, the complete handoff was printed, and the input pack retained its original process SHA. No remote network, login or model was used. [Probe receipt](git-integration.txt).

## Tested file hashes

- `scripts/independent-review.py`: SHA-256 `e736c6f10da55d7b7d17a27d73c3778de0297b931ef6d53dcb2b43df3d3dc668`; Git blob `dfdbfe66344476e9c09a99710dbe7a32d7b559df`.
- `tests/test_independent_review.py`: SHA-256 `a1c3ffc973815a74b5743dc2faf0d55ec594275fc81b5eb0da532105df68bade`; Git blob `0a10994056bf6c0b2265ef31da9f1839e6ce0933`.
- `scripts/prepare-review-run.py`: SHA-256 `2a7e53fffb8f1da7edb60bf3c4f26a244e13093d1736eedb2f3fe2e6bb6a81aa`; Git blob `9f4700ae0b8d49da7cff0747894c3d55be7dd2d7`.

## Limits and follow-up

The full existing repository test suite was not rerun; these are the 20 new launcher tests plus the separate local Git probe. No real Codex binary/config enforcement, ChatGPT device login, model selection, token/quota usage, network sandbox, system-instruction discovery, Windows/macOS behavior or Python 3.10 runtime was validated. The tool does not create a container or prevent every outside-file read. `isolation_verified` remains false; no gate or review result was approved.

Direct public GitHub/raw access failed DNS in this environment; repository reads/writes used the GitHub connector. The preparation helper and prior journal were reconstructed from connector reads and checked against their exact existing Git blob hashes before reuse/append. This report does not imply access to the operator's server.

Official Codex documentation was checked for the configuration/authentication flags; references and residual risks are in [the command guide](../../docs/independent-review-command.md). The next validation is an actual operator-run attempt, retaining the failed attempt rather than changing its status. Login/model failures must not trigger a less isolated profile, a paid API fallback or an invented COMPLETE result.
