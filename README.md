# Company Knowledge Assistant Demo

A demo for company decision makers showing how shared company knowledge can support answers, informed decisions, and approved actions.

**Current stage:** planning. The application and sample documents are planned; they have not been built yet.

## Planned walkthrough

1. Browse a fictional company's knowledge library.
2. Ask a question and inspect the answer's source evidence.
3. Review a suggested action and approve it.
4. See the decision in a shared log so colleagues can reuse the insight.

All demo documents, customers, and events will be fictional. Actions in the first demo will be simulated and recorded locally, with no real refunds, emails, or changes to client systems.

## Planned project structure

```text
frontend/              Browser interface; consider Sites when ready
backend/               API, approvals, and shared decision records
processing/            Document parsing, indexing, and retrieval
data/demo-documents/   Generated fictional knowledge sources
docs/                  Product brief and architecture notes
```

These directories will be added as each component is built. See [PLAN.md](PLAN.md) for the demo story, delivery sequence, and success criteria.

The first milestone is a working local proof of concept. A public source repository and a hosted client walkthrough are separate deliverables; hosting will be selected once the interface is ready.
