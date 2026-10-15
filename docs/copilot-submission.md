# Microsoft 365 Copilot Cowork package

Source: [`plugins/legalcode-copilot`](../plugins/legalcode-copilot).
Canonical repository: <https://github.com/legalcode-md/legalcode-plugin>.

This is a Microsoft 365 Cowork plugin with one MCP research guide and one hosted connector.
The guide, examples, and MIT license are byte-identical to the current Claude guide. It links
to Document-to-skill, Tabulate, and jurisdiction/task skills for separate installation.
Claude and OpenAI keep their own package formats and release versions.

## Build and validate

From the repository root:

```sh
uv run --python 3.13 --with-requirements requirements-copilot.txt \
  python scripts/build_copilot_package.py
```

The build downloads Microsoft's official manifest 1.29 schema and checks its pinned canonical
JSON digest before validation. Network access is required. If the schema changes, review the
semantic diff before deliberately updating the pinned hash. Python's schema self-check is
skipped because unused Microsoft definitions contain JavaScript Unicode regex syntax;
validation of the actual manifest still runs.

Checks cover the strict manifest schema, one guide/connector, current seven-tool examples,
guide parity with Claude, Agent Skills validation, icon dimensions and outline transparency,
local references, MIT license parity, exact file inventory, common secret patterns, ZIP
integrity, and extracted/source byte equality. No executable helper is included.

Outputs:

- `dist/legalcode-copilot-1.0.0.zip`
- `dist/legalcode-copilot-1.0.0.zip.sha256`
- `dist/legalcode-copilot-1.0.0.validation.json`

GitHub Actions builds the same files and saves them in the `legalcode-copilot-upload` artifact.
The manifest, icons, guide, README, and licenses sit directly inside the ZIP; no enclosing folder.
Keep the manifest's app ID stable for updates and increment its version for releases.

For Microsoft's additional package checks, install Agents Toolkit and run:

```sh
npm install -g @microsoft/m365agentstoolkit-cli
atk validate --package-file ./dist/legalcode-copilot-1.0.0.zip \
  --validate-method validation-rules --telemetry false
```

These checks do not establish successful tenant installation, OAuth consent, live research in
Cowork, or Microsoft approval. Follow the package README to install and run the reviewer scenarios.

The initial local build on 2026-10-15 passed the checks above. Agents Toolkit 1.1.18's
`validation-rules` check required Microsoft 365 sign-in before returning a validation result;
that platform check remains pending. Public Legalcode OAuth discovery advertised DCR and PKCE
S256, and the live server card advertised all seven read-only tools on `/mcp`.

## Authentication and host scope

Manifest 1.29 permits a URL-only `agentConnectors[].toolSource.remoteMcpServer`. The connector
points to `https://mcp.legalcode.md/mcp` and deliberately omits `authorization`. In Cowork this
uses Dynamic Client Registration (DCR), rather than declaring anonymous access or embedding a
dummy vault reference. Legalcode's public OAuth metadata advertises `/oauth/register` and PKCE S256.

Microsoft documents omitted authorization only for **Cowork**. Regular Copilot Chat requires a
separate `OAuthPluginVault` registration and corresponding agent configuration. This package
must not be described as verified for regular Copilot Chat. A different Microsoft host should
get its own package and validation rather than weakening this connector's authentication.

The manifest requests no Graph permissions. Tool arguments go to Legalcode; patent tools use
the EPO service through Legalcode. Account/operational retention follows the privacy policy.
See the [package disclosure](../plugins/legalcode-copilot/README.md#data-handling-and-license).

## Reviewer scenarios

1. Install in an eligible Microsoft 365 work tenant; record the returned app/title IDs privately.
2. Enable the plugin in Cowork and sign in through Legalcode OAuth. Confirm success in the
   authenticated Cowork session; metadata discovery alone does not prove this flow.
3. Ask what Icelandic law and case sources are available. Confirm current Discover coverage
   governs tool selection and no unavailable source is promised.
4. Research an Icelandic employment question. Confirm Search candidates are followed by Fetch,
   with readable legal citations, exact provision locators, and official links in the answer.
5. Ask for EU-to-national implementation tracing. Confirm relationship targets are verified
   through Fetch and missing evidence is reported explicitly.
6. Retrieve an exact patent publication. Confirm separate patent Search/Fetch tools and truthful
   reporting when claims or description text is unavailable.
7. Ask about optional Document-to-skill/Tabulate and jurisdiction skills. Confirm links are
   offered without claiming those skills are installed or bundled.

## Icon provenance

The Microsoft-sized brand icons were reused from Legalcode's existing local Microsoft 365
scaffold, based on the Legalcode brand mark. Both were visually inspected before reuse.
The 192px color icon places the mark in the central safe area; the 32px outline is white with
a transparent background. SHA-256:

```text
color.png    72ce59692120426ccf243629966d0425688b1fd40613cf3fd8bd9a67ec1d3219
outline.png  75dfc516a2801f0463baab30405fa7815f68fd1eccaedf4d658ad6bd4ef8983b
```

## Microsoft references

- [Build plugins for Copilot Cowork](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)
- [Official manifest 1.29 schema](https://developer.microsoft.com/json-schemas/teams/v1.29/MicrosoftTeams.schema.json)
- [Configure MCP/API plugin authentication](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api-plugin-authentication)

Tenant deployment and public Partner Center submission are separate steps. This repository
provides the package and validation tooling; it does not represent a Microsoft approval.
