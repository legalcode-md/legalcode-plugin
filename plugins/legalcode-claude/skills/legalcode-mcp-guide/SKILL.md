---
name: legalcode-mcp-guide
description: >
  Coordinate Legalcode's Discover, Search, Fetch, Patent Search, Patent Fetch, Analyze, and Trace tools for
  primary-source research. Use for capability questions, current source
  discovery, multi-tool research, aggregate analysis, relationship tracing,
  verified source text, or recovery from a rejected Legalcode call. Not for
  connection or installation setup.
---

# Legalcode MCP Guide

Use the connected schemas and the current `legalcode_discover` response as the contract for
parameters, fields, values, limits, and readiness. This guide adds only the cross-tool workflow and
handoffs that individual tool descriptions cannot express.

## Tool roles

| Tool | Purpose | What it hands to the next tool |
| --- | --- | --- |
| `legalcode_discover` | Learn the current shape of a jurisdiction and source family | searchable and filterable fields, facets, source codes, sorts, analytics readiness, and relationship coverage |
| `legalcode_search` | Find and rank candidate records | `sourceRef`, citation metadata, official URLs, snippets, and sometimes `downloadUrl` |
| `legalcode_fetch` | Verify one known record or provision | source metadata and the text needed to support a conclusion |
| `legalcode_patent_search` | Search live EPO patent publications | patent metadata, publication identifiers, source links, and exact `sourceRef` handles |
| `legalcode_patent_fetch` | Retrieve one exact patent publication | source metadata and available claims or description text |
| `legalcode_analyze` | Count or group a defined indexed cohort | buckets, measures, and document handles when that profile permits them |
| `legalcode_trace` | Follow a persisted legal relationship | related-record handles and, for legislative history, flow handles |

Search discovers records; Fetch verifies their text; Analyze measures a cohort; Trace follows known
edges. Do not use Search-result counts as analytics or Trace edges as a substitute for reading the
underlying source.

## Discover the shape first

For each new indexed jurisdiction and source family in a research task, call Discover `source_profile`
before the first Search, Analyze, or Trace. It establishes what the current corpus actually
supports. Use `facet_values` when an exact stored filter value is needed. Never guess a
`sourceCode`, field, facet value, analytics dimension, measure, or relationship capability.

Reuse a current profile already present in the conversation; do not repeat Discover for every call
within the same scope. Fetching a returned `sourceRef` and continuing a cursor-paginated call do not
need another discovery step.

Patents use their own tool schema. They are not a Discovery source family and are not accepted by
generic Search or Fetch. Use `legalcode_patent_search` and `legalcode_patent_fetch` directly for patent research.
If that tool or a described parameter is absent from the connected schema, report the capability
as unavailable in this connection. Package instructions cannot enable an unapproved tool update.

## Search from most specific to least specific

1. Use an exact identifier or identifier filter when the authority is known.
2. Add structured filters advertised by Discover when the requested scope is known.
3. Use phrase mode when every meaningful term must occur together.
4. Use source-language keyword text for open-ended topic discovery.

Free text never creates jurisdiction, source-type, court, date, or other structured constraints.
Put those in explicit parameters. If a filter is rejected, correct it through Discover rather than
silently dropping it and broadening the question.

## Cross-tool handoffs

- **Candidate to evidence:** Discover → Search → Fetch. Copy the returned `sourceRef` exactly;
  never construct or decode it.
- **Aggregate to documents:** Discover → Analyze → Search → Fetch. Search the same jurisdiction,
  `q`, and every filter that Discover marks valid for Search; do not replace the analyzed cohort
  with a looser paraphrase.
- **Authority to related authorities:** Discover first. Then Search to resolve an uncertain
  authority, or pass a certain exact identifier directly to Trace. Fetch material targets. Trace
  starting inputs are relationship-specific; follow the connected schema rather than assuming one
  identifier works for every relationship.
- **Legislative history:** Discover → Search the enacted law → Trace its pre-law relationship →
  use each returned `flowKey` in a document-level pre-law Search → Fetch or download the relevant
  documents.
- **Complete text:** Prefer a returned `downloadUrl`; otherwise use Fetch full-text pagination and
  keep the source, mode, and cursor scope unchanged.
- **Cross-jurisdiction work:** repeat Discover and research separately for each jurisdiction, then
  normalize the comparison in the answer.

## Patent publications

Use `legalcode_patent_search` with an explicit `jurisdiction`. Use `patentId`
for an exact publication, including its kind code, or supported applicant, inventor, office, and
publication-date constraints for a defined search. Each page returns at most 20 results; only the
first 2,000 provider results can be paged. Continue using the returned cursor and preserve every
search constraint. An unsupported jurisdiction needs an explicit supported office; never broaden
it silently to all offices.

Copy the returned patent `sourceRef` exactly into `legalcode_patent_fetch`. Neither patent tool accepts an `action` dispatcher.
Metadata, excerpt, and full modes describe the requested retrieval; follow text continuations
without changing the publication or mode. Search-only inputs do not belong in a Fetch request.
Available metadata or a publisher link does not prove that description or claims text was
retrieved. Report body availability, provider failures, and incomplete text explicitly. The tool
reads the external EPO service, so results and availability may vary between requests.

## Parliamentary entries and exact versions

Alþingi bill proceedings use `pre_law`; other parliamentary records use `public_record`.
Discover the exact source and readiness before choosing fields. Use explicit session, matter,
document, person, role, stage, outcome, subject, and date filters only when the profile advertises
them. Generic query text never adds those constraints.

Where supported, Search `resultLevel:"event"` or `"participant"` returns an independently
fetchable entry and its parent reference. A participant entry represents a participation or role
assignment, which may be a speaker, voter, or dated office or membership assignment. It is not
necessarily a distinct person. Keep conditions intended for one assignment or event together.
For historical roles, use the supported temporal operators; uncertain dates do not establish
definite membership on a date.

Fetch parent context through `publicRecordContext` with kind `participants`, `events`, or
`relations`. Follow the context cursor separately from body-text pagination. Preserve exact
document numbers, manifestation or revision identity, transcript status, and proposal versus
adopted-document identity. Count records, documents, events, assignments, ballots, and people
only with the measures and definitions advertised by the current analytics profile. Native ballot
actions remain distinct, and overlapping groups need not add to a corpus total.

For planned versus actual proceedings, retrieve both the agenda and the journal, then follow
relevant event and relation context pages to the proceeding, speech, vote, and final document.
An agenda stage shows a plan; a proceeding start, vote time, and final disposition are separate
observations. Verify the source marker and timestamp for each assertion. Retrieve the vote's
native ballot evidence when a roll call or outcome is required; a meeting summary alone does not
establish it. Treat announced starts separately from supported actual opening and closing times.

When Fetch returns a manifestation inventory handle, follow that exact handle and its continuation
to select the required representation or acquisition revision. Continue its pagination independently
of text and parent-context cursors. An archived acquisition is not proof of the publisher's complete
revision history or original publication date. Source links, structured metadata, reduced extraction,
and a complete stored XML body are different availability states; preserve the reported limits.

For a last-three or last-four amendment request, establish the cutoff, qualifying amendment
relationships, and exact versions. Adoption, publication, and commencement are different dates.
Fetch the amendment evidence and relevant versions; latest consolidated text alone cannot
establish the requested changes. If the indexed chain or a document body is incomplete, state
which required evidence was not retrieved rather than asserting completeness.

See [validated call examples](references/tool-examples.json) for argument shapes. Replace example
handles with values returned by the connected tools, and check readiness before executing an
analytics example.

## Trace starting points

Trace inputs depend on the selected relationship:

| Relationship | Valid starting point |
| --- | --- |
| `cases_for_law` | `lawKey`, `legalBasisKey`, citation, or law `sourceRef` |
| `laws_for_case` | case `sourceRef` |
| `cited_cases` | case `sourceRef` |
| `citing_cases` | case `sourceRef` or citation |
| `pre_law_for_law` | `lawKey`, `legalBasisKey`, `relatedNumberYear`, or law `sourceRef` |
| `related_pre_law_flows` | `lawKey`, law `sourceRef`, `flowKey`, or EU pre-law `sourceRef` |
| `eea_incorporation_for_law` | EU `lawKey`, `legalBasisKey`, citation or CELEX, or `sourceRef` |
| `implementing_laws_for_eu_law` | the same EU identifiers plus the required national `jurisdiction` |
| `eu_law_for_implementing_law` | national `lawKey`, `legalBasisKey`, citation, or `sourceRef`; add national `jurisdiction` when it cannot be inferred |

## Evidence and reader-facing output

Search snippets identify candidates, not proof. Fetch the relevant provision or passage before
making a material legal claim. Analyze reports indexed counts under the applied scope; Trace reports
indexed relationships. Neither establishes causation, legal effect, or complete real-world
coverage, so preserve material coverage warnings.

Keep `sourceRef`, `lawKey`, `flowKey`, `sourceCode`, relationship names, metric keys, and field names
inside tool calls. In ordinary answers, use titles, legal citations, decision numbers, courts or
issuing bodies, dates, provision locators, and official URLs. Show raw machine vocabulary only when
the user explicitly asks for technical or machine-readable output.

## Bundled document workflows and the wider collection

- Use the bundled `legalcode-document-to-skill` when the user wants a reusable drafting skill
  from example Word or PowerPoint documents. Read its entrypoint and supporting references;
  preserve the approved design and keep private source documents out of shared packages.
- Use the bundled `legalcode-tabulate` when the user wants a traceable workbook from supplied
  documents. Read its entrypoint and runtime guidance; preserve per-cell source evidence,
  uncertainty, and the distinction between extracted facts and assessment.
- For additional jurisdiction, practice-area, or task workflows, consult the
  [Legalcode skill collection](https://github.com/legalcode-md/skills),
  [task and practice-area catalogue](https://github.com/legalcode-md/skills/blob/main/CATALOG.md),
  [general workflows](https://github.com/legalcode-md/skills/tree/main/skills/general), and
  [jurisdiction workflows](https://github.com/legalcode-md/skills/tree/main/skills/jurisdictions).
  Read the selected skill and its prerequisites before use. Collection links do not mean the
  whole collection is installed. Install additional skills only when the user authorizes it.
  A jurisdiction skill does not establish current source coverage; check Discover for the matter.
