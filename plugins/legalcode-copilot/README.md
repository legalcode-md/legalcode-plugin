# Legalcode for Microsoft 365 Copilot Cowork

Research primary legal sources through the hosted Legalcode MCP connection. The included
`legalcode-mcp-guide` helps Cowork discover coverage, find authorities, verify source text,
and present citations with official links. It covers Discover, Search, Fetch, Patent Search,
Patent Fetch, Analyze, and Trace. Coverage and access vary by source, jurisdiction, and account.

## Install and connect

Build the ZIP using the [repository build instructions](https://github.com/legalcode-md/legalcode-plugin/blob/main/docs/copilot-submission.md).
Use a Microsoft 365 work account with access to Cowork and permission to install custom apps.
For personal testing, install Microsoft 365 Agents Toolkit and run:

```sh
npm install -g @microsoft/m365agentstoolkit-cli
atk auth login
atk install --file-path ./dist/legalcode-copilot-1.0.0.zip --scope Personal
```

For tenant distribution, an administrator uploads the ZIP through Microsoft 365 admin center >
Manage apps > Upload custom app > Add agent. Open Cowork > Sources & Skills > Plugins, enable
Legalcode, and complete Legalcode sign-in when prompted. Tenant policy and feature availability
can affect installation. Public App Store distribution requires a separate Partner Center submission.

This package uses Microsoft's Cowork plugin format (manifest 1.29). The connector URL is
`https://mcp.legalcode.md/mcp`. Cowork discovers OAuth and dynamically registers a client;
the omitted `authorization` object enables that flow. It does not mean anonymous access.
No credentials or Microsoft token-store placeholders are embedded in the package.

This authentication configuration targets **Copilot Cowork**. Regular Copilot Chat requires a
separate Microsoft `OAuthPluginVault` registration and the corresponding agent configuration;
this ZIP does not claim that compatibility. See Microsoft's
[Cowork packaging and authentication guide](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development).

## Try it

- “What Icelandic legislation and court decisions address termination of employment? Verify the relevant passages and link the official sources.”
- “Find this EU directive and trace its Icelandic implementation. Distinguish indexed relationships from verified source text.”
- “Retrieve patent publication EP1000000A1. Say whether claims and description text were actually retrieved.”

The guide checks current source coverage before research. Missing coverage, unavailable tools,
access restrictions, and incomplete text must be stated explicitly.

## Optional skills

The package includes one research guide. Browse the separate
[Legalcode skill collection](https://github.com/legalcode-md/skills),
[task and practice-area catalogue](https://github.com/legalcode-md/skills/blob/main/CATALOG.md),
[jurisdiction workflows](https://github.com/legalcode-md/skills/tree/main/skills/jurisdictions), and
[general workflows](https://github.com/legalcode-md/skills/tree/main/skills/general).

[Document-to-skill](https://github.com/legalcode-md/skills/tree/main/skills/general/drafting-documents/legalcode-document-to-skill)
and [Tabulate](https://github.com/legalcode-md/skills/tree/main/skills/general/drafting-documents/legalcode-tabulate)
are optional workflows. A link does not install a skill. Check its host support, prerequisites,
and license before installing it separately.

## Data handling and license

Selected tool arguments, including search terms, jurisdictions, filters, source identifiers, and
requested text ranges, are sent to the hosted Legalcode service. Legalcode returns legal-source
metadata and text. Patent tools access the external European Patent Office service through
Legalcode. Include confidential matter details in queries only when necessary and authorized.

The package requests no Microsoft Graph permissions and includes no document-upload workflow,
executable helpers, or hooks. Account and operational records are handled under the
[privacy policy](https://legalcode.md/privacy); this package does not promise zero retention.

Published by **Fordæmi ehf.** See [terms](https://legalcode.md/terms) and
[support](https://legalcode.md/contact). The package and guide use the [MIT license](LICENSE).
Optional skills retain their own licenses. Verify legal conclusions against the underlying sources.
