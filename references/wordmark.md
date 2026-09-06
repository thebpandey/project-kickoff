# Project Kickoff wordmark

When Project Kickoff handles an explicit invocation or is selected implicitly
for a genuine kickoff action, show this filled-block wordmark once before the
first result or question:

```text
██████   ██████     ████   ████████ ████████   ██████ ████████
██    ██ ██    ██ ██    ██     ██   ██       ██         ████
██████   ██████   ██    ██     ██   ██████   ██         ████
██       ██  ██   ██    ██     ██   ██       ██         ████
██       ██    ██ ██    ██ ██  ██   ██       ██         ████
██       ██    ██   ████     ██     ████████   ██████   ████

██    ██ ████████   ██████ ██    ██   ████   ████████ ████████
██  ██     ████   ██       ██  ██   ██    ██ ██       ██
████       ████   ██       ████     ██    ██ ██████   ██████
████       ████   ██       ████     ██    ██ ██       ██
██  ██     ████   ██       ██  ██   ██    ██ ██       ██
██    ██ ████████   ██████ ██    ██   ████   ██       ██
```

Immediately below the code fence, show `Project Kickoff v<version>` using
`metadata.version` from the loaded `SKILL.md`. On the next line show:

Created by thebpandey.

Show the same block at the completed workflow final report. Do not show it for
each interview answer, progress update, hook result, or quoted mention. When a
short read-only invocation and its result share one reply, show it only once.
If the output surface cannot display the Unicode full-block character, replace
each block with `#` and preserve the spacing. No font, image, or dependency is
needed. The wordmark has no hook behavior and authorizes no action.
