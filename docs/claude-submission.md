# Claude Plugin Directory submission

Updated 2026-10-15 for Claude package **1.4.0**.

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
- Short description: Primary-source legal research with verified citations.

Legalcode connects Claude to primary legal materials through an authenticated, read-only MCP
server. The included guide coordinates seven research tools and keeps conclusions tied to
verified source text, citations, and official links. The package contains only the MCP connection
and research guide, with links to separately installable Document-to-skill, Tabulate, jurisdiction,
practice-area, and task skills.

## Data handling and reviewer setup

The plugin README describes the connector's outbound query data and EPO patent access.
Use that disclosure when completing the portal's data-handling step.
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

The Claude package contains one guide skill, its call examples and license, the hosted MCP
configuration, listing metadata, README, and icon. It contains no executable helpers or extra
workflow packages. Additional skill links remain references for separate installation.
