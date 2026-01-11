# /// script
# dependencies = ["tomlkit"]
# ///

"""
Pins flet* dependencies in a TOML file to the installed flet version.

Usage:
    uv run pin_flet_deps.py <toml_file> <version>
"""


import os
import re
import sys
from pathlib import Path

import tomlkit


def pin_requirement(requirement: str, version: str) -> str:
    parts = requirement.split(";", 1)
    req_part = parts[0].strip()
    if not req_part.lower().startswith("flet"):
        return requirement

    match = re.match(r"^(flet[a-z0-9._-]*)(\[[^\]]+\])?", req_part, re.IGNORECASE)
    if not match:
        return requirement

    name = match.group(1)
    extras = match.group(2) or ""
    pinned = f"{name}{extras}=={version}"
    if len(parts) == 2:
        pinned = f"{pinned};{parts[1]}"
    return pinned


def pin_dependencies(deps: list[str], version: str) -> None:
    for idx, dep in enumerate(deps):
        if isinstance(dep, str):
            deps[idx] = pin_requirement(dep, version)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run pin_flet_deps.py <toml_file>")
        sys.exit(1)

    toml_path = Path(sys.argv[1]).resolve()
    if not toml_path.exists():
        print(f"Error: File not found: {toml_path}")
        sys.exit(1)

    version = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("FLET_VERSION")
    if not version:
        print("Error: FLET_VERSION env var or <version> argument is required.")
        sys.exit(1)

    print(f"Patching {toml_path} to flet version {version}")

    with toml_path.open(encoding="utf-8") as f:
        data = tomlkit.parse(f.read())

    project = data.get("project")
    if project and "dependencies" in project:
        pin_dependencies(project["dependencies"], version)

    dep_groups = data.get("dependency-groups")
    if dep_groups and "dev" in dep_groups:
        pin_dependencies(dep_groups["dev"], version)

    with toml_path.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(data))

    print("Done.")


if __name__ == "__main__":
    main()
