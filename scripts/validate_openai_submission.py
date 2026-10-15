#!/usr/bin/env python3
"""Validate the exact Legalcode OpenAI submission package."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "plugins" / "legalcode-openai"
SKILL_NAME = "legalcode-mcp-guide"
MCP_URL = "https://mcp.legalcode.md/mcp"
OPENAI_PLUGIN_NAME = "app-6a5fc36564608191827f4e7716bdaba0"
TOOLS = {
    "legalcode_discover",
    "legalcode_search",
    "legalcode_fetch",
    "legalcode_patents",
    "legalcode_analyze",
    "legalcode_trace",
}
TRACE_RELATIONSHIPS = {
    "cases_for_law",
    "cited_cases",
    "citing_cases",
    "eea_incorporation_for_law",
    "eu_law_for_implementing_law",
    "implementing_laws_for_eu_law",
    "laws_for_case",
    "pre_law_for_law",
    "related_pre_law_flows",
}
EXPECTED_PACKAGE_FILES = {
    ".codex-plugin/plugin.json",
    ".mcp.json",
    "LICENSE",
    "README.md",
    "THIRD_PARTY_NOTICES.md",
    "assets/legalcode-composer-48.png",
    "assets/legalcode-directory-256.png",
    "assets/legalcode-directory-512.png",
    f"skills/{SKILL_NAME}/SKILL.md",
    f"skills/{SKILL_NAME}/agents/openai.yaml",
    f"skills/{SKILL_NAME}/references/tool-examples.json",
}
ROUTING_SEQUENCES = {
    "activate_source_coverage": ["legalcode_discover"],
    "activate_aggregate_workflow": [
        "legalcode_discover",
        "legalcode_analyze",
        "legalcode_search",
        "legalcode_fetch",
    ],
    "activate_legislative_history": [
        "legalcode_discover",
        "legalcode_search",
        "legalcode_trace",
        "legalcode_search",
        "legalcode_fetch",
    ],
    "activate_exact_authority": [
        "legalcode_discover",
        "legalcode_search",
        "legalcode_fetch",
    ],
    "activate_implementation_trace": [
        "legalcode_discover",
        "legalcode_trace",
        "legalcode_fetch",
    ],
    "activate_filter_recovery": ["legalcode_discover", "legalcode_search"],
    "activate_incomplete_authority": [],
    "activate_exact_patent": ["legalcode_patents", "legalcode_patents"],
}
MACHINE_PROMPT_PATTERN = re.compile(
    r"\b(?:sourceRef|lawKey|flowKey|sourceCode|document_count)\b|"
    r"source reference|law/[A-Z]{2}/",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return value


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def validate_package(failures: list[str]) -> Path:
    actual_files = {
        str(path.relative_to(PACKAGE_ROOT))
        for path in PACKAGE_ROOT.rglob("*")
        if path.is_file() and path.name != ".DS_Store"
    }
    require(
        actual_files == EXPECTED_PACKAGE_FILES,
        "OpenAI package file inventory differs from the exact submission bundle: "
        f"missing={sorted(EXPECTED_PACKAGE_FILES - actual_files)}, "
        f"extra={sorted(actual_files - EXPECTED_PACKAGE_FILES)}",
        failures,
    )

    manifest_path = PACKAGE_ROOT / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)
    require(manifest.get("name") == OPENAI_PLUGIN_NAME,
            f"OpenAI plugin name must match the existing dashboard identity: {OPENAI_PLUGIN_NAME}",
            failures)
    require(
        isinstance(manifest.get("version"), str)
        and re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]) is not None,
        "Plugin version must use strict semantic versioning",
        failures,
    )
    require(manifest.get("skills") == "./skills/", "Manifest must declare ./skills/", failures)
    require(
        manifest.get("mcpServers") == "./.mcp.json",
        "Manifest must declare the bundled Legalcode MCP configuration",
        failures,
    )
    require(
        not ({"apps", "hooks"} & set(manifest)),
        "Apps and hooks must not be embedded in the package manifest",
        failures,
    )

    mcp_config = load_json(PACKAGE_ROOT / ".mcp.json")
    require(
        mcp_config
        == {
            "mcpServers": {
                "legalcode": {
                    "type": "http",
                    "url": MCP_URL,
                    "oauth_resource": MCP_URL,
                }
            }
        },
        "Bundled MCP configuration must declare the canonical hosted Legalcode endpoint",
        failures,
    )

    interface = manifest.get("interface", {})
    require(
        isinstance(interface, dict),
        "Manifest interface must be an object",
        failures,
    )
    if isinstance(interface, dict):
        for field, maximum in {
            "displayName": 30,
            "shortDescription": 30,
            "longDescription": 4000,
            "developerName": 80,
            "category": 80,
        }.items():
            value = interface.get(field)
            require(isinstance(value, str) and 0 < len(value) <= maximum,
                    f"Manifest {field} is missing or exceeds its submission limit", failures)
        for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
            value = interface.get(field)
            require(isinstance(value, str) and value.startswith("https://") and len(value) <= 1024,
                    f"Manifest {field} must contain the public HTTPS listing URL", failures)
        prompts = interface.get("defaultPrompt", [])
        require(
            isinstance(prompts, list)
            and 1 <= len(prompts) <= 3
            and all(isinstance(prompt, str) and len(prompt) <= 128 for prompt in prompts),
            "Manifest must contain one to three default prompts of at most 128 characters",
            failures,
        )
        for key in ("composerIcon", "logo"):
            value = interface.get(key)
            require(
                isinstance(value, str)
                and value.startswith("./")
                and (PACKAGE_ROOT / value[2:]).is_file(),
                f"Manifest {key} must reference an included package asset",
                failures,
            )

    examples = load_json(PACKAGE_ROOT / "skills" / SKILL_NAME / "references" / "tool-examples.json")
    require({entry.get("tool") for entry in examples.get("examples", [])} == TOOLS,
            "Packaged call examples must cover all six tools", failures)

    skills_root = PACKAGE_ROOT / "skills"
    skill_directories = {path.name for path in skills_root.iterdir() if path.is_dir()}
    require(
        skill_directories == {SKILL_NAME},
        f"OpenAI package must contain only the {SKILL_NAME} skill",
        failures,
    )

    skill_root = skills_root / SKILL_NAME
    skill_path = skill_root / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
    require(frontmatter_match is not None, "Skill must begin with YAML frontmatter", failures)
    if frontmatter_match is not None:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        require(
            isinstance(frontmatter, dict) and frontmatter.get("name") == SKILL_NAME,
            "Skill frontmatter name must match its directory",
            failures,
        )
        description = (
            frontmatter.get("description", "")
            if isinstance(frontmatter, dict)
            else ""
        )
        require(
            "capabilit" in description.lower() and "recover" in description.lower(),
            "Skill description must cover capability questions and error recovery",
            failures,
        )

    require(
        "Copy the returned `sourceRef` exactly" in skill_text,
        "Skill must distinguish sourceRef chaining handles from legal citations",
        failures,
    )
    require(
        "inside tool calls" in skill_text,
        "Skill must keep machine identifiers out of ordinary reader-facing answers",
        failures,
    )
    require(
        "titles, legal citations, decision numbers" in skill_text,
        "Skill must require natural-language labels for machine fields and metrics",
        failures,
    )

    forbidden_skill_patterns = {
        "CLI or shell dependency": r"\b(?:CLI|Bash|shell|npm|pnpm|bun|python)\b",
        "provider-specific instruction": r"\b(?:Claude|Codex|ChatGPT|OpenAI)\b",
        "executable code fence": r"```(?:bash|sh|zsh|python|javascript|typescript)",
    }
    for markdown_path in skill_root.rglob("*.md"):
        markdown_text = markdown_path.read_text(encoding="utf-8")
        for label, pattern in forbidden_skill_patterns.items():
            require(
                re.search(pattern, markdown_text, re.IGNORECASE) is None,
                f"{markdown_path.relative_to(PACKAGE_ROOT)} contains a {label}",
                failures,
            )
        for index, example in enumerate(
            re.findall(r"```json\n(.*?)\n```", markdown_text, re.DOTALL),
            start=1,
        ):
            try:
                json.loads(example)
            except json.JSONDecodeError as error:
                failures.append(
                    f"{markdown_path.relative_to(PACKAGE_ROOT)} JSON example "
                    f"{index} is invalid: {error}"
                )

    combined_skill_text = "\n".join(
        path.read_text(encoding="utf-8") for path in skill_root.rglob("*.md")
    )
    for tool in TOOLS:
        require(
            tool in combined_skill_text,
            f"MCP guide must document {tool}",
            failures,
        )
    for relationship in TRACE_RELATIONSHIPS:
        require(
            relationship in skill_text,
            f"MCP guide must preserve the Trace starting point for {relationship}",
            failures,
        )

    metadata_path = skill_root / "agents" / "openai.yaml"
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    expected_dependency = {
        "tools": [
            {
                "type": "mcp",
                "value": "legalcode",
                "description": "Search, retrieve, analyze, and trace primary legal sources",
                "transport": "streamable_http",
                "url": MCP_URL,
            }
        ]
    }
    require(
        isinstance(metadata, dict) and metadata.get("dependencies") == expected_dependency,
        "Skill metadata must declare the hosted Legalcode MCP dependency",
        failures,
    )
    default_prompt = (
        metadata.get("interface", {}).get("default_prompt")
        if isinstance(metadata, dict)
        else None
    )
    require(
        isinstance(default_prompt, str) and f"${SKILL_NAME}" in default_prompt,
        f"Skill default prompt must mention ${SKILL_NAME}",
        failures,
    )
    return skill_root


def validate_local_marketplace(failures: list[str]) -> None:
    marketplace = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    require(
        marketplace
        == {
            "name": "legalcode-local",
            "interface": {"displayName": "Legalcode Local"},
            "plugins": [
                {
                    "name": OPENAI_PLUGIN_NAME,
                    "source": {
                        "source": "local",
                        "path": "./plugins/legalcode-openai",
                    },
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Business & Operations",
                }
            ],
        },
        "Local marketplace must install the canonical OpenAI package",
        failures,
    )


def validate_claude_connection(failures: list[str]) -> None:
    claude_root = REPO_ROOT / "plugins" / "legalcode-claude"
    claude_manifest = load_json(claude_root / ".claude-plugin" / "plugin.json")
    require(claude_manifest.get("name") == "legalcode",
            "Claude must retain its own legalcode plugin identity", failures)
    require(load_json(claude_root / ".mcp.json") == load_json(PACKAGE_ROOT / ".mcp.json"),
            "Both packages must retain the same hosted MCP connection", failures)
    # Provider packages release independently; validate each guide against its own tool contract.
    marketplace = load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
    entries = [entry for entry in marketplace.get("plugins", [])
               if entry.get("name") == claude_manifest["name"]]
    require(len(entries) == 1 and entries[0].get("version") == claude_manifest["version"],
            "Claude marketplace version must match the release package", failures)


def validate_routing(failures: list[str]) -> None:
    document = load_json(REPO_ROOT / "tests" / "openai-skill-routing.json")
    cases = document.get("cases")
    require(document.get("included_skills") == [SKILL_NAME], "Routing inventory drifted", failures)
    require(isinstance(cases, list) and len(cases) >= 7, "Routing cases are incomplete", failures)
    if not isinstance(cases, list):
        return
    cases_by_id = {
        case.get("id"): case
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("id"), str)
    }
    require(
        len(cases_by_id) == len(cases),
        "Routing case IDs must be present and unique",
        failures,
    )
    for case_id, expected_sequence in ROUTING_SEQUENCES.items():
        case = cases_by_id.get(case_id)
        require(case is not None, f"Routing fixture is missing {case_id}", failures)
        if case is not None:
            require(
                case.get("expected_skill") == SKILL_NAME,
                f"Routing case {case_id} must activate {SKILL_NAME}",
                failures,
            )
            require(
                case.get("expected_sequence") == expected_sequence,
                f"Routing case {case_id} must follow the packaged skill workflow",
                failures,
            )
    implicit_negative = cases_by_id.get("nonactivation_contract_edit_implicit")
    require(
        implicit_negative is not None
        and implicit_negative.get("expected_skill") is None
        and implicit_negative.get("expected_sequence") == [],
        "Routing fixtures must include a near-domain drafting request that does not activate Legalcode",
        failures,
    )
    output_contract_cases = 0
    for case in cases:
        require(isinstance(case, dict), "Every routing case must be an object", failures)
        if not isinstance(case, dict):
            continue
        require(
            case.get("expected_skill") in {SKILL_NAME, None},
            f"Routing case {case.get('id')} names an unbundled skill",
            failures,
        )
        sequence = case.get("expected_sequence")
        require(
            isinstance(sequence, list) and all(tool in TOOLS for tool in sequence),
            f"Routing case {case.get('id')} has an invalid tool sequence",
            failures,
        )
        prompt = case.get("prompt")
        require(
            isinstance(prompt, str)
            and MACHINE_PROMPT_PATTERN.search(prompt) is None
            and "persónuvernd" not in prompt.casefold(),
            f"Routing case {case.get('id')} exposes machine vocabulary or Icelandic query text",
            failures,
        )
        if case.get("expected_skill") == SKILL_NAME and sequence:
            require(
                sequence[0] == ("legalcode_patents" if case.get("id") == "activate_exact_patent" else "legalcode_discover"),
                f"Routing case {case.get('id')} must Discover before Search, Analyze, or Trace",
                failures,
            )
        output_contract = case.get("expected_output_contract")
        if output_contract is not None:
            output_contract_cases += 1
            require(
                isinstance(output_contract, list)
                and all(isinstance(requirement, str) for requirement in output_contract),
                f"Routing case {case.get('id')} has an invalid output contract",
                failures,
            )
    require(
        output_contract_cases >= 1,
        "Routing fixtures must test reader-facing output quality, not only activation",
        failures,
    )


def validate_submission_worksheet(failures: list[str]) -> None:
    worksheet = load_json(REPO_ROOT / "chatgpt-app-submission.json")
    require(
        worksheet.get("$schema")
        == "https://developers.openai.com/apps-sdk/schemas/chatgpt-app-submission.v1.json",
        "Submission worksheet schema URL drifted",
        failures,
    )
    require(set(worksheet.get("tools", {})) == TOOLS, "Worksheet tool inventory drifted", failures)
    test_cases = worksheet.get("test_cases")
    negative_cases = worksheet.get("negative_test_cases")
    require(
        isinstance(test_cases, list) and len(test_cases) == 5,
        "Submission worksheet must contain exactly five positive test cases",
        failures,
    )
    require(
        isinstance(negative_cases, list) and len(negative_cases) == 3,
        "Submission worksheet must contain exactly three negative test cases",
        failures,
    )
    if isinstance(test_cases, list):
        cases_by_tool = {case.get("tools_triggered"): case for case in test_cases if isinstance(case, dict)}
        covered_tools = {tool.strip() for names in cases_by_tool if isinstance(names, str)
                         for tool in names.split(",")}
        require(
            covered_tools == TOOLS,
            "Five positive submission cases must collectively cover all six Legalcode tools",
            failures,
        )
        for tool, case in cases_by_tool.items():
            prompt = case.get("user_prompt")
            expected_output = case.get("expected_output")
            require(
                isinstance(prompt, str) and "persónuvernd" not in prompt.casefold(),
                f"Worksheet prompt for {tool} contains Icelandic query text",
                failures,
            )
            require(
                isinstance(prompt, str)
                and MACHINE_PROMPT_PATTERN.search(prompt) is None,
                f"Worksheet prompt for {tool} exposes machine vocabulary",
                failures,
            )
            require(
                isinstance(expected_output, str)
                and MACHINE_PROMPT_PATTERN.search(expected_output) is None,
                f"Worksheet expected output for {tool} exposes machine vocabulary",
                failures,
            )
    if isinstance(negative_cases, list):
        require(
            all(case.get("tools_triggered") is None for case in negative_cases),
            "Negative submission cases must not trigger a Legalcode tool",
            failures,
        )
    manifest = load_json(PACKAGE_ROOT / ".codex-plugin" / "plugin.json")
    review = manifest.get("extensions", {}).get("com.openai", {}).get("review", {})
    packaged_cases = review.get("test_cases", {})
    for source, kind in ((test_cases, "positive"), (negative_cases, "negative")):
        expected = []
        for case in source or []:
            entry = {"description": case["description"], "prompt": case["user_prompt"],
                     "expected_behavior": case["expected_output"]}
            if kind == "positive":
                entry["tools_triggered"] = case["tools_triggered"]
            expected.append(entry)
        require(packaged_cases.get(kind) == expected,
                f"Packaged {kind} review cases must match the submission worksheet", failures)
    for tool, entry in worksheet.get("tools", {}).items():
        require(entry.get("annotations") == {
            "readOnlyHint": True, "openWorldHint": tool == "legalcode_patents",
            "destructiveHint": False, "idempotentHint": True,
        }, f"Worksheet safety hints drifted for {tool}", failures)
    require(not ({"test_credentials", "reviewer_instructions"} & set(review)),
            "Private reviewer access must stay outside the ZIP", failures)


def validate_reader_facing_docs(failures: list[str]) -> None:
    worksheet = load_json(REPO_ROOT / "chatgpt-app-submission.json")
    reader_facing_texts = {
        "demo script": (REPO_ROOT / "docs" / "demo-video-script.md").read_text(
            encoding="utf-8"
        ),
        "listing copy": worksheet.get("app_info", {}).get("description", ""),
        "package README": (PACKAGE_ROOT / "README.md").read_text(encoding="utf-8"),
        "submission guide": (REPO_ROOT / "docs" / "submission.md").read_text(
            encoding="utf-8"
        ),
    }
    for label, text in reader_facing_texts.items():
        for forbidden in ("sourceRef", "source reference", "law/IS/", "persónuvernd"):
            require(
                forbidden.casefold() not in text.casefold(),
                f"{label} exposes forbidden reader-facing vocabulary: {forbidden}",
                failures,
            )


def validate_skill_reference(skill_root: Path, failures: list[str]) -> None:
    executable = shutil.which("skills-ref")
    if executable is None:
        failures.append("skills-ref is unavailable; install requirements-dev.txt")
        return
    result = subprocess.run(
        [executable, "validate", str(skill_root)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip()
        failures.append(f"skills-ref validation failed: {details or 'no diagnostic output'}")


def main() -> int:
    global PACKAGE_ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT,
                        help="Validate an extracted ZIP against the source worksheet and routing contracts")
    PACKAGE_ROOT = parser.parse_args().package_root.resolve()
    failures: list[str] = []
    try:
        skill_root = validate_package(failures)
        validate_local_marketplace(failures)
        validate_claude_connection(failures)
        validate_routing(failures)
        validate_submission_worksheet(failures)
        validate_reader_facing_docs(failures)
        validate_skill_reference(skill_root, failures)
    except Exception as error:
        failures.append(str(error))

    if failures:
        print("OpenAI submission conformance failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        "OpenAI submission conformance passed: "
        "1 plugin package, 1 self-contained MCP guide skill."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
