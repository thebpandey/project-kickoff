# Release package checks

Checked: 2026-09-06

This report records a disposable archive check before the final documentation
commit. The checked runtime source is integration revision
`6a2fc9f095cad828e3ea062bc3907eab9262e53e`. The final documentation commit does
not change any runtime package file.

## Checked package

The candidate ZIP was created with `git archive`, prefix `project-kickoff/`, and
an explicit allowlist. The allowlist contains these 23 files:

- `SKILL.md`, `README.md`, `CHANGELOG.md`, and `LICENSE`;
- `agents/openai.yaml`;
- all seven Markdown references in `references/`;
- all eleven Markdown templates in `assets/templates/`.

The check extracted the ZIP to a new temporary directory. It did not install the
Skill, publish a release, create a tag, or contact the remote repository.

## Results

| Check | Actual result |
| --- | --- |
| ZIP integrity | Passed with `unzip -t`. |
| Contents | Exactly 23 allowed files under `project-kickoff/`; no other files. |
| Source identity | Every archived file was byte-for-byte equal to the same path at the checked revision. |
| Skill metadata | Name `project-kickoff`; version `0.1.0`. |
| Host metadata | Display name `Project Kickoff`; default prompt names `$project-kickoff`; implicit invocation is enabled. |
| Release names | README names version `0.1.0`, tag `v0.1.0`, and archive `project-kickoff-0.1.0.zip`; CHANGELOG contains release `0.1.0`. |
| Local links | All 37 local links resolved. Template output links resolved against the corresponding generated sibling template. |
| Mermaid source | Both block hashes match the rendered blocks in `docs/diagram-checks.md`: `904ef580845a09ca1a4fe028324072412548c36b4da6162c9d92d6284831b0aa` and `7473fa8b14f7d400676f213326b07247e2d9674392b106aef6da6eb65fa07352`. |

The candidate ZIP SHA-256 was
`c0e9305f7d12e6aaa2eecc7481c7929af787a6c07b7666b6b6dc34926c6db06e`.
This hash identifies the disposable candidate from the checked revision. The
distributed ZIP is rebuilt from the final source commit. Its authoritative hash
is stored beside it in `SHA256SUMS` after that build.

## Limits

These checks validate package construction, metadata, references, and source
identity. Behavioral, CLI, diagram, and installation evidence is in the other
development reports. No Git tag, push, GitHub release, remote visibility check,
or remote asset check occurred here.
