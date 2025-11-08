"""Autodoc generator for MkDocs — BuildingBlocks Edition.

- Scans all Python modules under `src/building_blocks/`
- Extracts top-level docstrings
- Generates .md files under `docs/reference/autodoc/`
- Updates mkdocs.yml under "Auto-Generated API Docs"
"""

#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

SRC_DIR = Path("src/building_blocks")
OUT_DIR = Path("docs/reference/autodoc")
MKDOCS_YML = Path("mkdocs.yml")


def read_docstring(file: Path) -> str:
    """Read the top-level docstring from a Python file."""
    try:
        source = file.read_text(encoding="utf-8")
        tree = ast.parse(source)
        return ast.get_docstring(tree) or ""
    except Exception as e:
        print(f"⚠️ Failed reading {file}: {e}")
        return ""


def module_title(path: Path) -> str:
    """Convert a module path to a title."""
    return path.stem.replace("_", " ").title()


def import_path(path: Path) -> str:
    """Convert a file path to a Python import path."""
    rel = path.relative_to(SRC_DIR)
    return f"building_blocks.{'.'.join(rel.with_suffix('').parts)}"


def ensure_dir(path: Path) -> None:
    """Ensure the parent directory of a path exists."""
    path.parent.mkdir(parents=True, exist_ok=True)


def find_source_files(base: Path) -> list[Path]:
    """Find all Python source files under a base directory, excluding __init__.py."""
    return [p for p in base.rglob("*.py") if p.name != "__init__.py"]


def generate_markdown(src: Path) -> Path:
    """Generate a markdown file for a given Python source file."""
    title = module_title(src)
    doc = read_docstring(src)
    out = OUT_DIR / src.relative_to(SRC_DIR).with_suffix(".md")
    ensure_dir(out)

    content = [f"# {title}", ""]
    if doc:
        content.append(doc)
        content.append("")

    content += [
        f"::: {import_path(src)}",
        "    options:",
        "      show_source: true",
        "      show_root_heading: true",
    ]
    out.write_text("\n".join(content), encoding="utf-8")

    print(f"✅ Generated: {out}")

    return out


def build_autodoc_section(files: list[Path], indent="  ") -> str:
    """Build the MkDocs navigation section for autodoc pages."""
    grouped: dict[str, list[tuple[str, str]]] = {}
    for f in files:
        parts = f.relative_to(OUT_DIR).parts
        if len(parts) < 2:
            continue
        layer = parts[0].title()
        title = parts[-1].replace("_", " ").removesuffix(".md").title()
        path = f"reference/autodoc/{'/'.join(parts)}"
        grouped.setdefault(layer, []).append((title, path))

    lines = [f"{indent}- Auto-Generated API Docs:"]
    for layer, entries in sorted(grouped.items()):
        lines.append(f"{indent}  - {layer}:")
        for name, link in sorted(entries):
            lines.append(f"{indent}    - {name}: {link}")
    return "\n".join(lines)


def update_nav(mkdocs: str, section: str) -> str:
    """Update the MkDocs navigation section with the autodoc section."""
    pattern = r"(?ms)^\s*- Auto-Generated API Docs:.*?(?=^\s*- [A-Z]|^[a-z_]+:|\Z)"
    if re.search(pattern, mkdocs):
        return re.sub(pattern, section, mkdocs)
    ref_pos = re.search(r"(?m)^\s*- Reference:", mkdocs)
    if ref_pos:
        insert = ref_pos.end()
        return mkdocs[:insert] + "\n" + section + "\n" + mkdocs[insert:]
    return mkdocs.rstrip() + "\n" + section + "\n"


def main() -> None:
    """Main function to generate autodoc pages and update mkdocs.yml."""
    if not SRC_DIR.exists():
        print(f"❌ Source directory not found: {SRC_DIR}")
        sys.exit(1)

    files = [generate_markdown(p) for p in find_source_files(SRC_DIR)]

    mkdocs_text = MKDOCS_YML.read_text(encoding="utf-8")
    section = build_autodoc_section(files)
    updated = update_nav(mkdocs_text, section)
    MKDOCS_YML.write_text(updated, encoding="utf-8")

    print("\n📘 Autodoc generation complete.\n")


if __name__ == "__main__":
    main()
