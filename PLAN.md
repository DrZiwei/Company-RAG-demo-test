# Company Knowledge and AI Assistant - Novastone demo

## Goal and audience

Help company decision makers review performance, inspect evidence, compare feasible actions, and share accountable decisions. Novastone is a fictional bioscience company supplying research-use assay kits and analytical services. All people, records, suppliers, customers, and figures are synthetic.

## Current milestone

The source corpus is ready: 20 everyday and management documents, a source manifest with stable section IDs and PDF page ranges, and a 22-page readable PDF pack. The application has not been built. See [WALKTHROUGH.md](WALKTHROUGH.md) for the presentation and [EVALUATION.md](EVALUATION.md) for questions, evidence, and answer limits.

## Business-review story

At the Q3 2026 review, revenue grew 10% but missed target; margin, delivery, repeat purchasing, and service turnaround weakened. Leaders investigate the evidence and compare release-record improvements, alternate-supplier assessment, and customer-status portal discovery against six available specialist weeks. They review a proposed decision, identify owner and approval conditions, and record the result in a shared log.

Answers distinguish observations from causes, actuals from archived forecasts, and discussion/draft proposals from approved decisions. New decisions entered during the demo are stored separately from the imported baseline corpus.

## Interface and data boundaries

Plan a management overview, knowledge library, cited Q&A, option/decision review, and shared action/decision history. Offer live AI behind a client demo access code and clearly labelled replay examples for presentations. Keep API credentials server-side and enforce usage limits.

Keep the interface in `frontend/`, API and decision records in `backend/`, and document parsing/indexing/retrieval in `processing/`. Sources live in `data/demo-documents/novastone/`; the readable pack lives in `output/pdf/`. A source manifest carries owner, date, status, version, and section/page references. Audience labels in these synthetic files are metadata, not implemented access controls.

## Next implementation milestones

1. Specify APIs, source/answer/decision contracts, AI-provider setup, and hosted architecture in one technical design note. Evaluate Sites for the interface against backend needs.
2. Implement ingestion and cited answers, including stale and insufficient evidence, and verify against EVALUATION.md.
3. Implement client access, management interface, labelled replay, and approval-based simulated decisions.
4. Verify the full walkthrough from a clean setup and publish a shared client URL. The source repository is available; hosting is a separate milestone.

## Future workstream

Document drafting, meeting assistants, automatic folder ingestion, and scheduled follow-ups remain on [plan/document-services](https://github.com/DrZiwei/Company-RAG-demo-test/tree/plan/document-services). The source pack's meeting and action records can support that later walkthrough.

## Defaults

English interface and documents; public repository `DrZiwei/Company-RAG-demo-test`; fictional data only; live AI with replay; client live access via demo code; first-release actions are simulated. Use a concise product brief, one technical design document, and an evaluation checklist.
