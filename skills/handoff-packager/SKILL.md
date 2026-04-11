---
name: handoff-packager
description: Condense a conversation into a compact handoff for the next chat. Use when ending a thread, resetting context, or preparing a markdown starter with titles, summary, decisions, open items, files, and prompt history.
---

# Handoff Packager

## Purpose

Turn the current conversation into a short handoff that makes the next chat easy to resume with less context.

## When To Use

- The user wants to reset context or start a new conversation.
- The user asks for a summary, continuity note, or project handoff.
- The user wants the current chat title and a suggested next-chat title.
- The user wants a copyable markdown block with the important state.

## Output Rules

- Keep everything outside the markdown blocks very short.
- Outside the blocks, provide only:
  - `Título da conversa atual`
  - `Título da próxima conversa`
  - 1 brief line telling the user the file was saved and to copy the short block into the new chat
- Conversation titles must include a sequential number prefix, e.g. `#1 — Setup do projeto`, `#2 — Autenticação`, `#3 — Deploy`. Infer the current number from the existing title if it already has one; otherwise start at `#1`. The next conversation title always increments by 1.
- The copied content must be only markdown.
- Do not repeat the outside instructions inside any copied markdown.
- If the conversation is in interactive mode and the thread is getting long, ask the user whether they want to generate the handoff now and start a fresh chat from it.
- Prefer splitting work into smaller chats by part, topic, domain, or limit when that helps keep context smaller.
- Use relative paths in markdown by default when the next chat will continue in the same project/workspace.
- Use absolute paths only when the handoff is meant for a different project, a different workspace, or a context where relative paths would not resolve.

## File Output

Save the full handoff markdown to `handoff/<filename>.md` in the current project directory. Choose a filename that is descriptive and date-prefixed, e.g. `handoff/2025-04-11-feature-auth.md`. Create the `handoff/` directory if it does not exist.

## Two-Block Output

After saving the file, produce two separate markdown blocks:

**Block 1 — Full handoff** (for reference and verification): the complete handoff content as defined in `Markdown Block Shape`. This is what gets saved to disk and what the user can inspect.

**Block 2 — Short reference block** (the one to copy into the next chat): a compact snippet that only contains:
- a pointer to the saved file so the next agent reads it for full context
- a short `## Next Steps` section with the first 2–4 concrete actions
- any single critical constraint worth repeating inline

The short block should be under 15 lines. Its purpose is to reduce what the user pastes — the next agent reads the file for everything else.

## What To Capture

Include only high-signal items:

- goal of the thread
- what was already done
- where the work stopped
- what remains to do
- key decisions and constraints
- important file paths, screenshots, or links
- user preferences and standing rules
- condensed user prompts when they matter for continuity

## Markdown Block Shape

Use a compact structure like this:

```markdown
# Handoff

## Context
...

## Start Point
...

## Done
...

## Open
...

## Files
...

## Rules
...

## Next
...

## Next Steps
...

## Split Rule
...

## Prompt Log
...
```

## Short Reference Block Shape

```markdown
# Handoff

> Full context: `handoff/2025-04-11-feature-auth.md`

## Next Steps
- [ ] ...
- [ ] ...

## Key Constraint
...
```

## Writing Guidance

- Prefer bullets over paragraphs.
- Compress repeated ideas into one line.
- Preserve relative links when possible.
- Mention concrete file paths when they help the next agent resume quickly.
- Keep the handoff factual; avoid extra commentary.
- Add a short "start point" note that tells the next agent exactly where to continue.
- Add a short "next steps" note that turns the remaining work into the first actions for the next chat.
- Keep the split rule brief and explicit so the next agent knows when to propose a new chat.
- For same-project continuations, prefer repository-relative links like `./docs/...` and `./app-base/...`.
- For cross-project or external handoffs, use absolute paths only when necessary for clarity.

## Chat Split Behavior

- When the thread is approaching its context limit, prompt the user to:
  - generate a handoff markdown
  - start a new chat from that handoff
  - split the work by topic, domain, or stage
- Make the suggestion short and practical.
- Do not rehash the whole handoff in plain text; put the useful state in the markdown block.
