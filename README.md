# Legalcode Plugins

This repository contains separate submission packages for Legalcode on OpenAI and Claude.

Legalcode gives AI assistants authenticated access to primary legal sources through the hosted
MCP endpoint:

```text
https://mcp.legalcode.md/mcp
```

## Claude plugin

The Claude package is [`plugins/legalcode-claude`](plugins/legalcode-claude), with its marketplace
catalog in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). It includes the
Legalcode research guide and hosted MCP connection. Document-to-skill, Tabulate, and the
[jurisdiction and task skill collection](https://github.com/legalcode-md/skills) are linked
for separate installation.
See [Claude submission details](docs/claude-submission.md) for the repository URL and plugin path.

```sh
claude plugin validate plugins/legalcode-claude --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## OpenAI submission package

The uploadable package is [`plugins/legalcode-openai`](plugins/legalcode-openai). It contains:

- the OpenAI plugin manifest;
- Legalcode brand assets and notices; and
- one provider-neutral skill: `legalcode-mcp-guide`.

The package deliberately contains no CLI, local MCP server, scripts, hooks, custom app, or
client-specific Claude/Codex bundles. Specialized legal workflow skills are maintained and
distributed separately so users can add only the workflows they need.

The hosted MCP connection is declared in the package's `.mcp.json` and entered again in the OpenAI
submission portal. Reviewer credentials remain only in the portal's private fields.
[`chatgpt-app-submission.json`](chatgpt-app-submission.json) is the checked-in worksheet for the
listing, tool annotations, and submission test cases.

## Validate

Run the pinned Python 3.11+ validation environment with `uv`:

```bash
uv run --python 3.13 --with-requirements requirements-dev.txt \
  python scripts/validate_openai_submission.py
```

The validator checks the exact one-skill inventory, MCP dependency metadata, package boundaries,
manifest assets, routing cases, and submission worksheet.

Build the upload archive and validate its extracted contents:

```bash
uv run --python 3.13 --with-requirements requirements-dev.txt \
  python scripts/build_openai_package.py
```

The archive, checksum and validation report are written under `dist/`. Upload the archive to the
existing Legalcode plugin. Hosted MCP tool approval is handled separately from package uploads.
The GitHub Actions conformance workflow builds the same package and saves it as the
`legalcode-openai-upload` artifact. Claude and OpenAI release independently and validate their own
skill inventories and tool contracts. Both retain the same hosted MCP connection.

## Licenses

Repository tooling and the packaged MCP guide use MIT. Optional skills in the separate
[Legalcode skill collection](https://github.com/legalcode-md/skills) retain their own licenses;
they are not bundled or relicensed by this repository.

Validate the Claude package with:

```sh
uv run --python 3.13 --with-requirements requirements-dev.txt \
  python scripts/validate_claude_package.py
```
