# Novastone evidence and answer checklist

Use this checklist to evaluate live RAG and label replay examples. It specifies supported claims and limits, not a single mandatory phrasing. Source section IDs appear in the Markdown documents and PDF pack; PDF page ranges are in the manifest.

| Question | Supported answer / decision | Required evidence |
|---|---|---|
| What changed in Q3 and did we hit revenue target? | Revenue £2.64m versus £2.40m (+10%); £240,000 short of £2.88m target (8.33% below). Margin 57% versus 61%, down 4 percentage points. Gross profit £1,504,800 versus £1,464,000. | NVS-003-S01/S02 |
| Which commercial line grew? | Kit revenue £1.44m to £1.68m; service revenue £0.96m both quarters. Pipeline is not revenue. | NVS-003-S01; NVS-004-S01/S03 |
| Why might repeat purchasing have weakened? | Slower delivery and unclear updates are plausible contributors; do not assert proved causality. Listening sample of 8 is not representative; reorder cohorts differ. | NVS-003-S03/S05; NVS-006-S01/S02/S03 |
| What were the late-order categories? | Supplier availability 7, release documentation queue 4, courier 3, incomplete PO 2; total 16 late of 100. Do not substitute the 28-lot denominator. | NVS-005-S01/S02 |
| Is the release problem's root cause confirmed? | No. QA-26-014 is open; proposal is not a validated fix. Preserve independent review. | NVS-013-S01/S03/S04 |
| Which improvement fits the available resources? | 6 discretionary specialist weeks; release project 4 + measurement/coordination 2 fits. Supplier option 6 or portal discovery 5 are alternatives, not simultaneous additions. No exact ROI claim. | NVS-007-S01/S02/S03; NVS-017-S02 |
| Who can approve the £18,000 project and release changes? | Daniel after Priya budget confirmation; Aisha independently accepts release-related change. Quality reporting is independent of Operations. | NVS-002-S01/S03; NVS-008-S02/S03; NVS-017-S03 |
| Did leadership already approve executing the improvement? | No. Meeting requested comparison; DEC-04 has no selected option or approver. ACT-02 is preparation. | NVS-010-S03/S04; NVS-019-S01; NVS-020-S01/S02 |
| Which October actions are outstanding, and who owns them? | ACT-02 Owen due 5 Oct, ACT-03 Nina 7 Oct, ACT-04 Tom 6 Oct, ACT-05 Maya review 6 Oct, ACT-06 Samir 8 Oct. ACT-01 completed. Snapshot as of 2 Oct. | NVS-019-S01/S02 |
| What is Novastone's Q4 revenue forecast or cash runway? | No approved Q4 forecast or runway provided; ask Finance. £780k quotations cannot answer this. | NVS-003-S05; NVS-004-S03; NVS-009-S03 |
| Why does an older document say revenue £2.88m? | It is an archived forecast/target, not actuals. Approved close on 2 Oct is £2.64m. | NVS-009-S01/S02; NVS-003-S01/S04 |
| Who should a new starter ask about kit, service, and quality questions? | Owen for kit scheduling, Samir for service timing, Aisha for Quality; Nina coordinates customer status and Grace approves messaging. | NVS-002-S02/S03; NVS-018-S01 |

## Acceptance criteria

Every numerical claim has a source reference and uses the correct period, denominator, unit, and actual/forecast distinction. Citations must resolve to the claimed section or PDF page. Do not show an invented confidence percentage. Label hypotheses and recommendations, give alternative options where relevant, and explicitly say when evidence is insufficient.

The recommended decision includes owner, budget condition, review date, Quality gate, and unresolved uncertainty. Only a demo human's recorded review can move a proposed decision to an approved state; imported meeting notes cannot perform that transition. Client live mode uses an access code; saved replay examples carry a replay label.

## Corpus checks performed by the generator

Checks cover revenue line totals, growth and target shortfall, headcount, delay counts, eligible-account ratios, resource allocation, valid cross-references, and extraction of every section ID from the PDF. PDF rendering is reviewed separately for layout quality. These checks validate the fictional corpus, not a RAG implementation that has yet to be built.
