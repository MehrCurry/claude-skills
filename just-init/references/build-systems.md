# Build System Detection & Recipe Templates

## Detection Signals

Check these files in project root (in priority order when multiple exist):

| File | Build System |
|------|-------------|
| `pyproject.toml` + `uv.lock` | **uv** (Python) |
| `pyproject.toml` | uv or pip (prefer uv unless pip-only) |
| `package.json` | **npm** / bun / yarn / pnpm — check `packageManager` field or lockfiles |
| `bun.lockb` / `bun.lock` | **bun** |
| `yarn.lock` | **yarn** |
| `pnpm-lock.yaml` | **pnpm** |
| `pom.xml` | **Maven** |
| `build.gradle` / `build.gradle.kts` | **Gradle** |
| `Cargo.toml` | **Cargo** (Rust) |
| `go.mod` | **Go** |
| `mix.exs` | **Elixir Mix** |
| `*.sln` / `*.csproj` | **.NET** (dotnet CLI) |
| `composer.json` | **PHP Composer** |
| `Makefile` | **Make** (wrap targets) |

Multiple build systems can coexist (e.g. `pyproject.toml` + `package.json` for a full-stack project). Generate recipes for all detected systems, grouped with comments.

---

## Recipe Templates by Build System

### uv (Python)

```just
# First-time setup
setup:
    uv sync
    @test -f .env || (cp .env.example .env && echo "Created .env — fill in required vars")

# Run tests
test:
    uv run pytest

# Run single test (usage: just test-one tests/test_foo.py::test_bar)
test-one test:
    uv run pytest {{test}} -v

# Lint
lint:
    uv run ruff check src/
    uv run ruff format --check src/

# Format
fmt:
    uv run ruff format src/

# Type check
typecheck:
    uv run mypy src/
```

Also check `pyproject.toml` for `[project.scripts]` to add a `run` recipe, and for tool configs (ruff, mypy, pytest) to confirm lint/test commands are valid.

---

### npm / bun / yarn / pnpm

Read `scripts` section from `package.json` and map to just recipes. Common mapping:

```just
# Install dependencies
setup:
    npm install          # or: bun install / yarn / pnpm install

# Start dev server
dev:
    npm run dev

# Build for production
build:
    npm run build

# Run tests
test:
    npm test

# Lint
lint:
    npm run lint

# Format
fmt:
    npm run format       # or: npm run fmt

# Clean build artifacts
clean:
    rm -rf dist .next out
```

Only generate recipes for scripts that actually exist in `package.json`. Skip if the script key is absent.

---

### Maven

```just
# Build (skip tests for speed)
build:
    mvn package -DskipTests

# Run tests
test:
    mvn test

# Full clean build
clean:
    mvn clean

# Run application (add if spring-boot-maven-plugin is in pom.xml)
run:
    mvn spring-boot:run

# Code quality checks
lint:
    mvn checkstyle:check
```

Check `pom.xml` for `<packaging>`, Spring Boot plugin, and module structure.

---

### Gradle

```just
# Build
build:
    ./gradlew build

# Run tests
test:
    ./gradlew test

# Clean
clean:
    ./gradlew clean

# Run application
run:
    ./gradlew run       # or: ./gradlew bootRun for Spring Boot

# All checks (lint + test)
check:
    ./gradlew check
```

Use `./gradlew` (not `gradle`) for wrapper portability. Check `build.gradle` for `application` or `org.springframework.boot` plugins.

---

### Cargo (Rust)

```just
# Build
build:
    cargo build

# Build release
build-release:
    cargo build --release

# Run tests
test:
    cargo test

# Lint (clippy)
lint:
    cargo clippy -- -D warnings

# Format
fmt:
    cargo fmt

# Run
run:
    cargo run

# Clean
clean:
    cargo clean
```

---

### Go

```just
# Build
build:
    go build ./...

# Run tests
test:
    go test ./...

# Lint (use golangci-lint if present, else go vet)
lint:
    go vet ./...

# Format
fmt:
    gofmt -w .

# Run
run:
    go run .

# Clean
clean:
    go clean ./...
```

Check if `golangci-lint` is in go.mod tools or `.golangci.yml` exists — if so, use `golangci-lint run` for lint.

---

### Elixir Mix

```just
# Install dependencies
setup:
    mix deps.get

# Run tests
test:
    mix test

# Compile
build:
    mix compile

# Start interactive shell
run:
    iex -S mix

# Start Phoenix server (if phoenix dep present)
dev:
    mix phx.server

# Format
fmt:
    mix format

# Lint (credo)
lint:
    mix credo
```

---

### .NET (dotnet)

```just
# Restore packages
setup:
    dotnet restore

# Build
build:
    dotnet build

# Run tests
test:
    dotnet test

# Run application
run:
    dotnet run

# Publish
publish:
    dotnet publish -c Release

# Clean
clean:
    dotnet clean
```

---

### PHP Composer

```just
# Install dependencies
setup:
    composer install

# Run tests
test:
    vendor/bin/phpunit     # or: php artisan test for Laravel

# Lint
lint:
    vendor/bin/phpcs

# Format
fmt:
    vendor/bin/phpcbf

# Start dev server (Laravel)
dev:
    php artisan serve
```

---

### Makefile (wrapping)

Read existing `Makefile` targets and wrap them:

```just
# Wrap existing Makefile targets
build:
    make build

test:
    make test

clean:
    make clean
```

Only wrap targets that actually exist. Show the Makefile contents to determine what to wrap.

---

## Standard Recipes (add to all projects)

These recipes belong in every justfile regardless of build system:

```just
# Default: list all recipes
default:
    @just --list
```

---

## CLAUDE.md Update Rules

1. **If a `## Commands` section exists**: Replace its entire content (the fenced code block and any surrounding text up to the next `##` heading) with:
   ```markdown
   ## Commands

   ```bash
   just          # list all available commands
   just setup    # first-time setup
   ```
   ```

2. **If no Commands section exists**: Add the above block after `## Project Overview` (or at the top after the title if no overview section exists).

3. **If no CLAUDE.md exists**: Create a minimal one with just the Commands section.

4. **Never remove** other sections (Architecture, Conventions, ADK Gotchas, etc.) — only replace the Commands block.
