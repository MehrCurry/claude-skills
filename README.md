# claude-skills

Reusable Claude Code skills for AI coding agents.

## Available Skills

| Skill | Description |
|-------|-------------|
| [slim-claude-md](./slim-claude-md/SKILL.md) | Apply context disclosure to a project's CLAUDE.md — trim it to the bare minimum and extract situational knowledge into focused skills |
| [just-init](./just-init/SKILL.md) | Bootstrap a justfile for any project based on its build system, then update CLAUDE.md to use `just --list` |

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
