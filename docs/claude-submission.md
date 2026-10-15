# Claude Plugin Directory submission

Updated 2026-10-15 for Claude package **1.3.2**.

## Source step

- Portal: https://claude.ai/directory/manage/new/plugin
- Repository: `https://github.com/legalcode-md/legalcode-plugin`
- Plugin path: `plugins/legalcode-claude`
- Branch: `main` (the default branch)
- Direct folder link: https://github.com/legalcode-md/legalcode-plugin/tree/main/plugins/legalcode-claude

The portal accepts the direct folder link and fills the path and branch. Select **Validate**
and resolve blocking findings before continuing. A local validation pass does not establish
portal acceptance. The directory tracks new commits on the selected branch and scans updates.
Existing submissions and reviewer feedback are available at https://claude.ai/directory/manage.

Official instructions: https://claude.com/docs/plugins/submit and
https://claude.com/docs/plugins/pre-submission-checklist.

## Listing copy

- Display name: Legalcode
- Publisher: Fordæmi ehf.
- Website: https://legalcode.md
- Support: https://legalcode.md/contact
- Privacy: https://legalcode.md/privacy
- Terms: https://legalcode.md/terms
- Short description: Legal research, reusable drafting skills, and traceable document tables.

Legalcode connects Claude to primary legal materials through an authenticated, read-only MCP
server. The included guide coordinates seven research tools and keeps conclusions tied to
verified source text, citations, and official links. Document-to-skill turns Word and PowerPoint
examples into reusable drafting skills while preserving house style. Tabulate turns document
collections into traceable Excel workbooks with summaries and visible uncertainty. The package
links to the wider Legalcode collection of jurisdiction, practice-area, and task skills.

## Data handling and reviewer setup

The plugin README describes the connector's outbound data, EPO patent access, local document
helpers, optional runtime setup, and the distinction between Claude's document handling and
Legalcode queries. Use that disclosure when completing the portal's data-handling step.
Complete client-managed authentication at `https://mcp.legalcode.md/mcp` using a Legalcode account.
Provide reviewer credentials only in private submission fields.

## Validation and maintenance

```sh
claude plugin validate plugins/legalcode-claude --strict
claude plugin validate .claude-plugin/marketplace.json --strict
uv run --python 3.13 --with-requirements requirements-dev.txt python scripts/validate_claude_package.py
```

The Claude and OpenAI packages release independently. The Claude guide follows the current
seven-tool endpoint; the submitted OpenAI package retains its existing six-tool guide until
its separate update. Each package's tests enforce its own inventory and guide contract.
The hosted endpoint is shared. Do not use the retired CLI repository as this submission's source.

When refreshing bundled workflow skills, copy complete committed packages from
https://github.com/legalcode-md/skills, verify each file against that commit's catalog.json,
and update skills-provenance.json. Retain each package's license and rerun validation.
Do not copy unrelated, uncommitted work from the skills checkout into a release.
