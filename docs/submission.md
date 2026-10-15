# OpenAI Plugins Directory submission

## Final listing

- Name: Legalcode
- Version: 1.2.3
- Subtitle: Legal research for business
- Category: Business & Operations
- Developer identity: verified Fordæmi ehf.
- Plugin author: Fordæmi ehf.
- Website: https://legalcode.md
- Customer support: https://legalcode.md/contact
- Privacy policy: https://legalcode.md/privacy
- Terms of service: https://legalcode.md/terms
- MCP type: Universal
- MCP URL: https://mcp.legalcode.md/mcp
- Commerce and purchasing: unchecked
- Custom UI, screenshots, and CSP: none
- Plugin repository: https://github.com/legalcode-md/legalcode-plugin
- Included skill: legalcode-mcp-guide

Description:

> Research primary legal sources for business, compliance and professional legal work. Find legislation, court decisions, legislative history and patents; retrieve available text, compare exact versions, count indexed records and follow verified relationships. Where coverage supports it, research parliamentary documents, speeches, votes, events and historical roles. Results include source identities and links so you can verify the evidence. Coverage and text availability vary by jurisdiction and source.

Starter prompts:

1. Research an Icelandic legal issue using current legislation and case law.
2. Find EU legislation and decisions, then trace national implementation measures.
3. Find European patent EP4811984A1 and verify its published claims.

Release notes:

> Version 1.2.3 updates the canonical repository to legalcode-md/legalcode-plugin. The research guide, six-tool submission contract, category and hosted MCP connection are unchanged.

Submission assets:

- Directory icon: plugins/legalcode-openai/assets/legalcode-directory-256.png
- Composer icon: plugins/legalcode-openai/assets/legalcode-composer-48.png
- Local submission worksheet: chatgpt-app-submission.json

`chatgpt-app-submission.json` is hand-maintained at the repository root; no script generates it.
Use it to keep the listing metadata, tool annotations, five positive cases, and three negative cases
consistent while completing the OpenAI submission portal. The manifest imports review cases from the package. The portal retains reviewer access and the demo video separately; private credentials are never included in this worksheet or ZIP.

## MCP contract

The submission advertises exactly:

1. legalcode_discover
2. legalcode_search
3. legalcode_fetch
4. legalcode_patents
5. legalcode_analyze
6. legalcode_trace

Every tool declares OAuth with legalcode.public.read, legalcode.laws.read, and legalcode.cases.read. The six research tools only retrieve or compute legal information and cannot change legal materials, relationships, user content, or public or external systems, so the annotations are:

- readOnlyHint: true
- openWorldHint: false for corpus tools; true for Patents because it reads the external EPO service
- destructiveHint: false
- idempotentHint: true

The tools cannot alter, publish, send, file, purchase, or delete legal materials or user content. Retired names remain hidden compatibility aliases and must not appear in tools/list.

The OAuth server uses dynamic client registration and PKCE S256. Do not enter a static client ID. OpenAI callback URLs are registered dynamically. UserInfo is https://mcp.legalcode.md/oauth/userinfo and returns only sub, email, and email_verified.

## Reviewer access

Create one dedicated reviewer user with stable Pro entitlements. The fixed-OTP allowlist must suppress email delivery. Put the reviewer email and fixed code only in the portal’s private reviewer fields. Do not commit either value. The account must require no mailbox access, MFA, SMS, invitation, or private network.

Before submission, create a completely fresh ChatGPT Developer Mode connection and complete dynamic registration, authorization, token exchange, UserInfo, tool listing, and calls.

## Required evaluation cases

### Positive

1. Discover and compare current source coverage for Iceland, the European Union, and the United States.
2. Search European patent EP4811984A1, retrieve that same publication, and verify its available claims with the source link.
3. Resolve GDPR by CELEX, then fetch and explain Article 22 with an official EUR-Lex link.
4. Analyze Icelandic Data Protection Authority decisions from 2018 through 2025, then search and fetch the two newest records from the identical cohort.
5. Resolve Icelandic Act No. 90/2018, trace its original legislative matter, enumerate submitted opinions, and fetch the committee report.

Every prompt is reader-facing. Search or Trace supplies Fetch with the opaque record handle inside the
tool workflow; reviewers are never asked to construct or type one.

### Negative

1. Do not invoke Legalcode to file a pleading.
2. Do not invoke Legalcode for a self-contained contract edit that requires no source research.
3. Do not invoke Legalcode to draft routine legal correspondence that requires no source research.

## Demo recording

Record a reviewer-accessible demonstration of:

- account linking;
- all six MCP tools;
- the MCP tool-guide explaining supported capabilities;
- one uploaded-document workflow;
- citation verification;
- one unsupported external-action request.

Cover the web, iOS, and Android experiences requested by the portal. Show no checkout or upgrade direction.

## Production evidence gate

The production host must set OPENAI_APPS_CHALLENGE_TOKEN to the value generated by Apps Management. GET https://mcp.legalcode.md/.well-known/openai-apps-challenge must return that exact value as text/plain with no wrapper. It returns 404 while unset.

Before clicking Submit:

1. Verify OAuth and OpenID discovery, UserInfo, protected-resource metadata, server card, challenge route, and authenticated tools/list.
2. Run MCP Inspector against https://mcp.legalcode.md/mcp.
3. Run all five positive and three negative tests from a fresh connection.
4. Confirm telemetry shows successful registration, authorization, token exchange, and tool calls with no invalid_client, invalid_redirect_uri, or tool_not_found events.
5. Copy the validated worksheet values into the portal, enter all five positive and three negative
   cases, and provide both icons, the one-skill bundle, reviewer credentials, and demo URL.
6. Select the verified Fordæmi ehf. identity.
7. Submit only after Scan Tools is clean.

Publication and identity selection remain manual portal actions.

## Version 1.2.2 package update

Upload `dist/legalcode-openai-1.2.2.zip` to the existing Legalcode plugin after the
scoped runtime release is verified. The package keeps the existing identity,
Business & Operations category, MCP connection and six-tool schema. The shared
OpenAI/Claude guide now explains agenda versus journal evidence, scheduled versus
actual times, separate vote and disposition evidence, and exact manifestation
pagination. Availability still depends on the connected source's Discovery profile.
Package conformance does not establish completed history or deployed tool readiness.

## Version 1.2.1 package update

Upload `dist/legalcode-openai-1.2.1.zip` to the existing Legalcode plugin. Its manifest name is the
assigned dashboard identity `app-6a5fc36564608191827f4e7716bdaba0`; its display name remains Legalcode.
The ZIP preserves the MCP endpoint and imports updated listing metadata, one guide skill, five positive
and three negative review cases. Customer support metadata is included. Existing country targeting
and the saved demo URL are preserved by omission. This package does not bypass held MCP tool
updates: inspect their findings, rescan or appeal through the separate MCP review panel.

## Version 1.2.3 repository update

The public repository is now https://github.com/legalcode-md/legalcode-plugin.
Use `dist/legalcode-openai-1.2.3.zip` for the metadata update; the MCP connection and guide are unchanged.
