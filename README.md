# Company Knowledge and AI Assistant

A decision-maker demo for **Novastone**, a fictional bioscience company supplying research-use assay kits and analytical services. It shows how shared company knowledge supports a business review, evidence-backed recommendations, and accountable actions.

**Current stage:** source documents and the walkthrough are ready; the RAG backend and interface are not implemented yet.

## Explore the demo materials

- [20 fictional company documents and provenance manifest](data/demo-documents/novastone/)
- [Readable 22-page PDF pack](output/pdf/novastone-company-knowledge-pack.pdf)
- [Downloadable source pack](novastone-demo-pack.zip)
- [Business-review walkthrough](WALKTHROUGH.md)
- [Questions, expected evidence, and answer limits](EVALUATION.md)
- [Project plan](PLAN.md)

The documents include an org chart, finance/KPI review, leadership meeting, operations meeting, lab stand-up, supplier review, customer listening notes, project update, Quality investigation, onboarding notes, and shared action/decision logs. Dates, versions, owners, statuses, and references make cross-document questions possible. All names, numbers, and events are invented and do not describe any actual business using the name Novastone.

## Demonstration story

Understand why revenue growth coexists with delivery, margin, and repeat-order problems; inspect evidence and unknowns; compare improvements against available capacity; review and record a simulated decision. Live AI will use a client access code; saved presentation examples will be labelled as replay.

## Planned application structure

```text
frontend/              Management interface; consider Sites when ready
backend/               API, approvals, and shared decision records
processing/            Document parsing, indexing, and retrieval
data/demo-documents/   Fictional source files and manifest
output/pdf/            Readable source pack
tools/                 Reproducible corpus generator
```

To regenerate the corpus and PDF, run `python tools/generate_novastone_pack.py` with `reportlab` and `pypdf` installed. The generator checks numerical reconciliation, cross-references, and extractable source section IDs. It does not run an AI service.

Future document creation, connected meeting capture, and scheduled automation are planned on [plan/document-services](https://github.com/DrZiwei/Company-RAG-demo-test/tree/plan/document-services).
