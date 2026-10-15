# Legalcode for Claude

Research primary legal sources through the hosted Legalcode MCP connection. The included
`legalcode-mcp-guide` helps Claude discover source coverage, find authorities, verify their text,
and keep conclusions tied to citations and official links.

The guide coordinates seven read-only tools: Discover, Search, Fetch, Patent Search, Patent
Fetch, Analyze, and Trace. Coverage and permissions vary by jurisdiction, source, and account;
the guide checks the connected schemas and current source coverage before research.

Try asking Claude to research an Icelandic legal issue with verified legislation and case law,
find EU legislation and trace national implementation, or retrieve an exact patent publication.

## Install and connect

In Claude Code:

```text
/plugin install legalcode --marketplace legalcode-md/legalcode-plugin
```

In Claude and Cowork, add this repository as a marketplace from Customize > Plugins, then
select Legalcode. Connect the bundled remote connector at `https://mcp.legalcode.md/mcp`
through the plugin's Connectors tab and complete Legalcode authentication.

## Optional document, jurisdiction, and task skills

Additional workflows are available separately:

- [Document-to-skill](https://github.com/legalcode-md/skills/tree/main/skills/general/drafting-documents/legalcode-document-to-skill): turn Word or PowerPoint precedents into reusable drafting skills that preserve house style.
- [Tabulate](https://github.com/legalcode-md/skills/tree/main/skills/general/drafting-documents/legalcode-tabulate): turn documents into traceable Excel workbooks with summaries, source references, and visible uncertainty.
- [Task and practice-area catalogue](https://github.com/legalcode-md/skills/blob/main/CATALOG.md).
- [Jurisdiction skills](https://github.com/legalcode-md/skills/tree/main/skills/jurisdictions).
- [General workflows](https://github.com/legalcode-md/skills/tree/main/skills/general).

Browse the full [Legalcode skill collection](https://github.com/legalcode-md/skills) and install
only the workflows you need. These optional skills are not bundled with this plugin; their
prerequisites and licenses apply separately.

## Data handling

Research sends Claude's selected tool arguments, such as search terms, jurisdiction, filters,
source identifiers, and requested text ranges, to the hosted Legalcode MCP service. The server
returns legal-source metadata and text. Patent Search and Patent Fetch use the external European
Patent Office service through Legalcode. Keep confidential matter details out of source queries
unless that disclosure is authorized and necessary.

This package contains the hosted connection and guide, with no executable helpers, local MCP
server, hooks, or document-upload workflow.

Privacy policy: [legalcode.md/privacy](https://legalcode.md/privacy).
Terms: [legalcode.md/terms](https://legalcode.md/terms).
Support: [legalcode.md/contact](https://legalcode.md/contact).

Published by **Fordæmi ehf.**, [legalcode.md](https://legalcode.md). The package and MCP guide
use the [MIT license](LICENSE). Verify legal conclusions against the underlying sources.
