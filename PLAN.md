# Company Knowledge Assistant Demo — Plan

## Goal

Show company decision makers how a knowledge assistant can make company knowledge easier to find, ground answers in approved sources, and support accountable actions. The demo should make shared understanding and informed decisions visible, not just show a chat box.

## Demo story

Use a fictional company and generated documents throughout. A support teammate asks how to handle a customer request. The assistant answers from current company policy, links each important claim to its source, flags any uncertainty or conflicting guidance, and proposes an action. A human reviews and approves the action. The resulting decision appears in a shared activity or decision log so other teams can learn from it.

## Main screens and workflow

1. **Overview:** Show the knowledge base's document count and freshness, recent questions, decisions awaiting review, and a small feed of shared insights.
2. **Ask:** Let a user ask a question and see a concise answer, source excerpts with document/page references, and a clear confidence or evidence state.
3. **Knowledge library:** Show generated policy and process documents with owner, status, version/date, and processing state. Include a simple add-document flow for the demo.
4. **Proposed action:** Present a suggested support action with its policy basis. Require a person to approve before marking it complete; record who approved it and why.
5. **Decision log:** Show the question, cited evidence, chosen action, reviewer, and timestamp so the result is reusable by colleagues.

## Generated demo data

Create a small, internally consistent fictional document set: customer refund policy, support escalation guide, product incident runbook, and a short company operating-principles document. Include dates, owners, and versions. Add one deliberately outdated policy or a known policy conflict to demonstrate that the assistant can surface uncertainty instead of silently combining incompatible guidance. Keep all names, customers, and events fictional.

## Technical organization

Keep the browser interface, Python API, and document/RAG processing as separate modules in one repository. Organize the repo around `frontend/` (interface), `backend/` (API and action/decision records), `processing/` (document parsing, indexing, retrieval), `data/demo-documents/` (fictional sources), and `docs/` (product and architecture notes). Expose API boundaries for document listing/ingestion, question answering with citations, and proposed/approved actions. Use seeded local demo data so the walkthrough works without private company files. Keep model/provider configuration outside source control and document the local setup.

Use a concise product brief and one architecture note (or ADR) rather than a large SDD package. Add focused tests around the important contracts: document metadata survives ingestion, answers return source references, unsupported questions are marked as such, and actions cannot be recorded as approved without a reviewer decision. TDD can be used for these behaviors without maintaining a separate TDD document.

## Delivery sequence

1. Create the public repository and commit this plan and a short README.
2. Generate the fictional document set and define its expected questions, citations, and one uncertainty case.
3. Build the backend ingestion and retrieval path, then the answer/citation and approval-action APIs.
4. Build the interface around the five-screen walkthrough and connect it to the API.
5. Verify the walkthrough from a clean setup, add run instructions, and decide whether Sites is a suitable hosting/presentation layer for the finished interface.

## Success criteria

- A decision maker can understand the value in a short guided walkthrough without reading implementation details.
- Answers show inspectable source evidence and clearly handle missing or conflicting evidence.
- A suggested action waits for human approval and the approved decision is visible to colleagues.
- The demo runs from generated data, with setup instructions and a public repository that contains no real company data or secrets.

## Working defaults

- Public repository: `DrZiwei/Company-RAG-demo-test`.
- Audience: company decision makers.
- Data: generated fictional policies and operational documents only.
- First release: a working local proof of concept with a polished walkthrough; consider Sites for hosting after the interface is ready.
- GitHub visibility: public, as requested.
