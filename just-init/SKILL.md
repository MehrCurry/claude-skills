---
name: just-init
description: Bootstraps a justfile for the current project based on its build system (uv, npm, bun, yarn, pnpm, Maven, Gradle, Cargo, Go, Elixir Mix, .NET, PHP Composer, Makefile), then updates CLAUDE.md to replace raw command docs with a just --list reference. Use when the user runs /just-init, says 'create a justfile', 'set up just for this project', or 'bootstrap just'.
---

# just-init

Generate a justfile for the current project and clean up command docs in CLAUDE.md.

## Workflow

### 1. Detect build systems

Glob for indicator files in the project root. Multiple may coexist (e.g. `pyproject.toml` +
`package.json` for a full-stack project). Read [references/build-systems.md](references/build-systems.md)
for the full detection table and recipe templates.

**Detect all build systems before generating any recipes.**

### 2. Read existing configs to tailor recipes

- `package.json` → read `scripts` section; only generate recipes for scripts that exist
- `pyproject.toml` → check `[project.scripts]` for entry points; check tool sections for ruff/mypy/pytest
- `pom.xml` → check for Spring Boot plugin to decide between `mvn exec:java` and `spring-boot:run`
- `build.gradle` → check for `application` or `org.springframework.boot` plugins
- `Makefile` → read targets to wrap

### 3. Check for existing justfile

- **No justfile**: create from scratch
- **Existing justfile**: read it, then extend with missing recipes only. Preserve all existing content and comments.

### 4. Write the justfile

Structure:
```
# <Project Name> — Justfile
# Install: brew install just

# Default recipe
default:
    @just --list

# --- <Build System> ---
<recipes>
```

- Always start with `default: @just --list`
- Group by build system with `# ---` section comments when multiple systems exist
- Use `@` prefix on echo/status-only lines to suppress echoing
- One blank line between recipes

### 5. Update CLAUDE.md

See "CLAUDE.md Update Rules" in [references/build-systems.md](references/build-systems.md).

Replace the entire `## Commands` section content with:

```markdown
## Commands

```bash
just          # list all available commands
just setup    # first-time setup
```
```

- If no `## Commands` section: add it after `## Project Overview`
- If no CLAUDE.md: create a minimal one with just the Commands section
- Never remove other sections (Architecture, Conventions, etc.)

### 6. Confirm

Print a results block:

```
## just-init results

Build systems detected: uv, npm
Justfile: created (12 recipes)
CLAUDE.md: 87 lines → 54 lines (−38%)
```

Count CLAUDE.md lines with `wc -l` before step 5 (record as "before") and after (record as "after"). Calculate: `reduction = round((before - after) / before * 100)`. If no CLAUDE.md existed before, show `0 lines → N lines (created)`.
