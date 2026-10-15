#!/usr/bin/env python3
"""Check Claude's complete skill inventory, provenance, references, and tool contract."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins/legalcode-claude"
SKILLS = {"legalcode-mcp-guide", "legalcode-document-to-skill", "legalcode-tabulate"}
TOOLS = {
    "legalcode_discover", "legalcode_search", "legalcode_fetch",
    "legalcode_patent_search", "legalcode_patent_fetch", "legalcode_analyze", "legalcode_trace",
}


def prose_links(text: str) -> list[str]:
    """Exclude examples of files to be generated, rather than shipped references."""
    prose, fence = [], None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, rest = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is None:
            prose.append(line)
    return re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", "\n".join(prose))


def main() -> None:
    skills_root = PACKAGE / "skills"
    actual = {p.name for p in skills_root.iterdir() if p.is_dir()}
    assert actual == SKILLS, f"Skill inventory mismatch: {actual}"
    for path in PACKAGE.rglob("*"):
        assert not path.is_symlink(), f"Symlink in plugin: {path}"
        assert path.name not in {".DS_Store", "Thumbs.db", "desktop.ini", "__MACOSX", "__pycache__"}, path
        if path.is_file():
            assert path.stat().st_size < 256 * 1024, f"Oversized file: {path}"
    assert sum(p.is_file() for p in PACKAGE.rglob("*")) <= 512
    for name in sorted(SKILLS):
        skill = skills_root / name
        text = (skill / "SKILL.md").read_text()
        front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        assert front, f"Missing frontmatter: {name}"
        meta = yaml.safe_load(front[1])
        assert meta["name"] == name and isinstance(meta["description"], str)
        for path in skill.rglob("*.md"):
            for target in prose_links(path.read_text()):
                target = target.split(' "')[0].split("#")[0]
                if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                if any(char in target for char in "{}[]"):
                    continue
                resolved = (path.parent / target).resolve()
                assert resolved.is_relative_to(skill.resolve()) and resolved.exists(), (path, target)
        subprocess.run(["skills-ref", "validate", str(skill)], check=True)

    provenance = json.loads((PACKAGE / "skills-provenance.json").read_text())
    assert provenance["repository"] == "https://github.com/legalcode-md/skills"
    assert re.fullmatch(r"[0-9a-f]{40}", provenance["commit"])
    assert set(provenance["skills"]) == SKILLS - {"legalcode-mcp-guide"}
    for name, entry in provenance["skills"].items():
        directory = skills_root / name
        files = {str(p.relative_to(directory)): p for p in directory.rglob("*") if p.is_file()}
        assert set(files) == set(entry["files"]), f"Incomplete package: {name}"
        for relative, path in files.items():
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["files"][relative], path
        assert (directory / "LICENSE.md").read_bytes() == (PACKAGE / "LICENSE.md").read_bytes()

    guide = (skills_root / "legalcode-mcp-guide/SKILL.md").read_text()
    assert "legalcode_patents" not in guide, "Retired tool alias in Claude guide"
    examples = json.loads((skills_root / "legalcode-mcp-guide/references/tool-examples.json").read_text())
    assert {e["tool"] for e in examples["examples"]} == TOOLS
    for example in examples["examples"]:
        assert example["tool"] in guide
        if example["tool"].startswith("legalcode_patent_"):
            assert "action" not in example["input"]
    for text in [guide, (PACKAGE / "README.md").read_text()]:
        assert "https://github.com/legalcode-md/skills" in text
        assert "skills/jurisdictions" in text and "CATALOG.md" in text
    manifest = json.loads((PACKAGE / ".claude-plugin/plugin.json").read_text())
    assert (PACKAGE / manifest["icon"]).is_file()
    assert "https://legalcode.md/privacy" in (PACKAGE / "README.md").read_text()
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    entry = next(p for p in marketplace["plugins"] if p["name"] == manifest["name"])
    assert entry["version"] == manifest["version"] and entry["source"] == "./plugins/legalcode-claude"
    mcp = json.loads((PACKAGE / ".mcp.json").read_text())
    assert mcp["mcpServers"]["legalcode"]["url"] == "https://mcp.legalcode.md/mcp"
    print(f"Claude package passed: 3 complete skills, 7 tools, provenance {provenance['commit']}.")


if __name__ == "__main__":
    main()
