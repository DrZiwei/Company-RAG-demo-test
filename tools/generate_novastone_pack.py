"""Build the fictional Novastone corpus, provenance manifest, and readable PDF.

Uses bundled reportlab/pypdf. Content is fictional; no scientific procedures or
real company records are included. Run from the repository root.
"""
from pathlib import Path
import hashlib
import json
import re
import zipfile
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Flowable
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/demo-documents/novastone'
OUT = ROOT / 'output/pdf'
SOURCE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

# ID, filename, title, kind, owner, date, status, sections.
DOCS = [
('NVS-001', 'company-profile', 'Company profile and operating model', 'company profile', 'Maya Chen, CEO', '2026-09-30', 'current', [
('Business', 'Novastone is a fictional Cambridge-based bioscience company with 60 employees. It supplies research-use-only biomarker assay kits and contract analytical services to university laboratories and biotechnology research teams. Its two commercial lines are Atlas research assay kits and Stonebridge analytical services. These products are not intended for clinical diagnosis; this pack describes business operations, not laboratory methods.'),
('Operating model', 'Sales receives customer purchase orders. Commercial operations checks scope and documentation, then coordinates with production for kits or laboratory services for analytical work. Quality independently reviews applicable release records. Finance recognises product revenue on dispatch and service revenue when the agreed deliverable is accepted. Quotes and bookings are not recognised revenue.'),
('Review context', 'The Q3 business review covers 1 July to 30 September 2026. Revenue increased, but service delivery and repeat purchasing weakened. Leaders must choose a feasible October improvement using the capacity in NVS-007, current actuals in NVS-003, and customer evidence in NVS-006.'),
('Company boundaries', 'All people, customers, suppliers, projects, figures, and events in this pack are invented. Novastone is a fictional scenario, with no claim about any real business using the same name. GBP amounts exclude VAT. Working-day turnaround measures exclude weekends and UK public holidays; no individual calendar calculation is required for the demo.')]),
('NVS-002', 'org-chart-and-responsibilities', 'Organisation chart and decision responsibilities', 'org chart / RACI', 'Leah Morgan, People and Operations', '2026-10-01', 'current', [
('Organisation chart', 'Maya Chen - Chief Executive Officer (CEO)\n  Priya Shah - Chief Financial Officer (CFO); Finance and People, 8 staff\n  Daniel Brooks - Chief Operating Officer (COO); Production and Supply Chain, 14 staff\n  Dr Elena Ruiz - Chief Scientific Officer (CSO); R&D and Laboratory Services, 19 staff\n  Grace Okafor - Head of Commercial; Sales and Customer Success, 12 staff\n  Dr Aisha Patel - Head of Quality; Quality and Regulatory Operations, 6 staff\nCEO: 1 staff. Total headcount: 1 + 8 + 14 + 19 + 12 + 6 = 60. Quality reports to the CEO, independently of Operations.'),
('Working contacts', 'Leah Morgan leads People within Priya\'s group. Owen Reed is the Production Lead under Daniel. Dr Samir Khan leads Laboratory Services under Elena. Nina Ellis is the Customer Success Manager under Grace. Tom Bell is the Supply Chain Manager under Daniel. Job titles identify owners even if a person is absent; there are no real contact details in the demo.'),
('Responsibility matrix', 'Quarterly figures: Priya accountable; Finance prepares; Commercial and Operations consulted. Production improvements: Daniel accountable; Owen delivers; Aisha reviews quality implications. Scientific claims and service scope: Elena accountable. Customer communications: Grace accountable; Nina drafts; Quality consulted on product or release statements. Quality release decisions: Aisha accountable; Operations supplies evidence, but cannot overrule Quality.'),
('Escalation', 'A customer-impacting delay goes to the relevant operating owner and Nina. A quality concern goes directly to Aisha. Resource allocation across functions is reviewed by Maya after Daniel, Elena, and Priya assess the proposal. Spending authority is defined in NVS-008; owning an action does not imply authority to approve its expenditure.')]),
('NVS-003', 'q3-finance-and-kpi-review', 'Q3 2026 finance and KPI review', 'management report', 'Priya Shah, CFO', '2026-10-02', 'approved', [
('Revenue and margin', 'Q2 recognised revenue was GBP 2,400,000: Atlas kits GBP 1,440,000 and Stonebridge services GBP 960,000. Q3 recognised revenue was GBP 2,640,000: kits GBP 1,680,000 and services GBP 960,000. The Q3 revenue target was GBP 2,880,000. Revenue therefore grew 10% quarter on quarter and missed target by GBP 240,000 (8.33% of target). Targets are management goals, not another source of actual revenue.'),
('Gross profit', 'Q2 gross margin was 61%, producing GBP 1,464,000 gross profit. Q3 gross margin was 57%, producing GBP 1,504,800 gross profit. The Q3 margin target was 60%. Revenue rose faster than gross profit, while margin fell by four percentage points. Higher expedited shipping and production rework are reported cost pressures; their exact separate contributions have not yet been reconciled by Finance.'),
('Operating KPIs', 'Q2 on-time shipment: 94 of 100 due orders (94%). Q3: 84 of 100 due orders (84%), against a 95% target. Customer reorder rate: Q2 41 of 50 eligible accounts (82%); Q3 36 of 50 (72%), against an 85% target. These are separate quarterly cohorts, not a longitudinal customer churn calculation. Service turnaround: Q2 average 8 working days; Q3 average 12, against an 8-day target.'),
('Definitions and close', 'Recognised revenue follows NVS-001. Gross margin = (revenue minus cost of sales) / revenue. On-time shipment counts dispatch by the customer-confirmed date, not arrival. Reorder rate measures eligible accounts placing at least one repeat order in the quarter; eligibility is defined before the period closes. Turnaround is from complete sample receipt/documentation to delivery of the agreed report. This approved close supersedes the preliminary Q3 flash figures discussed in NVS-010; figures happen to match after reconciliation.'),
('Interpretation limits', 'NVS-005 supports shipment-delay categories; NVS-006 provides qualitative customer feedback. Neither proves that delays caused the reorder decline. Product mix, purchase cycles, and budget timing may also contribute. This pack does not supply net profit, cash runway, individual customer contracts, exact intervention ROI, or a completed Q4 forecast.')]),
('NVS-004', 'commercial-pipeline-update', 'Commercial pipeline and customer commitments', 'commercial update', 'Grace Okafor, Head of Commercial', '2026-09-30', 'current', [
('Quarter close', 'Atlas recognised kit revenue increased from GBP 1.44m to GBP 1.68m. Stonebridge recognised service revenue remained GBP 0.96m. These figures are reconciled with NVS-003. A larger active quotation pipeline is not booked revenue and is not evidence of a completed Q4 revenue forecast.'),
('Customer commitments', 'Fictional customers include Larch Bioanalytics, Merrow University Research Centre, and Kestrel Discovery. Larch requested an updated delivery plan after two delayed September shipments. Merrow requested one named coordinator for service status. Kestrel requested clarification of Atlas documentation before scheduling its next research order. No binding new delivery date may be promised without the operating owner confirming it.'),
('Pipeline review', 'The commercial team estimates GBP 780,000 of open Q4 quotations at 30 September, before probability weighting. This is a planning indicator only. It includes expected service enquiries and kit quotations; the pack does not provide a signed order breakdown or conversion model. Grace asks the business review to stabilise fulfilment before increasing outbound promotions.'),
('Actions', 'Nina to prepare a customer recovery communication draft by 7 October. Daniel and Samir to supply realistic service and kit timing. Finance to reconcile any requested pricing concessions before approval. Customer messages remain drafts until Grace approves their content; financial commitments also follow NVS-008.')]),
('NVS-005', 'operations-quarterly-review', 'Operations review: production, release, and delivery', 'operations report', 'Daniel Brooks, COO', '2026-09-30', 'current', [
('Production and shipment', 'Production planned 28 kit lots for Q3. Twenty-five were released by 30 September and three were awaiting release documentation completion. A lot is not an order: the 28-lot count must not be used as the denominator for the 100 due customer orders. Of those 100 orders, 84 dispatched on time and 16 late.'),
('Delay categories', 'Operations assigned one primary delay category per late order: supplier availability, 7 orders; release documentation queue, 4; courier collection, 3; incomplete customer PO details, 2. These categories sum to 16. They classify operational delays and do not establish the causes of all revenue or reorder changes.'),
('Observed bottleneck', 'The release documentation queue grew during September. Owen reported repeated handoffs to correct incomplete checklists. Quality has not authorised any bypass of release review. NVS-013 records the related investigation and distinguishes an observed pattern from a confirmed root cause.'),
('October options', 'Operations proposes improving record completeness and handoffs before increasing output. The short project in NVS-017 needs four specialist weeks and GBP 18,000. An alternate-supplier assessment needs six specialist weeks and GBP 45,000 (NVS-014). Both compete for the six-week improvement allocation in NVS-007. Concurrent full execution is not feasible within that allocation.')]),
('NVS-006', 'customer-success-feedback', 'Customer success listening notes and repeat purchasing', 'customer feedback memo', 'Nina Ellis, Customer Success Manager', '2026-09-30', 'current', [
('Sample and metric', 'Customer Success interviewed eight fictional research customer contacts in September using a convenience sample. Five mentioned unpredictable kit timing, three unclear service status, and two documentation questions; themes overlap. This is not a representative survey and percentages must not be presented as company-wide prevalence. Separately, the Finance-approved reorder metric is 36 of 50 eligible Q3 accounts (72%), versus 41 of 50 in Q2 (82%).'),
('Listening notes', 'Larch: repeated delivery changes make its research scheduling difficult; requested a dependable update cadence. Merrow: the analytical report was useful, but status updates required contacting several people. Kestrel: purchasing postponed one planned reorder pending document clarification. These are qualitative fictional paraphrases, not verified causes across the entire customer cohort.'),
('Hypotheses', 'Delivery predictability and clearer status communication may help repeat purchasing. Nina recommends testing this rather than claiming that the reorder decline is entirely caused by Operations. The available documents do not quantify price sensitivity, competitor substitution, seasonality, or annual customer budget changes.'),
('Follow-up', 'Track confirmed shipment dates, late-order explanations, and customer update completion for October. Nina owns a recovery-message draft; Grace approves external messaging. The team will review next-quarter reorder rate when the new eligible cohort is defined. The current pack cannot establish an exact revenue uplift from either intervention.')]),
('NVS-007', 'october-capacity-and-options', 'October improvement capacity and option comparison', 'resource plan', 'Daniel Brooks and Dr Elena Ruiz', '2026-10-01', 'approved', [
('Available capacity', 'Four cross-functional specialists have 16 person-weeks available over the four-week October planning window. Ten person-weeks are already reserved for routine customer work, quality review support, and Orion milestones. Six specialist person-weeks remain for improvement work. This is a shared allocation, not six weeks from each department.'),
('Options', 'Release documentation improvement (NVS-017): four specialist weeks, GBP 18,000, proposed owner Owen. Alternate-supplier qualification assessment (NVS-014): six specialist weeks, GBP 45,000, proposed owner Tom with Quality input. Customer-status portal discovery: five specialist weeks, GBP 22,000, proposed owner Nina. The portal estimate covers discovery and a prototype, not production deployment.'),
('Feasible allocation', 'A release documentation improvement plus two weeks of measurement and customer coordination fits the six-week envelope. It cannot also include a full six-week supplier assessment or five-week portal discovery. Routine supplier monitoring and customer communications can continue within their already reserved functional workload; this does not mean the full competing projects have been funded.'),
('Decision boundaries', 'Costs are planning estimates with no quantified financial return. Priya must confirm budget availability. Quality must assess any release-related change. Project approval and Quality acceptance are separate gates. Capacity can be reallocated only by an explicitly recorded leadership decision, not inferred from meeting suggestions.')]),
('NVS-008', 'priorities-and-approval-policy', 'Q4 priorities and management approval policy', 'strategy and policy', 'Maya Chen, CEO', '2026-10-01', 'approved', [
('Priority order', '1. Protect reliable research supply and quality integrity. 2. Improve delivery predictability and customer trust. 3. Grow commercially where operating capacity supports commitments. An improvement recommendation must identify supporting evidence, tradeoffs, a responsible owner, and a review date.'),
('Spending authority', 'For a proposed operational project costing up to and including GBP 25,000, Daniel as COO may approve after Priya confirms budget availability. Above GBP 25,000 and up to GBP 75,000 requires both Daniel and Priya. Above GBP 75,000 requires Maya and Priya. This fictional internal rule is for the demo, not a statement of external regulation.'),
('Quality and scientific boundaries', 'Aisha independently approves quality implications and release-related changes. Spending approval never overrides a release hold. Elena reviews scientific scope and claims. Grace approves customer-facing communications; the accountable executive also approves associated financial commitments where required.'),
('Decision records', 'Record the evidence, chosen option, rejected options, owner, approver, date, budget condition, and follow-up measure. Recommendations and draft meeting action points do not constitute an approved decision. The shared log should distinguish proposed, approved, completed, and blocked items.')]),
('NVS-009', 'archived-q3-forecast', 'Archived Q3 forecast and delivery assumptions', 'forecast', 'Priya Shah, CFO', '2026-08-20', 'superseded', [
('Historical forecast', 'The August planning forecast projected GBP 2,880,000 Q3 revenue, gross margin 60%, and 95% on-time shipment. These were estimates and targets, not final actuals. It assumed sufficient supplier availability and a stable release-documentation queue.'),
('Why retained', 'This document is kept to explain what leadership expected before the quarter closed. It is superseded for actual performance by NVS-003 dated 2 October. The business review must not quote the forecast as recognised revenue or replace the current actual margin with the old expectation.'),
('Unresolved future', 'A complete approved Q4 forecast is not included in this pack. The Q4 quotation pipeline in NVS-004 is insufficient to infer Q4 recognised revenue. Ask Finance for the forecast instead of extrapolating an exact answer.')]),
('NVS-010', 'leadership-review-meeting', 'Leadership review meeting - 30 September', 'meeting notes', 'Leah Morgan, meeting recorder', '2026-09-30', 'reviewed', [
('Meeting context', 'Time: 09:00-09:45, Cambridge office / video call. Attendees: Maya, Priya, Daniel, Elena, Grace, Aisha, Leah. Purpose: prepare the Q3 review and select the information required for an October improvement decision. Finance presented provisional close figures of GBP 2.64m revenue and 57% gross margin; these became approved in NVS-003 on 2 October.'),
('Discussion', 'Grace described customer concerns about predictable delivery. Daniel distinguished supplier availability from release-record handoff problems. Aisha said no one may shorten release review by removing required evidence. Elena asked for the Orion reserved capacity to stay explicit. Maya requested an option comparison rather than a single uncosted proposal.'),
('Decisions and non-decisions', 'Agreed: prepare the six-week capacity plan and compare costed options for the next leadership review. The meeting did not approve the release project, supplier assessment, portal, or any customer compensation. A possible preference for documentation improvements was a discussion point, not authorisation.'),
('Action points', 'ACT-01 Priya: approve Q3 KPI close by 2 October. ACT-02 Owen: prepare release improvement proposal by 5 October. ACT-03 Nina: draft customer updates by 7 October. ACT-04 Tom: maintain supplier recovery tracking by 6 October. ACT-05 Maya: chair decision review on 6 October. Statuses and dependencies are in NVS-019.')]),
('NVS-011', 'weekly-operations-meeting', 'Weekly operations meeting - 29 September', 'meeting notes', 'Owen Reed, Production Lead', '2026-09-29', 'reviewed', [
('Attendance and agenda', '08:30-09:00. Attendees: Owen, Tom, Samir, Nina, and Aisha. Agenda: September dispatch, incomplete release records, customer update ownership, and supplier recovery. The team used operating figures that were reconciled in NVS-005 at quarter close.'),
('Working notes', 'Owen: three planned kit lots remain in the documentation queue. Aisha: incomplete records must be corrected and reviewed before release. Tom: supplier recovery dates are provisional and should be checked against current acknowledgements. Nina: customer updates need one accountable sender rather than separate unofficial messages.'),
('Agreed tasks', 'Owen to list recurring record omissions for the investigation in NVS-013. Tom to refresh supplier status. Nina to consolidate draft messages for Grace. No agreement changed the quality release rule. The meeting requested a project proposal; it did not approve a project budget.'),
('Carry-over', 'Readiness of the three lots remains dependent on complete records and Quality review. No guaranteed release or dispatch date is recorded here. Older planning dates are not current customer promises.')]),
('NVS-012', 'lab-team-standup', 'Laboratory services stand-up - 30 September', 'daily team note', 'Dr Samir Khan, Laboratory Services Lead', '2026-09-30', 'current', [
('Daily context', '09:15-09:30. Participants: Samir and the service scheduling team. Stonebridge turnaround averaged 12 working days in Q3, compared with the eight-day target. This is a service timing measure, not kit shipment performance.'),
('Work queue', 'The team discussed incomplete customer paperwork and report-review scheduling as possible contributors to waiting time. The quarterly pack does not break turnaround into validated stage durations, so neither contribution can be quantified yet. Samir requested a simple queue-stage review before promising a revised service lead time.'),
('Today\'s actions', 'Samir to review the waiting queue with the scheduler. Nina to provide the named-coordinator contact plan for Merrow. No individual laboratory protocol or experimental procedure is captured in these notes.'),
('Escalation', 'A change to scientific service scope goes to Elena. Quality concerns go to Aisha. A customer timing commitment requires confirmation from Samir and approval of the external wording by Grace.')]),
('NVS-013', 'quality-investigation-capa', 'QA investigation QA-26-014 and corrective action status', 'quality status record', 'Dr Aisha Patel, Head of Quality', '2026-10-02', 'current', [
('Record status', 'QA-26-014 opened 24 September after recurring incomplete release checklists were observed. Corrective and preventive action (CAPA) investigation is open. At 2 October, the root cause is not confirmed. This is a fictional business-level record, not a completed quality investigation or regulatory filing.'),
('Observed evidence', 'The quarter-close operations report records three planned lots awaiting documentation completion and four late orders with release documentation queue as their primary delay category. These are related observations using different units. They do not show that the three lots caused exactly four late orders.'),
('Containment and proposal', 'Incomplete records remain in the review queue until corrected. Owen proposes completeness checks and clearer handoffs. Aisha will evaluate whether the proposed change preserves required evidence and independent review. The project cannot be described as a validated fix or an approved change before this gate.'),
('Next review', 'Aisha to review the change proposal after ACT-02 is ready. Samir and Owen to contribute operational observations. Closure requires documented investigation conclusions and evidence that the accepted action is effective. There is no committed closure date in this pack.')]),
('NVS-014', 'supplier-review', 'Supplier performance and contingency review', 'supplier memo', 'Tom Bell, Supply Chain Manager', '2026-10-01', 'current', [
('Supplier context', 'Helix Materials is a fictional supplier supporting Atlas production. Operations attributed seven of the sixteen late Q3 orders primarily to supplier availability. Tom is monitoring delivery acknowledgements with Helix; these remain forecasts, not guaranteed shipment commitments to Novastone customers.'),
('Contingency option', 'An assessment of fictional alternate supplier Alder Scientific is estimated at six specialist weeks and GBP 45,000. This is an assessment/qualification planning estimate, not proof of product equivalence or an approval to use material. Quality and scientific review would be required before any relevant release change.'),
('Tradeoff', 'The full assessment uses all six improvement weeks in NVS-007. It cannot run alongside the full four-week documentation project within that envelope. Daniel and Priya must jointly approve its spend, and Quality retains its independent technical acceptance gate.'),
('Uncertainty', 'The pack contains no exact avoided-loss calculation, signed replacement supply agreement, or comparative technical validation. Continued routine supplier monitoring is distinct from approving the alternate-supplier project.')]),
('NVS-015', 'orion-project-update', 'Project Orion monthly research product update', 'project update', 'Dr Elena Ruiz, CSO', '2026-09-30', 'current', [
('Project scope', 'Orion is a fictional internal project to improve the usability and documentation of the Atlas research product family. Its October milestone is an internal documentation and feasibility review, not a clinical launch or an approved commercial claim. No assay design, experimental recipe, or clinical performance data is provided.'),
('Progress', 'Customer Success collected documentation questions; R&D reviewed scope; Quality requested clearer separation of draft claims from approved statements. The team is preparing the review pack. Any exact launch date or financial benefit is unknown from these records.'),
('Capacity and dependencies', 'The October routine-work reservation in NVS-007 includes Orion support. Those weeks are not part of the six discretionary improvement weeks. Elena must assess any proposal to redirect Orion staff. Aisha reviews quality statements; Grace reviews customer-facing material.'),
('Management request', 'Keep Orion\'s reserved milestone capacity visible while comparing operational improvements. Do not describe research feasibility as validated product performance. Ask for the reviewed milestone outcome before recommending an external product announcement.')]),
('NVS-016', 'document-governance-guide', 'Working guide: documents, meetings, and knowledge ownership', 'internal procedure', 'Leah Morgan and Dr Aisha Patel', '2026-10-01', 'approved', [
('Document ownership', 'Every shared record has an owner, document ID, version, effective/update date, and status. Owners correct errors and publish new versions. Superseded records are retained for context but are not the current authority for actual figures or instructions. NVS-003 is the current source for Q3 actual KPIs.'),
('Meeting practice', 'The recorder separates discussion, decisions, and action points. Attendees review factual errors. Action items include a named owner and due date; proposed projects still require the approval route in NVS-008. A meeting summary cannot substitute for a quality release record or a spending approval.'),
('Sharing and source use', 'This fictional pack uses internal-demo audience labels to exercise the product design; its exported files are public synthetic content. Those labels are metadata, not an access-control mechanism. A future real deployment must enforce source permissions. Retain citations and original meeting context when generating a summary.'),
('AI-generated drafts', 'Generated drafts must display draft status until reviewed. Imported text and meeting suggestions are knowledge sources, not permission to operate connected services. Corrected versions should replace older indexed content while preserving provenance and the historical decision trail.')]),
('NVS-017', 'release-improvement-proposal', 'Proposal: improve release record completeness', 'project proposal', 'Owen Reed, Production Lead', '2026-10-02', 'draft', [
('Proposed intervention', 'Standardise completeness checks, clarify who owns each handoff, and measure time spent waiting for corrected release records. Preserve all existing Quality review requirements. This proposal is intended to address an observed queue problem, while QA-26-014 remains under investigation.'),
('Effort and budget', 'Estimate: four specialist person-weeks and GBP 18,000. Reserve the remaining two of the six available improvement weeks for measurement and coordination if leadership chooses this option. The combined allocation fits NVS-007; simultaneous full supplier assessment or portal discovery does not.'),
('Approval and measures', 'Daniel may approve the operational project after Priya confirms budget availability, because the estimate is below GBP 25,000. Aisha must independently accept release-related changes. Proposed review on 30 October: completeness on first submission, release-record waiting time, and the next comparable on-time shipment measure. Baselines for the first two measures still need to be collected.'),
('Limits and next step', 'No budget is approved in this document. No exact margin, reorder, or revenue uplift is claimed. ACT-02 is to prepare the proposal, not execute it. After approval, Owen should establish the baseline and an agreed measurement definition before reporting improvement.')]),
('NVS-018', 'new-starter-handover', 'New starter and team handover notes', 'onboarding / handover', 'Leah Morgan, People and Operations', '2026-10-01', 'current', [
('Who to ask', 'For quarterly financial definitions, contact Priya\'s team. For kit scheduling, Owen; for supplier status, Tom; for analytical service timing, Samir. Nina coordinates customer status, and Grace approves external communications. Aisha handles Quality escalation independently of Operations.'),
('First-week orientation', 'Read NVS-001 for the business model, NVS-002 for the organisation, NVS-016 for document practice, and NVS-008 for approval rules. Product and service records are for research use only. New starters should not make scientific claims or promise dispatch dates based on unreviewed notes.'),
('Current handover', 'The October business review is considering release documentation improvements. That proposal is still draft. Three planned Q3 lots await complete documentation and Quality review; the exact release date is not provided. Service turnaround and kit delivery are different measures.'),
('Everyday tasks', 'Record handover questions in the team meeting notes, link the current source, and assign an owner rather than forwarding an unexplained extract. Ask the document owner to resolve discrepancies. Refer to NVS-019 for current actions; an overdue date alone does not prove an action failed.')]),
('NVS-019', 'shared-action-tracker', 'Shared action tracker - snapshot at 2 October', 'action tracker', 'Leah Morgan, coordination owner', '2026-10-02', 'current', [
('Action register', 'ACT-01 | Priya | approve Q3 KPI close | due 2 Oct | completed 2 Oct | evidence NVS-003.\nACT-02 | Owen | prepare release improvement proposal | due 5 Oct | in progress | draft NVS-017; not execution approval.\nACT-03 | Nina | prepare customer recovery messages | due 7 Oct | in progress | depends on operating timing and Grace review.\nACT-04 | Tom | update routine supplier recovery tracking | due 6 Oct | open | NVS-014.\nACT-05 | Maya | chair improvement decision review | due 6 Oct | scheduled | requires NVS-007 and costed proposals.\nACT-06 | Samir | establish service queue-stage review | due 8 Oct | open | requested in NVS-012.'),
('Status meanings', 'Open: assigned and not yet started. In progress: preparation under way. Scheduled: a planned review, not a completed decision. Completed: owner supplied evidence. Blocked items must identify their dependency. Dates here are calendar due dates, not automation schedules.'),
('Execution boundary', 'The tracker does not authorise a project, spend, product release, message, or connected-service action. Project approval follows NVS-008; future automations can prepare proposals from this tracker only within an explicitly configured scope.')]),
('NVS-020', 'decision-and-risk-log', 'Decision history and current management risks', 'decision / risk register', 'Maya Chen, CEO', '2026-10-02', 'current', [
('Existing decisions', 'DEC-01 | 30 Sep | leadership agreed to prepare an option comparison; owner Daniel; no project funding approved. DEC-02 | 1 Oct | Daniel and Elena approved a six-person-week improvement capacity envelope after reserving ten routine-work weeks; no project selected. DEC-03 | 2 Oct | Priya approved the quarter-close KPI report NVS-003.'),
('Pending decision', 'DEC-04 is reserved for the 6 October improvement review. It has no chosen option or approver yet. The assistant may propose release record improvements with a budget condition and a Quality gate, but must not claim they were already approved.'),
('Current risks', 'RISK-01 supplier availability: Tom owns monitoring; likelihood medium, customer impact high. RISK-02 release-record waiting: Owen owns proposal preparation; quality implications reviewed by Aisha; likelihood high, impact high. RISK-03 customer trust: Nina tracks feedback and communications; likelihood medium, impact high. RISK-04 resource overload: Daniel and Elena own the shared capacity plan; likelihood medium, impact medium. Ratings are judgemental internal labels, not calculated probabilities.'),
('Review evidence', 'An informed decision should cite NVS-003 for actual performance, NVS-005/006 for operating and customer observations, NVS-007 for capacity, NVS-008 for authority, and NVS-017 for the draft intervention. A selected recommendation should include alternative options, unknowns, owner, review date, and approval state.')]),
]

manifest=[]
for idx, slug, title, kind, owner, date, status, sections in DOCS:
    path=SOURCE/(slug+'.md')
    metadata={'document_id':idx,'title':title,'type':kind,'owner':owner,'updated_at':date,'version':'1.0','status':status,'company':'Novastone','audience':'internal-demo','synthetic':True,'period':'Q3 2026 / October planning'}
    body='---\n'+'\n'.join(f'{k}: {json.dumps(v)}' for k,v in metadata.items())+'\n---\n\n'
    body+=f'# {title}\n\nFICTIONAL DEMO DOCUMENT - no real company, customer, or scientific records.\n\n'
    for n,(heading,content) in enumerate(sections,1):
        display='```text\n'+content+'\n```' if idx=='NVS-002' and n==1 else content
        body+=f'## {idx}-S{n:02d} | {heading}\n\n{display}\n\n'
    path.write_text(body,encoding='utf-8')
    manifest.append({**metadata,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(body.encode()).hexdigest(),'sections':[{'id':f'{idx}-S{n:02d}','title':h} for n,(h,_) in enumerate(sections,1)]})

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='DocTitle',fontName='Helvetica-Bold',fontSize=20,leading=24,textColor=colors.HexColor('#173c4f'),spaceAfter=12))
styles.add(ParagraphStyle(name='DocBody',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8))
styles.add(ParagraphStyle(name='DocSection',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=colors.HexColor('#267c83'),spaceBefore=10,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='Meta',fontName='Helvetica',fontSize=8,leading=11,textColor=colors.HexColor('#52616b'),spaceAfter=8))
story=[]
page_starts={}
class PackTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(flowable,'doc_id'):
            page_starts[flowable.doc_id]=self.page

def para(txt, style='DocBody'):
    return Paragraph(escape(txt).replace('\n','<br/>'),styles[style])
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#d6e4e7'));canvas.line(18*mm,17*mm,192*mm,17*mm)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#52616b'))
    canvas.drawString(18*mm,12*mm,'NOVASTONE | SYNTHETIC KNOWLEDGE PACK | 2 OCT 2026')
    canvas.drawRightString(192*mm,12*mm,f'Page {doc.page}')

class OrgChart(Flowable):
    def __init__(self):
        super().__init__()
        self.width=174*mm
        self.height=65*mm
    def draw(self):
        c=self.canv
        c.setStrokeColor(colors.HexColor('#267c83'))
        c.setFillColor(colors.HexColor('#edf5f6'))
        c.roundRect(57*mm,45*mm,60*mm,18*mm,3*mm,fill=1)
        c.setFillColor(colors.HexColor('#173c4f'));c.setFont('Helvetica-Bold',9)
        c.drawCentredString(87*mm,56*mm,'Maya Chen | CEO')
        c.setFont('Helvetica',8);c.drawCentredString(87*mm,50*mm,'1 staff | 60 company total')
        c.line(87*mm,45*mm,87*mm,39*mm);c.line(16*mm,39*mm,158*mm,39*mm)
        groups=[('Priya Shah','CFO','Finance / People','8 staff'),('Daniel Brooks','COO','Production / Supply','14 staff'),('Dr Elena Ruiz','CSO','R&D / Lab Services','19 staff'),('Grace Okafor','Commercial','Sales / Success','12 staff'),('Dr Aisha Patel','Quality','Independent of Ops','6 staff')]
        for i,g in enumerate(groups):
            x=i*35.5*mm;c.line(x+16*mm,39*mm,x+16*mm,32*mm)
            c.setFillColor(colors.HexColor('#edf5f6'));c.roundRect(x,7*mm,32*mm,25*mm,2*mm,fill=1)
            c.setFillColor(colors.HexColor('#173c4f'))
            for j,line in enumerate(g):
                c.setFont('Helvetica-Bold' if j==0 else 'Helvetica',7)
                c.drawCentredString(x+16*mm,(26-j*5)*mm,line)

story += [Spacer(1,20*mm),para('Novastone','DocTitle'),para('Business review and everyday company knowledge','DocTitle'),para('Q3 2026 | 20 fictional source documents | Snapshot: 2 October 2026'),para('A bioscience company scenario for demonstrating evidence-based business reviews, source citations, accountable decisions, and shared knowledge.'),para('All names, figures, customers, suppliers, and records are invented. This material does not describe any actual company using the name Novastone. Research-use business context only; no laboratory procedures, clinical advice, or real confidential records.'),para('Reading this pack','DocSection'),para('Each document starts on a new page and carries an ID, owner, date, version, and status. Section IDs match the separate Markdown source files and the source manifest. Current actuals, forecasts, meeting discussion, and draft proposals retain their distinct statuses.'),PageBreak(),para('Source index','DocTitle')]
for idx,slug,title,kind,owner,date,status,sections in DOCS:
    story.append(para(f'{idx} | {title} | {status}','Meta'))
for idx,slug,title,kind,owner,date,status,sections in DOCS:
    story.append(PageBreak())
    title_p=para(title,'DocTitle');title_p.doc_id=idx;story.append(title_p)
    story.append(para(f'{idx} | {kind} | Version 1.0 | {status.upper()}\nOwner: {owner} | Updated: {date} | Audience: internal-demo (synthetic public export)','Meta'))
    story.append(para('FICTIONAL DEMO DOCUMENT - no real company, customer, or scientific records.','Meta'))
    for n,(heading,content) in enumerate(sections,1):
        story.append(para(f'{idx}-S{n:02d} | {heading}','DocSection'))
        if idx=='NVS-002' and n==1:
            story.append(OrgChart())
        story.append(para(content))
pdf=OUT/'novastone-company-knowledge-pack.pdf'
PackTemplate(str(pdf),pagesize=(210*mm,297*mm),rightMargin=18*mm,leftMargin=18*mm,topMargin=18*mm,bottomMargin=23*mm,title='Novastone - Fictional Company Knowledge Pack',author='Fictional Novastone demo').build(story,onFirstPage=footer,onLaterPages=footer)
pages=len(PdfReader(str(pdf)).pages)
for i,m in enumerate(manifest):
    m['pdf_path']=str(pdf.relative_to(ROOT))
    m['pdf_start_page']=page_starts[m['document_id']]
    m['pdf_end_page']=page_starts[manifest[i+1]['document_id']]-1 if i+1<len(manifest) else pages
(SOURCE/'manifest.json').write_text(json.dumps({'snapshot_date':'2026-10-02','company':'Novastone','synthetic':True,'source_count':len(manifest),'documents':manifest},indent=2)+'\n')

# Checks support useful evidence rather than comparing a generated file to itself.
assert len(DOCS)==20 and len(set(x[0] for x in DOCS))==20
assert 1680000+960000==2640000
assert round((2640000/2400000-1)*100,2)==10
assert 2880000-2640000==240000
assert 7+4+3+2==16 and 84+16==100
assert 1+8+14+19+12+6==60 and 16-10==6 and 4+2==6
assert 36/50==.72 and 41/50==.82
all_ids={d[0] for d in DOCS}
for m in manifest:
    content=(ROOT/m['path']).read_text()
    assert all(x in all_ids for x in re.findall(r'NVS-\d{3}',content)),m['path']
    text='\n'.join(PdfReader(str(pdf)).pages[i].extract_text() for i in range(m['pdf_start_page']-1,m['pdf_end_page']))
    assert m['document_id'] in text and 'FICTIONAL DEMO' in text,m['document_id']
    for sec in m['sections']:
        assert sec['id'] in text,sec['id']
print(json.dumps({'documents':len(DOCS),'pdf_pages':pages,'pdf':str(pdf),'consistency_checks':'passed','source_ranges':page_starts},indent=2))
