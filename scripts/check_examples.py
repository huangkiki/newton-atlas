"""Parse teaching Python files and fenced snippets without importing an engine."""

import ast
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
files = sorted((root / "examples").rglob("*.py"))
for path in files:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path.relative_to(root)))

snippet_count = 0
for page in sorted(root.rglob("*.md")):
    if any(part in {".git", ".venv", "build", "outputs"} for part in page.relative_to(root).parts):
        continue
    text = page.read_text(encoding="utf-8")
    for match in re.finditer(r"^```(?:python|py)\s*\n(.*?)^```\s*$", text, re.M | re.S):
        line = text[:match.start()].count("\n") + 1
        ast.parse(match.group(1), filename=f"{page.relative_to(root)}:{line}")
        snippet_count += 1

print(f"Python syntax passed: {len(files)} example files, {snippet_count} Markdown snippets; none executed.")
