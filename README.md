# claude-skills

Reusable Claude Code skills for AI coding agents.

## Available Skills

| Skill | Description |
| ----- | ----------- |
| `just-init` | Bootstraps a justfile for the current project based on its build system (uv, npm, bun, yarn, pnpm, Maven, Gradle, Cargo, Go, Elixir Mix, .NET, PHP Composer, Makefile), then updates CLAUDE.md to replace raw command docs with a just --list reference. Use when the user runs /just-init, says 'create a justfile', 'set up just for this project', or 'bootstrap just'. |
| `slim-claude-md` | Apply context disclosure to a project's CLAUDE.md — audit the file, categorize content as always-useful vs situational, trim CLAUDE.md to the bare minimum, and extract situational knowledge into focused project-specific skills. Use when a CLAUDE.md is bloated or contains information only relevant to specific task types (frontend work, debugging, a specific subsystem), or when asked to "reduce CLAUDE.md", "apply context disclosure", "slim down project context", or "extract skills from CLAUDE.md". |

## Install

```bash
# Install all skills
npx skills add MehrCurry/claude-skills

# Install a single skill
npx skills add MehrCurry/claude-skills --skill slim-claude-md
npx skills add MehrCurry/claude-skills --skill just-init
```

## Usage

After installation, invoke a skill in Claude Code:

```
/slim-claude-md
/just-init
```

## About

Skills extend Claude Code agents with reusable, focused workflows. Each skill lives in its own directory with a `SKILL.md` file that Claude loads on demand.

Built with [skills.sh](https://skills.sh).
