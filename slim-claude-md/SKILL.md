---
name: slim-claude-md
description: Apply context disclosure to a project's CLAUDE.md — audit the file, categorize content as always-useful vs situational, trim CLAUDE.md to the bare minimum, and extract situational knowledge into focused project-specific skills. Use when a CLAUDE.md is bloated or contains information only relevant to specific task types (frontend work, debugging, a specific subsystem), or when asked to "reduce CLAUDE.md", "apply context disclosure", "slim down project context", or "extract skills from CLAUDE.md".
---

# Context Disclosure for CLAUDE.md

## The Problem

Every line of CLAUDE.md loads into every context window, every time. Architecture diagrams, gotcha lists, subsystem details — all consumed whether or not the current task touches them. This wastes tokens and dilutes signal.

## Principle

**CLAUDE.md = universal invariants only.** Everything else lives in project skills, loaded only when relevant.

## Categorization Rules

### Keep in CLAUDE.md

Content that is true and useful regardless of what the user is working on:

- Project overview (2–3 sentences max)
- Run / build commands (`just`, `npm run`, etc.)
- Toolchain conventions (language version, package manager, linter, test runner)
- Design principles (KISS, YAGNI, FAIL FAST, etc.)
- A skill reference table listing available project skills and their triggers

### Extract to a Project Skill

Content only needed when working on a specific area:

| Content type | Example skill name |
| --- | --- |
| Agent/pipeline architecture, state flow | `<project>-architecture` |
| Framework-specific gotchas and bugs | `<project>-<framework>-gotchas` |
| Data model / schema / DSL details | `<project>-data-models` |
| Frontend stack, components, API contracts | `<project>-frontend` |
| Deployment / infrastructure | `<project>-infra` |
| Testing patterns and fixtures | `<project>-testing` |

## Process

### 1. Audit CLAUDE.md

Read the file. For each section ask: *"Would this matter if I were fixing a typo in a config file?"* If no — it's situational.

### 2. Group Situational Content into Themes

Cluster related situational items. Each theme becomes one skill. Aim for 3–6 skills; avoid micro-skills with fewer than 5 meaningful bullets.

### 3. Create Project Skills

Skills live in `.claude/skills/<skill-name>/skill.md` inside the project repo.

**Apply context disclosure inside each skill too:**

- `description` field: loaded into every context (triggering mechanism). Keep it under 3 sentences — just enough to trigger correctly, no more.
- Skill body: loaded only when invoked — put all detail here.
- If the body has sub-areas, split to `references/` files rather than inlining:

```
<skill-name>/
├── skill.md        ← core rules + links to sub-files
└── references/
    ├── patterns.md
    └── examples.md
```

### 4. Replace Extracted Sections with a Skill Table

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

CLAUDE.md: 142 lines → 31 lines (−78%)
Skills created: 3
  • my-project-architecture  (18 lines)
  • my-project-frontend       (24 lines)
  • my-project-testing        (14 lines)
```

Count lines with `wc -l` before starting (record as "before") and after writing the trimmed CLAUDE.md (record as "after"). Calculate: `reduction = round((before - after) / before * 100)`.
