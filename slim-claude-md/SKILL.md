---
name: slim-claude-md
description: Apply context disclosure to a CLAUDE.md — audit the file, categorize content as always-useful vs situational, trim CLAUDE.md to the bare minimum, and extract situational knowledge into focused skills. Works at **project level** (default) or **user level** (`~/.claude/CLAUDE.md` → `~/.claude/skills/`). Use when a CLAUDE.md is bloated, or when asked to "reduce CLAUDE.md", "apply context disclosure", "slim down project context", "slim my global CLAUDE.md", "slim user CLAUDE.md", or "extract skills from CLAUDE.md".
---

# Context Disclosure for CLAUDE.md

## The Problem

Every line of CLAUDE.md loads into every context window, every time. Architecture diagrams, gotcha lists, subsystem details — all consumed whether or not the current task touches them. This wastes tokens and dilutes signal.

## Operating Modes

| Mode | Target CLAUDE.md | Skills output |
|------|-----------------|---------------|
| **Project** (default) | `<project-root>/CLAUDE.md` | `.claude/skills/<name>/SKILL.md` |
| **User** | `~/.claude/CLAUDE.md` | `~/.claude/skills/<name>/SKILL.md` |

**Detect mode from user intent:**
- "slim my global CLAUDE.md" / "slim user-level" / "slim ~/.claude/CLAUDE.md" → User mode
- No explicit qualifier → Project mode (default)
- When ambiguous, ask before proceeding.

## Principle

**CLAUDE.md = universal invariants only.** Everything else lives in skills, loaded only when relevant.

## Categorization Rules

### Project-Level CLAUDE.md — Keep vs Extract

Content that is true and useful regardless of what the user is working on:

**Keep in CLAUDE.md:**
- Project overview (2–3 sentences max)
- Run / build commands (`just`, `npm run`, etc.)
- Toolchain conventions (language version, package manager, linter, test runner)
- Design principles (KISS, YAGNI, FAIL FAST, etc.)
- A skill reference table listing available project skills and their triggers

**Extract to `.claude/skills/<name>/SKILL.md`:**

| Content type | Example skill name |
| --- | --- |
| Agent/pipeline architecture, state flow | `<project>-architecture` |
| Framework-specific gotchas and bugs | `<project>-<framework>-gotchas` |
| Data model / schema / DSL details | `<project>-data-models` |
| Frontend stack, components, API contracts | `<project>-frontend` |
| Deployment / infrastructure | `<project>-infra` |
| Testing patterns and fixtures | `<project>-testing` |

### User-Level CLAUDE.md — Keep vs Extract

User CLAUDE.md holds cross-project conventions. The bar for "keep" is higher: content must be useful on *every* project, every task.

**Keep in `~/.claude/CLAUDE.md`:**
- Tool/package manager preferences (uv, glab, etc.)
- LLM endpoint & default models
- Core engineering principles (3–5 bullet summary)
- Skill and agent reference table

**Extract to `~/.claude/skills/<name>/SKILL.md`:**

| Content type | Example skill name |
|---|---|
| Research/Perplexity protocol | `perplexity-protocol` |
| Sub-agent delegation rules | `delegation-rules` |
| Bug-fixing workflow | `bug-fixing-workflow` |
| Security / git / architecture standards | `engineering-standards` |
| Domain-specific patterns (DDD, Hexagonal) | `domain-patterns` |
| Communication & review guidelines | `communication-guidelines` |

## Process

### 1. Audit CLAUDE.md

Read the file. For each section apply the mode-appropriate test:

- **Project mode:** *"Would this matter if I were fixing a typo in a config file?"* If no — situational.
- **User mode:** *"Is this useful on literally every project, for every task type?"* If not universally true — situational. The bar is stricter because user CLAUDE.md loads for 100% of all sessions.

### 2. Group Situational Content into Themes

Cluster related situational items. Each theme becomes one skill. Aim for 3–6 skills; avoid micro-skills with fewer than 5 meaningful bullets.

### 3. Create Skills

**Project mode:** `.claude/skills/<skill-name>/SKILL.md`
**User mode:** `~/.claude/skills/<skill-name>/SKILL.md`

Both modes use `SKILL.md` (uppercase) — the standard filename for Claude Code skills.

**Apply context disclosure inside each skill too:**

- `description` field: loaded into every context (triggering mechanism). Keep it under 3 sentences — just enough to trigger correctly, no more.
- Skill body: loaded only when invoked — put all detail here.
- If the body has sub-areas, split to `references/` files rather than inlining:

```
<skill-name>/
├── SKILL.md        ← core rules + links to sub-files
└── references/
    ├── patterns.md
    └── examples.md
```

### 4. Run just-init (project mode only)

After extracting skills, invoke the `just-init` skill. It bootstraps a justfile from the project's build system and replaces raw command docs in CLAUDE.md with a `just --list` reference — directly reducing the lines that would otherwise stay in CLAUDE.md. Skip this step in user mode.

### 5. Replace Extracted Sections with a Skill Table

In CLAUDE.md, replace all extracted content with a single reference table:

```markdown
## Skills

| Skill | Trigger |
| --- | --- |
| `/my-project-architecture` | Agent pipeline, state flow, pipeline debugging |
| `/my-project-gotchas` | Framework-specific bugs and workarounds |
```

## Skill Description Formula

```
Load when [working on X / debugging Y / modifying Z].
Also load when [alternative trigger].
```

- Too vague: *"Contains project information."*
- Too long: A full paragraph listing every bullet.
- Good: *"Load when working on pricing YAML files, the calculator engine, or the pricing DSL tool."*

## Token Budget Check

After refactoring, verify:

- CLAUDE.md: < 50 lines
- Each skill description: < 3 sentences
- Each skill body: < 200 lines (split to `references/` if larger)
- No content duplicated between CLAUDE.md and skills

## Summary Output

After completing the refactor, print a results block:

```
## slim-claude-md results

Mode: project
CLAUDE.md: 142 lines → 31 lines (−78%)
Skills created: 3
  • my-project-architecture  (18 lines) → .claude/skills/
  • my-project-frontend       (24 lines) → .claude/skills/
  • my-project-testing        (14 lines) → .claude/skills/
```

For user mode:

```
## slim-claude-md results

Mode: user
~/.claude/CLAUDE.md: 145 lines → 28 lines (−81%)
Skills created: 4
  • delegation-rules          (32 lines) → ~/.claude/skills/
  • perplexity-protocol       (18 lines) → ~/.claude/skills/
  • bug-fixing-workflow       (22 lines) → ~/.claude/skills/
  • engineering-standards     (41 lines) → ~/.claude/skills/
```

Count lines with `wc -l` before starting (record as "before") and after writing the trimmed CLAUDE.md (record as "after"). Calculate: `reduction = round((before - after) / before * 100)`.
