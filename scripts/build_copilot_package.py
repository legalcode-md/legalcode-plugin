#!/usr/bin/env python3
"""Validate and build the Microsoft 365 Copilot Cowork app package."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import jsonschema
from PIL import Image

from validate_claude_package import TOOLS, prose_links

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "plugins/legalcode-copilot"
CLAUDE = ROOT / "plugins/legalcode-claude"
SKILL = "skills/legalcode-mcp-guide"
SCHEMA_URL = "https://developer.microsoft.com/json-schemas/teams/v1.29/MicrosoftTeams.schema.json"
# Pin sorted, compact JSON so CDN whitespace changes do not alter the contract digest.
SCHEMA_SHA256 = "d8df4e18f6106933570768d68a2374185a1a3d8b07acb782469e17a30920dab7"
EXPECTED_FILES = {
    "manifest.json", "README.md", "LICENSE", "color.png", "outline.png",
    f"{SKILL}/SKILL.md", f"{SKILL}/LICENSE", f"{SKILL}/references/tool-examples.json",
}
SECRET = re.compile(
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    rb"\b(?:sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,})\b|"
    rb'"(?:access_token|refresh_token|client_secret|password)"\s*:\s*"[^"\s]+"'
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(package: Path, schema: dict) -> dict:
    paths = sorted(package.rglob("*"))
    require(not any(p.is_symlink() for p in paths), "Symlinks are not allowed")
    files = {p.relative_to(package).as_posix() for p in paths if p.is_file()}
    require(files == EXPECTED_FILES, f"Package inventory differs: {files ^ EXPECTED_FILES}")
    for name in files:
        data = (package / name).read_bytes()
        require(len(data) < 256 * 1024, f"Oversized file: {name}")
        require(not SECRET.search(data), f"Possible secret: {name}")
        require(b"${{" not in data, f"Unresolved template variable: {name}")

    manifest = json.loads((package / "manifest.json").read_text())
    validator = jsonschema.validators.validator_for(schema)
    # Microsoft's unused extensionFunction definition uses JS Unicode regex syntax
    # (\p{L}) that Python's metaschema regex checker cannot compile. Validate the
    # actual manifest; its selected definitions use Python-compatible patterns.
    validator(schema, format_checker=jsonschema.FormatChecker()).validate(manifest)
    require(manifest["$schema"] == SCHEMA_URL, "Unexpected manifest schema")
    require(manifest["agentSkills"] == [{"folder": f"./{SKILL}"}], "Expected one guide")
    connectors = manifest["agentConnectors"]
    require(len(connectors) == 1, "Expected one hosted connector")
    require(connectors[0]["toolSource"] == {
        "remoteMcpServer": {"mcpServerUrl": "https://mcp.legalcode.md/mcp"}
    }, "Cowork DCR requires the hosted URL and omitted authorization configuration")
    require(set(manifest) == {
        "$schema", "manifestVersion", "version", "id", "developer", "name",
        "description", "icons", "accentColor", "agentSkills", "agentConnectors",
    }, "Unexpected app capabilities or permissions")
    require(manifest["icons"] == {"color": "color.png", "outline": "outline.png"}, "Icon paths differ")
    require(manifest["developer"]["privacyUrl"] == "https://legalcode.md/privacy", "Privacy URL differs")
    require(manifest["developer"]["termsOfUseUrl"] == "https://legalcode.md/terms", "Terms URL differs")

    for name, size in [("color.png", (192, 192)), ("outline.png", (32, 32))]:
        with Image.open(package / name) as icon:
            require(icon.format == "PNG" and icon.size == size, f"Invalid icon: {name}")
            if name == "outline.png":
                pixels = list(icon.convert("RGBA").getdata())
                require(any(p[3] == 0 for p in pixels), "Outline needs transparency")
                require(all(p[:3] == (255, 255, 255) for p in pixels if p[3]), "Outline must be white")

    # Shared source equality prevents Microsoft and Claude research instructions drifting.
    for name in ["SKILL.md", "LICENSE", "references/tool-examples.json"]:
        require((package / SKILL / name).read_bytes() == (CLAUDE / SKILL / name).read_bytes(),
                f"Guide differs from current Claude source: {name}")
    require((package / "LICENSE").read_bytes() == (package / SKILL / "LICENSE").read_bytes(),
            "Package and guide licenses differ")
    subprocess.run(["skills-ref", "validate", str(package / SKILL)], check=True)
    for name in ["README.md", f"{SKILL}/SKILL.md"]:
        path = package / name
        text = path.read_text()
        for target in prose_links(text):
            target = target.split(' "')[0].split("#")[0]
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            resolved = (path.parent / target).resolve()
            require(resolved.is_relative_to(package.resolve()) and resolved.is_file(),
                    f"Missing or unsafe reference: {name}: {target}")
        require("https://github.com/legalcode-md/skills" in text and "CATALOG.md" in text
                and "skills/jurisdictions" in text, f"Missing optional skill references: {name}")
    examples = json.loads((package / SKILL / "references/tool-examples.json").read_text())
    require({e["tool"] for e in examples["examples"]} == TOOLS, "Seven-tool contract differs")
    return manifest


def main() -> None:
    with urllib.request.urlopen(SCHEMA_URL, timeout=30) as response:
        schema_bytes = response.read()
    schema = json.loads(schema_bytes)
    canonical_schema = json.dumps(schema, sort_keys=True, separators=(",", ":")).encode()
    require(hashlib.sha256(canonical_schema).hexdigest() == SCHEMA_SHA256,
            "Official schema changed; review the new snapshot before updating its pinned hash")
    manifest = validate(PACKAGE, schema)
    files = {name: (PACKAGE / name).read_bytes() for name in sorted(EXPECTED_FILES)}
    output = ROOT / "dist" / f"legalcode-copilot-{manifest['version']}.zip"
    output.parent.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="legalcode-copilot-") as temporary:
        archive_path = Path(temporary) / output.name
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(entry, data)
        extracted = Path(temporary) / "extracted"
        with zipfile.ZipFile(archive_path) as archive:
            require(archive.testzip() is None, "ZIP integrity failure")
            archive.extractall(extracted)
        validate(extracted, schema)
        require(all((extracted / name).read_bytes() == data for name, data in files.items()),
                "Extracted package differs from source")
        output.write_bytes(archive_path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(".zip.sha256").write_text(f"{digest}  {output.name}\n")
    report = {
        "archive": output.name, "version": manifest["version"], "app_id": manifest["id"],
        "bytes": output.stat().st_size, "sha256": digest,
        "schema": {"url": SCHEMA_URL, "canonical_json_sha256": SCHEMA_SHA256},
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
        "validation": {
            "official_manifest_schema": "passed", "source_and_extracted_conformance": "passed",
            "guide_parity_with_claude": "passed", "skills_ref": "passed", "icons": "passed",
            "secret_pattern_scan": "passed", "zip_integrity_and_byte_parity": "passed",
        },
        "limits": ["Tenant installation, OAuth consent, live Cowork research, and Microsoft acceptance are unverified."],
    }
    output.with_suffix(".validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"archive": str(output), "bytes": output.stat().st_size,
                      "files": len(files), "sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
