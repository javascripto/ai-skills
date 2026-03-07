---
name: web-design-guidelines
description: Review web interface files for compliance with the latest Web Interface Guidelines. Use when the user asks for UI/design standards checks, frontend guideline audits, or rule-based review of HTML/CSS/JSX/TSX files.
---

# Web Design Guidelines

## Overview

Run a deterministic UI-guideline review flow over user-specified files.
Always fetch the latest guideline rules before each review, then report only concrete findings.

## Guidelines Source

Fetch fresh rules from:

```text
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Do not reuse stale copies across reviews. Fetch this URL every time.

## Reference Origin

This skill is based on:

- https://skills.sh/vercel-labs/agent-skills/web-design-guidelines
- https://github.com/vercel-labs/agent-skills/tree/main/web-design-guidelines

## Review Workflow

1. Fetch the latest guidelines from the source URL.
2. Resolve target files from the user's path/pattern input.
3. Read only the relevant files.
4. Apply all fetched rules to each file.
5. Output findings in the format required by the fetched guidelines.

If the user does not provide files or patterns, ask which files should be reviewed.

## Output Requirements

- Keep output terse and actionable.
- Include exact file references and line numbers.
- Prefer `file:line` style for each finding unless the fetched guidelines demand a stricter variant.
- Skip praise or generic summaries unless the user explicitly asks for them.

## Execution Notes

- Use non-interactive commands and deterministic steps.
- Treat fetched guideline content as the source of truth for rule details and final output format.
- When the fetched guidelines and local assumptions conflict, follow the fetched guidelines.

## Typical Trigger Phrases

- "Review these TSX files against web design rules"
- "Run a guideline audit on this frontend folder"
- "Check if this UI complies with the web interface guidelines"
