# Preparing the first review run

The exporter creates immutable input files and a NOT_RUN template. It does not create a completed preflight record or an output directory. Passing TASK.md alone is therefore insufficient.

## Existing independent-design pack

From the operator's RustyBun checkout (not inside the blind review session):

```bash
python3 scripts/prepare-review-run.py --pack ../RustyBun-review-01 --out ../RustyBun-review-01-output --run-id phase0-independent-20260908-01 --allow-unverified-isolation
```

This works with the original v0.1 pack. It verifies all listed file hashes and sizes, rejects missing/unlisted files and symlinks, and refuses to overwrite any output directory. It neither edits the pack nor changes its manifest. Preserve the old process SHA: fixing setup must not silently switch the reviewed experiment inputs.

The output directory receives RUN-RECORD.json and START-REVIEW.txt. Supply only the pack, that output directory and the generated startup instruction to the reviewer. The actual run record and startup instruction are explicitly authorized administrative metadata, not additional design evidence. Do not attach this document, the main repository, the helper's source or the presentation journal to the independent designer.

## What PREPARED means

Required preflight identity and routing fields are supplied: run_id, role_id, stage, input_root, output_root, process_sha and input_manifest_sha256. It is not necessary or honest to fill future measurements or execution timestamps in advance. For a methodology-only pack, source_sha is null because no source snapshot was supplied. The reference SHA in the brief does not imply that code was read.

started_at and ended_at stay null until actual task execution. The agent may record observable model/client/settings and update the run record within output_root. Non-observable runtime fields stay unknown; unchecked isolation observations stay null. The preparation host's OS/Python version is recorded separately and is not the agent environment.

The original NOT_RUN template and MANIFEST.json remain unchanged. The generated PREPARED record, not the template, is the runtime metadata. COMPLETE can be recorded only after completing the role's task; no gate is approved by this helper.

## Isolation is a separate question

The helper cannot inspect another session's memory, global instructions, filesystem mounts or client tools. Consequently it always writes isolation_verified=false.

Without --allow-unverified-isolation it prepares metadata with preflight BLOCKED_ENVIRONMENT and does not authorize execution. The flag is an explicit operator choice to permit only an exploratory independent-design task while checks remain unverified. It is not permission to certify the run as blind/independent, to skip missing inputs, or to execute later stages. The report must display EXPLORATORY; INDEPENDENCE UNVERIFIED. For a verified run, the operator must actually check the isolation conditions and record supporting observations; do not just flip a boolean.

Known exposure to excluded proposals, history or extra project context still requires a fresh run. So do mismatched hashes, unavailable required inputs or an inaccessible output_root. Do not search the home directory or other repositories to establish isolation: that can itself expose excluded content. If the current session only stopped on preflight and received no excluded material, the operator may supply START-REVIEW.txt there; otherwise start afresh.

## Scope and environment

Only independent-design is supported. The helper does not run a model, start a Codex session, configure authentication, call an API, execute downloaded source, or create a sandbox. It does not authorize migration, purchases, Git pushes, or gate approvals. This permission is operational and design-only; other stage prerequisites remain unchanged.

Input/output paths must refer to the same locations visible to the agent. If a container uses different mount paths, the operator must update the record and startup instruction explicitly before invocation; hashes continue to describe the same inputs. Keep input files read-only and allow writes only to output_root. Do not mount the main checkout merely to make those paths accessible.

After the task, preserve the original input pack, manifest, startup instruction, record and report with output hashes. Audit local paths and logs before publishing. Preparation alone is not a review result or evidence that the runtime sandbox works.
