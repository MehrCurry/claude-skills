#!/usr/bin/env python3
"""Regenerate the Available Skills table in README.md from SKILL.md frontmatter.

Runs as a Claude Code Stop hook. Idempotent — only writes if content changes.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")

TABLE_PATTERN = re.compile(
    r"(## Available Skills\n\n)\|[^\n]+\n(?:\|[^\n]+\n)+",
    re.MULTILINE,
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    result = {}
    for line in text[3:end].strip().splitlines():
        key, sep, value = line.partition(":")
        if sep:
            result[key.strip()] = value.strip()
    return result


def find_skills() -> list[tuple[str, str]]:
    skills = []
    for entry in sorted(os.listdir(ROOT)):
        skill_md = os.path.join(ROOT, entry, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md) as f:
                fm = parse_frontmatter(f.read())
            if "name" in fm and "description" in fm:
                skills.append((fm["name"], fm["description"]))
    return skills


def build_table(skills: list[tuple[str, str]]) -> str:
    rows = ["| Skill | Description |", "| ----- | ----------- |"]
    for name, desc in skills:
        rows.append(f"| `{name}` | {desc} |")
    return "\n".join(rows) + "\n"


def update_readme(table: str) -> bool:
    with open(README) as f:
        content = f.read()

    new_content = TABLE_PATTERN.sub(rf"\g<1>{table}", content)
    if new_content == content:
        return False

    with open(README, "w") as f:
        f.write(new_content)
    return True


if __name__ == "__main__":
    # Consume stdin (Stop hook sends JSON) without blocking
    sys.stdin = open(os.devnull)

    skills = find_skills()
    if not skills:
        sys.exit(0)

    changed = update_readme(build_table(skills))
    if changed:
        print(f"README.md: skills table updated ({len(skills)} skills)")
