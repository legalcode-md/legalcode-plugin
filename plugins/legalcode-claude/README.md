# Legalcode for Claude

Research primary legal sources, turn Word and PowerPoint precedents into reusable drafting
skills, and turn document collections into traceable Excel workbooks.

## Included skills

| Skill | What it does |
| --- | --- |
| `legalcode-mcp-guide` | Coordinates Discover, Search, Fetch, Patent Search, Patent Fetch, Analyze, and Trace. Verifies source text and preserves citations, exact identities, scope, and coverage limits. |
| `legalcode-document-to-skill` | Builds a reusable drafting skill from example DOCX or PPTX documents, preserving house style, backgrounds, colors, fonts, layouts, and approved assets while removing matter-specific content. Includes the complete local inspection and template helpers. |
| `legalcode-tabulate` | Infers useful fields from supplied documents and produces a traceable Excel workbook with a summary, topic-specific sheets, source locations, and visible uncertainty. |

Try asking Claude to:

- Research an Icelandic legal issue using current legislation and case law, with verified citations.
- Turn these Word or PowerPoint examples into a reusable drafting skill that preserves our house style.
- Turn these documents into an Excel workbook with a summary and evidence for each finding.

The Tabulate workflow is written in Icelandic; request the workbook language you need.
Document and spreadsheet generation requires suitable tools in the host app. The bundled DOCX
and PPTX helpers use Python 3.9+ and its standard library; see each skill's runtime guidance.

## More skills by jurisdiction and task

The [Legalcode skill collection](https://github.com/legalcode-md/skills) contains **327 skills**
across **18 jurisdiction groups** and **15 practice areas**. Browse the
[task and practice-area catalogue](https://github.com/legalcode-md/skills/blob/main/CATALOG.md),
[general workflows](https://github.com/legalcode-md/skills/tree/main/skills/general), or
[jurisdiction workflows](https://github.com/legalcode-md/skills/tree/main/skills/jurisdictions).
Add the workflows relevant to your matter; the wider collection is available separately.
Read each skill's prerequisites and license before installing or redistributing it.

## Install and connect

In Claude Code:

```text
/plugin install legalcode --marketplace legalcode-md/legalcode-plugin
```

In Claude and Cowork, add this repository as a marketplace from Customize > Plugins, then
select Legalcode. The bundled remote connector is `https://mcp.legalcode.md/mcp`.
Connect it through the plugin's Connectors tab and complete Legalcode authentication.
Source availability, account permissions, and patent-provider availability can vary;
the guide checks the connected schemas and current source coverage before research.

## Data handling

Legal research sends the tool arguments Claude selects, including search terms, jurisdiction,
filters, source identifiers, and requested text ranges, to the hosted Legalcode MCP service.
Patent Search and Patent Fetch use the external European Patent Office service through Legalcode.
The server returns legal-source metadata and text. Keep confidential matter details out of
source queries unless that disclosure is authorized and necessary.

Document-to-skill and Tabulate read the documents the user supplies to Claude. The bundled
Python helpers inspect and generate local files without network access. The plugin does not
automatically upload those documents to Legalcode or any other service. Research that supports
a document may send a minimized legal query through the connector; external OCR or other
services need authorization. Handling of documents within Claude is governed by the user's
Claude plan and settings. Optional runtime setup or documentation lookup may contact the
software provider or documentation site described in the skill's runtime references.

Privacy policy: [legalcode.md/privacy](https://legalcode.md/privacy).
Terms: [legalcode.md/terms](https://legalcode.md/terms).
Support: [legalcode.md/contact](https://legalcode.md/contact).

## Publisher, licenses, and provenance

Published by **Fordæmi ehf.**, [legalcode.md](https://legalcode.md).
Document-to-skill, Tabulate, and their supporting files retain the
[Legalcode Skills Source-Available License 1.0](LICENSE.md). The MCP guide retains its
[MIT license](skills/legalcode-mcp-guide/LICENSE). These are separate grants; the repository's
MIT license does not relicense the source-available skills.

The bundled workflow packages are copied in full from the published skill collection.
[skills-provenance.json](skills-provenance.json) records the exact source commit and file hashes.
Coverage and legal accuracy still require verification for each matter.
