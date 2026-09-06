# Project Kickoff 0.3.0 release checks

**Team:** TEAM-001  
**Owner:** approved-hooks / Complex Developer  
**Source commit:** `6236676060c52bbd66576b2696daaca9f20b95a0`  
**Checked:** 2026-09-06

## Integrated revision

- `git diff --name-status 37e2943..6236676060c52bbd66576b2696daaca9f20b95a0` reports only `A docs/hook-guard-review.md`.
- The runtime-path diff from reviewed revision `37e2943` to the source commit is empty.
- The integration worktree remained clean. `git status --short --ignored` returned no entries after verification.

## Test result

The required integrated suite ran once from the integration worktree:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
Ran 36 tests in 3.268s
OK
```

Native Codex and Claude Code host sessions were not run. The suite exercises the documented hook entry points with subprocess fixtures; it does not certify host behavior beyond those payloads and sample configurations.

## Archive result

The archive was built with `git archive` from the exact source commit, with prefix `project-kickoff/` and the 31 explicit runtime paths in the README install allowlist.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `dist/project-kickoff-0.3.0.zip` | 83,567 | `8307019df6c77b55404d8c40a0f3288cc0ad10adab0615183512be0e754d385a` |
| `dist/v0.3.0/SHA256SUMS` | 92 | `e16a85368c4646d11dbb485c70bdc498f9bfdf080bd5ba71e5c68fa31baab1c0` |

The checksum file contains:

```text
8307019df6c77b55404d8c40a0f3288cc0ad10adab0615183512be0e754d385a  project-kickoff-0.3.0.zip
```

The prior archives were preserved byte for byte:

- 0.1.0: `eac29b031619b279fd6165d7f3480e79e84e4af5d00499d7cccfc0f2b6707d4c`
- 0.2.0: `a61331eafeaebe0ac6b02df92de3a93df1550c3ee25ac8f02d8a480d608f602b`

## Extracted-package checks

A disposable extraction passed these checks and was then removed:

- Exactly 31 regular files matched the explicit allowlist.
- All 31 extracted files were byte-identical to the source commit.
- Both README install lists were identical and contained 31 unique paths.
- The system skill validator reported `Skill is valid!`.
- All 34 local links in `README.md`, `SKILL.md`, and `references/*.md` resolved inside the package.
- Both hook sample files parsed as JSON.
- Skill, README, changelog, archive, and release-tag text consistently used version 0.3.0.
- `docs/`, `tests/`, `.git`, `.agent-team`, `.project-kickoff`, and root `CONTEXT.md` were absent.

The two README Mermaid source blocks are byte-identical to the previously rendered blocks. Their hashes remain:

- `904ef580845a09ca1a4fe028324072412548c36b4da6162c9d92d6284831b0aa`
- `7473fa8b14f7d400676f213326b07247e2d9674392b106aef6da6eb65fa07352`

No renderer was installed or run for unchanged diagrams. No hook or host setting was activated.

## Published release verification

The project orchestrator published
[v0.3.0](https://github.com/thebpandey/project-kickoff/releases/tag/v0.3.0)
to the authorized private repository on 2026-09-06. GitHub reports both assets
as uploaded and the release as published, not a draft. The repository is private
and its default branch is main.

GitHub's ZIP and checksum-file digests equal the two local hashes above.
Remote main and the peeled release tag matched the exact source commit at
publication. Later maintainer evidence commits do not change the tagged runtime.
Releases 0.1.0 and 0.2.0 remain unchanged.

## Cleanup evidence

The feature branch was verified as an ancestor of main. Its only ignored file
was its task-owned CONTEXT.md; that note was preserved in the canonical local
handoff directory. The clean feature worktree and integrated branch were removed
through normal Git operations. No force removal or reset was used.

The integration checkout had no untracked or ignored output after package
verification. It is used only to record this release evidence, then is eligible
for normal removal after the documentation commit reaches main. No task-owned
servers, ports, or services were created. Temporary test repositories and archive
extractions were removed. The final archives and checksums remain in canonical
dist/, outside the disposable worktrees. Local task, context, and lesson records
remain in the canonical checkout.

After the evidence commit reached main, the orchestrator verified that the
integration branch was an ancestor of main and its checkout was clean, including
ignored files. Normal Git worktree removal and branch deletion succeeded. The
empty .worktrees directory was removed. The final Git worktree inventory contains
only canonical main; cleanup is complete.
