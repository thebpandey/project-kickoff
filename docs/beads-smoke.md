# Beads 1.1.2 live CLI smoke

Executed 2026-09-06 in a new disposable Git repository. This tests the installed
CLI's capabilities; it is **not** an execution or behavioral validation of the
project-kickoff skill.

## Environment and isolation

- Selected executable: `/home/server/.local/bin/bd`.
- `bd version`: `1.1.2 (20e493e56: HEAD@20e493e569c9)`.
- Version output also reported `/usr/local/bin/bd`; that binary was not tested.
- Fixture: `/tmp/project-kickoff-beads-30n26760`, created with Python's
  `tempfile.mkdtemp`, initialized with `git init`, and given only synthetic data.
- The real skill repository and its worktrees were not initialized with Beads.
- No packages were installed, Git remote configured, Dolt remote configured,
  publication performed, or user data supplied.
- Commands used `--sandbox`, whose actual help promises to disable Dolt
  auto-push. This flag does **not** establish network isolation; see the telemetry
  observation below. No explicit remote mutation command was run.

Fixture Git identity was `Fixture Tester <fixture@example.invalid>`. Its first
commit contained an approved dummy `PLAN.md` plus existing `AGENTS.md` and
`CLAUDE.md`, each containing a preservation sentinel.

| Plan ID | Type | Title | Parent | Depends on |
|---|---|---|---|---|
| EP-001 | epic | Local input summary | — | — |
| PK-001 | task | Inspect local input | EP-001 | — |
| PK-002 | task | Produce summary | EP-001 | PK-001 |

## Help checked and initialization

The runner inspected `bd init --help`, `bd create --help`, `bd dep --help`,
and `bd list --help` before using their options. The following command ran with
the fixture as its working directory and exited 0:

```sh
/home/server/.local/bin/bd --sandbox init \
  --non-interactive --skip-agents --skip-hooks --prefix pksmoke
```

Actual help describes `--skip-agents` as skipping AGENTS.md and Claude/Codex
setup generation, and `--skip-hooks` as skipping Git hooks installation.
Initialization reported backend `dolt`, mode `embedded`, database `pksmoke`.
No external database server was needed. It also automatically created fixture
Git commit `e10b7cc` (`bd init: initialize beads issue tracking`), after the
initial synthetic-data commit `5e93a21`.

Initialization warned that no Dolt remote was configured and that
`.beads/issues.jsonl` is an export rather than the source of truth or
cross-machine synchronization. No remote was added in response.

Python assertions after the smoke confirmed both instruction files were
byte-for-byte unchanged and `.git/hooks` contained no active hooks, only Git's
sample files. No `--stealth`, `--force`, or destructive reinitialization options
were used.

## Creation and actual mapping

Each row carried its stable plan ID in its title, exact `external_ref`, and
`metadata.plan_id`. Commands below show the actual arguments and returned IDs;
every command exited 0. All commands ran inside the fixture.

```sh
/home/server/.local/bin/bd --sandbox create '[EP-001] Local input summary' \
  --type epic --external-ref 'PLAN.md#EP-001' \
  --metadata '{"plan_id":"EP-001"}' \
  --description 'Synthetic approved PLAN.md epic.' --json

/home/server/.local/bin/bd --sandbox create '[PK-001] Inspect local input' \
  --type task --external-ref 'PLAN.md#PK-001' \
  --metadata '{"plan_id":"PK-001"}' \
  --description 'Synthetic approved PLAN.md row PK-001.' \
  --json --parent pksmoke-g70

/home/server/.local/bin/bd --sandbox create '[PK-002] Produce summary' \
  --type task --external-ref 'PLAN.md#PK-002' \
  --metadata '{"plan_id":"PK-002"}' \
  --description 'Synthetic approved PLAN.md row PK-002.' \
  --json --parent pksmoke-g70

/home/server/.local/bin/bd --sandbox dep add pksmoke-g70.2 pksmoke-g70.1 --json
```

| Plan ID | Actual Beads ID |
|---|---|
| EP-001 | pksmoke-g70 |
| PK-001 | pksmoke-g70.1 |
| PK-002 | pksmoke-g70.2 |

The runner wrote exactly these three rows to fixture `TASK-MAP.md` after
reconciliation. Beads assigned its IDs; stable plan IDs were not substituted
for Beads IDs.

The dependency command returned:

```json
{"depends_on_id":"pksmoke-g70.1","issue_id":"pksmoke-g70.2","schema_version":1,"status":"added","type":"blocks"}
```

Actual dependency help confirms the direction: `bd dep add <blocked> <blocker>`.
`bd show <id> --json` showed exactly one `parent-child` relation from each task
to `pksmoke-g70`, and exactly one `blocks` dependency from PK-002 to PK-001.
PK-001 had no `blocks` dependencies. `bd list --all --limit 0 --parent
pksmoke-g70 --json` returned exactly the two child tasks.

`bd ready --json` included PK-001 and excluded PK-002, confirming that the
blocking edge affected readiness in the intended direction. The open epic was
also returned; callers should distinguish task and epic records.

## Partial creation and repeated reconciliation

The epic was deliberately created before any local mapping existed. A Python
runner then read `bd --sandbox list --all --limit 0 --json` and reconciled each
plan row using exact equality on either `metadata.plan_id` or `external_ref`.
It asserted at most one matching record per plan ID, reused a matching record,
and created only missing records. Ambiguous multiple matches would fail the
fixture rather than choose one silently.

| Pass | Starting state | Created | Final count |
|---|---|---|---:|
| 1 | Epic exists; mapping absent | PK-001, PK-002 | 3 |
| 2 | All three records exist | None | 3 |

Both passes produced the identical mapping above. The second pass did not
re-add the dependency; subsequent reads and assertions verified the existing
parent and blocking relations and their exact counts. This demonstrates
resume-by-reconciliation, not that unconditional `bd create` is idempotent.

For recovery after interrupted creation, query all records including closed
ones with no result limit, recover IDs from the stable fields, and inspect
the parent and dependency relations before adding anything missing. A missing
mapping file alone is not evidence that Beads records need creation. This
smoke exercised the missing-map/existing-epic case and a complete repeated
pass; it did not inject every possible interruption or concurrent writer.

## Cleanup and limitations

The process audit found PID `719241`, with the fixture as its working
directory and command `/home/server/.local/bin/bd send-metrics`. Follow-up
`bd send-metrics --help` identifies it as an internal process that flushes
queued telemetry events. The process had already exited before a verified
termination could be sent; no signal was sent to an unrelated PID.

No packet capture or egress denial was active, so this smoke cannot establish
whether the telemetry process transmitted anything. Future strictly offline
fixtures need explicit egress isolation or a verified telemetry-disable
setting before running the CLI. `--sandbox` alone is insufficient evidence.

A second `/proc` audit, checking fixture working directories and command-line
references, found no remaining task-owned processes. The runner then removed
the exact disposable fixture directory and its temporary pointer file and
confirmed the fixture no longer existed. Raw fixture logs and the embedded
database were removed with it; the commands, IDs, assertions, and observations
above preserve the relevant evidence. No shared database daemon was stopped.

The local CLI smoke passed initialization, safe instruction-file handling,
hook avoidance, creation, hierarchy, dependency direction, readiness, mapping,
and duplicate-free reconciliation. It does not establish skill behavior,
installation behavior, network isolation, remote durability, deployment,
concurrent reconciliation safety, or compatibility with other Beads versions.
