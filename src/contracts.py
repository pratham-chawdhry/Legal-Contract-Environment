"""
contracts.py — Synthetic contract generator with injected fault manifests.
All contracts are entirely fictional. Ground truth is programmatically defined.

Complexity targets (for benchmarking):
  easy   — 7 sections, 4 real faults (spread across sections), 1 trap
  medium — 10 sections, 6 real faults (incl. cross-section), 3 traps
  hard   — 14 sections, 9 real faults (incl. layered/definitional), 5 traps
"""
from __future__ import annotations
from typing import Dict, List
from src.models import FaultEntry


# ================================================================== #
#  EASY — 1-page NDA
#  Faults spread across 4 different sections. 1 trap.
# ================================================================== #

NDA_SECTIONS: Dict[str, str] = {
    "parties": """
MUTUAL NON-DISCLOSURE AGREEMENT

This Agreement is entered into as of January 15, 2025, between:
  Acme Corp, a Delaware corporation ("Disclosing Party"), and
  Beta Ventures LLC, a California LLC ("Receiving Party").
""".strip(),

    "purpose": """
PURPOSE

The parties wish to explore a potential business collaboration related to
artificial intelligence tooling ("Purpose"). Each party may disclose
confidential information to the other solely to evaluate this Purpose.
""".strip(),

    "definition_confidential": """
DEFINITION OF CONFIDENTIAL INFORMATION

"Confidential Information" means any non-public information disclosed by
either party in written form only. Oral disclosures shall not be considered
Confidential Information unless confirmed in writing within five (5) business
days of disclosure. This includes, but is not limited to, trade secrets,
business plans, financial data, technical specifications, and customer lists.
""".strip(),

    "obligations": """
OBLIGATIONS OF RECEIVING PARTY

The Receiving Party agrees to:
(a) hold Confidential Information in strict confidence;
(b) not disclose Confidential Information to any third party without prior
    written consent of the Disclosing Party;
(c) use Confidential Information solely for the Purpose;
(d) protect the Confidential Information using at least the same degree of
    care it uses to protect its own confidential information, but in no event
    less than reasonable care.

The Receiving Party shall defend, indemnify, and hold harmless the
Disclosing Party from and against any and all claims, damages, losses,
costs, and expenses (including attorneys' fees) arising out of or relating
to any breach of this Agreement by the Receiving Party, with no limitation
on the amount of such indemnification.
""".strip(),

    "exceptions": """
EXCEPTIONS TO CONFIDENTIALITY

The obligations of confidentiality shall not apply to information that:
(a) is or becomes publicly available through no breach of this Agreement;
(b) was rightfully known to Receiving Party prior to disclosure;
(c) is independently developed by Receiving Party without use of Confidential
    Information;
(d) is required to be disclosed by law or court order, provided Receiving Party
    provides prompt written notice to Disclosing Party.

Note: The exceptions in (a) through (d) above apply equally to sublicensees
and affiliates of the Receiving Party, who may freely use information falling
within any exception without restriction or notice to the Disclosing Party.
""".strip(),

    "term": """
TERM

This Agreement shall remain in effect for a period of five (5) years from
the Effective Date, unless earlier terminated by either party upon thirty
(30) days written notice. Confidentiality obligations shall survive termination
of this Agreement for a period of one (1) year.
""".strip(),

    "governing_law": """
GOVERNING LAW AND DISPUTES

This Agreement shall be governed by and construed in accordance with the
laws of the State of Delaware, without regard to its conflict of law provisions.
Any dispute arising under this Agreement shall be resolved exclusively by
binding arbitration administered by the American Arbitration Association,
and judgment on the award may be entered in any court having jurisdiction.
The parties waive all rights to a jury trial and to seek injunctive relief
in any court in connection with any dispute arising under this Agreement.
""".strip(),

    "general": """
GENERAL

This Agreement constitutes the entire agreement between the parties with
respect to its subject matter and supersedes all prior agreements. This
Agreement may be amended only by a written instrument signed by both parties.
If any provision is found to be unenforceable, the remaining provisions shall
remain in full force.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date
first written above.

Acme Corp: _______________________     Beta Ventures LLC: _______________________
""".strip(),
}

NDA_FAULTS: List[FaultEntry] = [
    # F1 — obligations: unlimited indemnity (critical, risky)
    FaultEntry(
        fault_id="F1",
        fault_type="risky_clause",
        section="obligations",
        clause_id="unlimited_indemnity",
        risk_level="critical",
        description=(
            "The indemnification clause imposes unlimited, one-sided indemnity on the "
            "Receiving Party with no cap, no carve-outs, no notice requirement, and no "
            "right to control defense. This is non-standard and highly unfavorable."
        ),
        standard_language=(
            "Each party shall indemnify the other for direct damages caused by its "
            "material breach, subject to a mutual liability cap, provided the indemnified "
            "party gives prompt written notice and cooperates in defense."
        ),
    ),
    # F2 — obligations: missing liability cap (critical, missing)
    FaultEntry(
        fault_id="F2",
        fault_type="missing_clause",
        section="obligations",
        clause_id="liability_cap",
        risk_level="critical",
        description=(
            "No liability cap exists. The unlimited indemnification in 'obligations' "
            "exposes the Receiving Party to infinite financial liability for any breach."
        ),
        standard_language=(
            "IN NO EVENT SHALL EITHER PARTY'S TOTAL LIABILITY EXCEED THE GREATER OF "
            "(A) $50,000 OR (B) AMOUNTS PAID IN THE PRIOR 12 MONTHS UNDER THIS AGREEMENT."
        ),
    ),
    # F3 — definition_confidential: oral disclosures excluded (medium, risky)
    FaultEntry(
        fault_id="F3",
        fault_type="risky_clause",
        section="definition_confidential",
        clause_id="oral_disclosure_exclusion",
        risk_level="medium",
        description=(
            "The definition of Confidential Information covers written disclosures only. "
            "Oral disclosures are excluded unless confirmed in writing within 5 days. "
            "In practice, most sensitive disclosures in early-stage business discussions "
            "happen verbally — this definition leaves them unprotected."
        ),
        standard_language=(
            "Confidential Information means any non-public information disclosed by either "
            "party, whether orally, in writing, or by inspection of tangible objects, that "
            "is designated as confidential or that reasonably should be understood to be "
            "confidential given the nature and circumstances of disclosure."
        ),
    ),
    # F4 — exceptions: affiliates carve-out (medium, risky)
    FaultEntry(
        fault_id="F4",
        fault_type="risky_clause",
        section="exceptions",
        clause_id="affiliate_exception_overreach",
        risk_level="medium",
        description=(
            "The exceptions clause extends all confidentiality exceptions to the Receiving "
            "Party's affiliates and sublicensees without restriction. This effectively "
            "allows any affiliate to freely use information it claims falls under an "
            "exception, with no notice or accountability to the Disclosing Party."
        ),
        standard_language=(
            "Exceptions apply solely to the Receiving Party. Affiliates receiving "
            "Confidential Information remain bound by the obligations of this Agreement "
            "as if they were the Receiving Party."
        ),
    ),
    # F5 — term: post-termination survival too short (low, risky) — TRAP
    FaultEntry(
        fault_id="F5",
        fault_type="risky_clause",
        section="term",
        clause_id="survival_one_year",
        risk_level="low",
        description=(
            "Post-termination survival of 1 year is on the shorter end but within "
            "market range for a short-term NDA. NOT a genuine red flag — 1–3 year "
            "post-termination survival is standard for NDAs of this type."
        ),
        is_trap=True,
    ),
    # F6 — governing_law: waiver of injunctive relief (critical, risky)
    FaultEntry(
        fault_id="F6",
        fault_type="risky_clause",
        section="governing_law",
        clause_id="injunctive_relief_waiver",
        risk_level="critical",
        description=(
            "The governing law section contains a blanket waiver of injunctive relief "
            "for both parties. For an NDA, injunctive relief is typically the primary "
            "remedy for breach — money damages are often inadequate when confidential "
            "information is disclosed. This waiver effectively guts the enforceability "
            "of the agreement against a breaching party."
        ),
        standard_language=(
            "Each party acknowledges that breach of this Agreement may cause irreparable "
            "harm for which monetary damages would be inadequate, and that injunctive or "
            "other equitable relief may be sought in any court of competent jurisdiction "
            "without posting bond or other security."
        ),
    ),
]


# ================================================================== #
#  MEDIUM — 8-page SaaS Agreement
#  6 real faults including 2 cross-section issues. 3 traps.
# ================================================================== #

SAAS_SECTIONS: Dict[str, str] = {
    "definitions": """
DEFINITIONS

1.1 "Agreement" means this Software as a Service Agreement including all Schedules.
1.2 "Authorized Users" means employees of Customer permitted to access the Service,
    limited to the number of seats specified in Schedule B.
1.3 "Customer Data" means all data submitted by Customer through the Service.
1.4 "Documentation" means the user guides and technical specifications provided by Vendor.
1.5 "Feedback" means any suggestions, ideas, enhancement requests, or recommendations
    provided by Customer or its Authorized Users regarding the Service.
1.6 "Service" means Vendor's cloud-based platform described in Schedule A.
1.7 "Subscription Term" means the Initial Term and any Renewal Terms as further described
    in Section 9.1. Unless Customer provides written notice of non-renewal no less than
    thirty (30) days prior to the end of the then-current Subscription Term, this Agreement
    shall automatically renew for successive one (1) year periods at Vendor's then-current
    list price, which may be increased by up to fifteen percent (15%) upon renewal without
    further notice to Customer.
1.8 "Aggregate Data" means data derived from Customer Data that has been anonymized such
    that it does not directly identify Customer or its users.
""".strip(),

    "license_grant": """
LICENSE GRANT

2.1 Subject to the terms of this Agreement and payment of applicable fees, Vendor grants
    Customer a non-exclusive, non-transferable, limited license to access and use the
    Service during the Subscription Term solely for Customer's internal business purposes.
2.2 Customer may not: (a) sublicense, sell, or transfer the Service; (b) reverse engineer
    or attempt to derive source code; (c) use the Service to build a competing product.
2.3 Customer grants Vendor a non-exclusive, worldwide, royalty-free license to use,
    reproduce, and display Customer Data solely to provide the Service and as otherwise
    permitted under this Agreement.
""".strip(),

    "fees_payment": """
FEES AND PAYMENT

3.1 Customer shall pay all fees set forth in Schedule B within thirty (30) days of invoice.
3.2 All fees are non-refundable except as expressly set forth herein.
3.3 Vendor reserves the right to suspend access immediately and without notice for
    past-due amounts exceeding thirty (30) days.
3.4 Fees are exclusive of taxes; Customer is responsible for all applicable taxes.
3.5 Vendor may modify its fee schedule at any time upon thirty (30) days notice to Customer.
    Continued use of the Service after such notice constitutes acceptance of revised fees.
""".strip(),

    "data_privacy": """
DATA PRIVACY AND SECURITY

4.1 Vendor shall implement and maintain reasonable administrative, technical, and physical
    safeguards designed to protect Customer Data.
4.2 Vendor shall notify Customer of any confirmed security breach affecting Customer Data
    within seventy-two (72) hours of Vendor becoming aware of such breach.
4.3 Vendor may use Customer Data in aggregated, anonymized form to improve its services
    and for any other commercial purpose, including sale to third parties, provided such
    data is de-identified.
4.4 Upon termination, Vendor shall delete Customer Data within ninety (90) days unless
    legally required to retain it.
4.5 Customer acknowledges that the Service is hosted on third-party cloud infrastructure
    and that Vendor's security obligations are limited to controls within Vendor's reasonable
    administrative control.
""".strip(),

    "intellectual_property": """
INTELLECTUAL PROPERTY

5.1 Vendor retains all right, title, and interest in the Service and Documentation.
5.2 Customer retains all right, title, and interest in Customer Data.
5.3 Notwithstanding Section 5.2, Customer hereby grants Vendor a worldwide, perpetual,
    irrevocable, royalty-free license to use Customer Data to provide and improve the
    Service, to develop new products and services, and to sublicense such rights to
    Vendor's affiliates and third-party service providers without restriction or
    Customer consent. This license survives termination of this Agreement.
5.4 All Feedback submitted by Customer is hereby assigned to Vendor and Customer waives
    all moral rights therein. Vendor may use Feedback for any purpose without compensation
    or attribution to Customer.
5.5 Any custom features or integrations developed by Vendor at Customer's request shall
    be owned solely by Vendor unless separately agreed in writing.
""".strip(),

    "warranties": """
WARRANTIES AND DISCLAIMERS

6.1 Vendor warrants that the Service will perform materially in accordance with the
    Documentation during the Subscription Term.
6.2 EXCEPT AS EXPRESSLY SET FORTH IN SECTION 6.1, THE SERVICE IS PROVIDED "AS IS."
    VENDOR DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES
    OF FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
6.3 Customer warrants that it has obtained all necessary rights and consents to provide
    Customer Data to Vendor and that such data does not violate any applicable law.
""".strip(),

    "limitation_liability": """
LIMITATION OF LIABILITY

7.1 NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL
    DAMAGES, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
7.2 VENDOR'S TOTAL AGGREGATE LIABILITY SHALL NOT EXCEED THE FEES PAID BY CUSTOMER
    IN THE THREE (3) MONTHS PRECEDING THE CLAIM.
7.3 The limitations in this Section 7 shall apply regardless of the theory of liability
    and notwithstanding any failure of essential purpose of any limited remedy.
""".strip(),

    "term_termination": """
TERM AND TERMINATION

8.1 Initial Term: This Agreement commences on the Effective Date and continues for
    one (1) year ("Initial Term").
8.2 Termination for Cause: Either party may terminate this Agreement upon thirty (30)
    days written notice if the other party materially breaches this Agreement and fails
    to cure such breach within such notice period.
8.3 Effect of Termination: Upon termination, all licenses granted hereunder shall
    immediately terminate and Customer shall cease all use of the Service.
8.4 Vendor may terminate this Agreement immediately upon written notice if Customer
    files for bankruptcy, makes an assignment for the benefit of creditors, or becomes
    subject to insolvency proceedings.
""".strip(),

    "general": """
GENERAL PROVISIONS

9.1 Governing Law: This Agreement shall be governed by the laws of California.
9.2 Entire Agreement: This Agreement constitutes the entire agreement between the parties.
9.3 Amendments: Vendor may amend this Agreement at any time by posting updated terms to
    its website. Customer's continued use of the Service after thirty (30) days of such
    posting constitutes acceptance of the amended Agreement.
9.4 Waiver: Failure to enforce any provision shall not constitute a waiver.
9.5 Severability: If any provision is unenforceable, remaining provisions continue.
9.6 Assignment: Customer may not assign this Agreement without Vendor's prior written
    consent. Vendor may assign this Agreement freely, including to a competitor of Customer.
""".strip(),

    "schedule_a_sla": """
SCHEDULE A — SERVICE LEVELS

A.1 Vendor will use commercially reasonable efforts to make the Service available.
    No specific uptime commitment is made and no credits are available for downtime.
A.2 Scheduled maintenance windows may occur at any time with or without advance notice.
A.3 Vendor's support team is available Monday–Friday, 9AM–5PM Pacific Time.
    Response time targets are non-binding and for informational purposes only.
A.4 Customer's sole remedy for any Service degradation or outage is to submit a
    support ticket. No refunds, credits, or termination rights arise from downtime.
""".strip(),
}

SAAS_FAULTS: List[FaultEntry] = [
    # F1 — definitions: auto-renewal with price hike buried in definitions (medium, risky)
    FaultEntry(
        fault_id="F1",
        fault_type="risky_clause",
        section="definitions",
        clause_id="auto_renewal_buried",
        risk_level="medium",
        description=(
            "Auto-renewal with up to 15% price escalation is buried in Section 1.7 "
            "(Definitions — 'Subscription Term'), not in the Term & Termination section. "
            "The 30-day non-renewal notice window is aggressively tight. This is a common "
            "predatory drafting pattern designed to trap customers into renewing."
        ),
        standard_language=(
            "Auto-renewal terms and price change provisions must appear in the Term & "
            "Termination section with at least 60 days notice of non-renewal and 90 days "
            "advance notice of any price increase exceeding CPI."
        ),
    ),
    # F2 — intellectual_property: irrevocable, sublicensable data license surviving termination (critical, risky)
    FaultEntry(
        fault_id="F2",
        fault_type="risky_clause",
        section="intellectual_property",
        clause_id="irrevocable_data_license",
        risk_level="critical",
        description=(
            "Section 5.3 grants Vendor a perpetual, irrevocable, sublicensable license "
            "to Customer Data that survives termination, covers new product development, "
            "and permits sublicensing to third parties without restriction or consent. "
            "This contradicts Section 5.2's statement that Customer retains its data, "
            "and is extraordinarily broad — Customer cannot revoke this grant ever."
        ),
        standard_language=(
            "Any license to Customer Data should be limited in scope to providing the "
            "Service, non-sublicensable without Customer consent, and must terminate "
            "upon contract expiration with data return/deletion obligations."
        ),
    ),
    # F3 — data_privacy: commercial sale of de-identified data (medium, risky)
    FaultEntry(
        fault_id="F3",
        fault_type="risky_clause",
        section="data_privacy",
        clause_id="data_sale_permitted",
        risk_level="medium",
        description=(
            "Section 4.3 permits Vendor to sell Customer Data to third parties as long "
            "as it is de-identified. De-identification standards are not defined, and "
            "no Customer consent is required. Combined with the irrevocable license in "
            "Section 5.3, this creates a dual pathway for Vendor to commercialize "
            "Customer Data both during and after the contract term."
        ),
        standard_language=(
            "Vendor shall not sell, rent, or otherwise commercialize Customer Data or "
            "Aggregate Data derived therefrom. Vendor may only use de-identified data "
            "to improve the Service provided to Customer, not for external commercialization."
        ),
    ),
    # F4 — schedule_a_sla: no uptime SLA anywhere (medium, missing)
    FaultEntry(
        fault_id="F4",
        fault_type="missing_clause",
        section="schedule_a_sla",
        clause_id="sla_uptime_commitment",
        risk_level="medium",
        description=(
            "Schedule A explicitly disclaims any uptime commitment and removes all "
            "remedies (credits, refunds, termination) for downtime. A SaaS agreement "
            "without any measurable uptime SLA leaves Customer with no recourse for "
            "service degradation regardless of severity or duration."
        ),
        standard_language=(
            "Vendor commits to 99.9% monthly uptime (excluding scheduled maintenance "
            "with 48hr notice). For each hour of excess downtime, Customer receives a "
            "service credit of 1/720th of monthly fees, up to 30% of monthly fees. "
            "Repeated failure (3+ months below SLA in any 12-month period) constitutes "
            "grounds for termination for cause."
        ),
    ),
    # F5 — general: unilateral amendment right (critical, risky)
    # CROSS-SECTION: this interacts with fees_payment Section 3.5 which also allows unilateral fee changes
    FaultEntry(
        fault_id="F5",
        fault_type="risky_clause",
        section="general",
        clause_id="unilateral_amendment",
        risk_level="critical",
        description=(
            "Section 9.3 allows Vendor to unilaterally amend any term of the Agreement "
            "by posting to its website, with Customer's continued use constituting "
            "acceptance. This is compounded by Section 3.5 which allows unilateral "
            "fee changes on 30-day notice. Together these provisions mean Customer "
            "has no contractual stability — Vendor can change price, scope, data rights, "
            "or liability caps at any time. Standard SaaS agreements require mutual "
            "written amendment."
        ),
        standard_language=(
            "No amendment to this Agreement shall be valid unless made in writing and "
            "signed by authorized representatives of both parties. Unilateral amendments "
            "posted to a website do not constitute a valid amendment under this Agreement."
        ),
    ),
    # F6 — limitation_liability: 3-month cap is extremely low (medium, risky)
    FaultEntry(
        fault_id="F6",
        fault_type="risky_clause",
        section="limitation_liability",
        clause_id="liability_cap_three_months",
        risk_level="medium",
        description=(
            "Vendor's liability is capped at only 3 months of fees paid — half the "
            "12-month cap that is standard in the industry. For an annual subscription "
            "this means Vendor's maximum exposure is 25% of the contract value, "
            "regardless of the magnitude of data breach or service failure. This is "
            "particularly problematic given the broad data rights granted to Vendor "
            "in Sections 5.3 and 4.3."
        ),
        standard_language=(
            "Vendor's total aggregate liability shall not exceed fees paid in the "
            "twelve (12) months preceding the claim. For claims arising from data "
            "breaches or IP infringement, the cap shall be no less than 24 months of fees."
        ),
    ),
    # F7 — TRAP: Customer warranty in 6.3 is reasonable and standard
    FaultEntry(
        fault_id="F7",
        fault_type="risky_clause",
        section="warranties",
        clause_id="customer_data_warranty",
        risk_level="low",
        description=(
            "Customer's warranty that it has rights to the data it uploads (Section 6.3) "
            "is entirely standard in SaaS agreements and not adversarial. NOT a red flag."
        ),
        is_trap=True,
    ),
    # F8 — TRAP: Vendor's bankruptcy termination right is standard
    FaultEntry(
        fault_id="F8",
        fault_type="risky_clause",
        section="term_termination",
        clause_id="bankruptcy_termination",
        risk_level="low",
        description=(
            "Vendor's right to terminate immediately upon Customer bankruptcy (Section 8.4) "
            "is a standard ipso facto clause in SaaS contracts. While technically subject "
            "to bankruptcy automatic stay, its presence is not adversarial drafting. NOT a red flag."
        ),
        is_trap=True,
    ),
    # F9 — TRAP: Vendor's free assignment right looks risky but context matters
    FaultEntry(
        fault_id="F9",
        fault_type="risky_clause",
        section="general",
        clause_id="vendor_free_assignment",
        risk_level="low",
        description=(
            "Section 9.6 allows Vendor to freely assign the Agreement without Customer "
            "consent. While this is less favorable than a mutual consent requirement, "
            "free assignment by SaaS vendors is market standard, particularly on change "
            "of control. The real issues in this agreement are elsewhere. NOT a primary red flag."
        ),
        is_trap=True,
    ),
]


# ================================================================== #
#  HARD — 20-page M&A Term Sheet
#  9 real faults including cross-section and definitional/layered faults. 5 traps.
# ================================================================== #

MA_SECTIONS: Dict[str, str] = {
    "transaction_summary": """
TERM SHEET — ACQUISITION OF NOVA SYSTEMS INC.

This non-binding Term Sheet outlines the proposed acquisition of Nova Systems Inc.
("Target") by Meridian Capital Partners ("Acquirer"). Execution of definitive
agreements is subject to satisfactory completion of due diligence, board approval,
and regulatory clearance.

Purchase Price: $42,000,000 (forty-two million USD)
Structure: Asset purchase
Closing Target: 90 days from signing of definitive agreement
Exclusivity: 60-day no-shop period commencing on execution of this Term Sheet
""".strip(),

    "definitions": """
DEFINITIONS

For purposes of this Term Sheet and any definitive agreement:

"ARR" has the meaning set forth in Schedule B.
"Business Day" means any day other than Saturday, Sunday, or a U.S. federal holiday.
"Closing" means the consummation of the transactions contemplated herein.
"Earnout Period" means the 24-month period commencing on the Closing Date.
"Fundamental Representations" means representations relating to title, authority,
    capitalization, taxes (but not including deferred revenue tax treatment), and fraud.
"Key Employees" means the individuals listed in Schedule D.
"Material Adverse Effect" or "MAE" means any event, circumstance, or development that
    has or would reasonably be expected to have a material adverse effect on the business,
    operations, financial condition, or prospects of Target, taken as a whole, excluding
    effects resulting from: (i) general economic conditions; (ii) conditions affecting
    the industry generally; (iii) changes in law or regulation; (iv) the announcement of
    this transaction; or (v) acts of war or terrorism.
"Working Capital" means current assets minus current liabilities as calculated by
    Acquirer in accordance with Acquirer's accounting policies, which may differ from
    Target's historical accounting policies.
""".strip(),

    "purchase_price_adjustment": """
PURCHASE PRICE AND ADJUSTMENTS

2.1 Base Purchase Price: $42,000,000, subject to adjustment as set forth herein.
2.2 Working Capital Adjustment: Purchase price shall be adjusted dollar-for-dollar
    for deviations from Target Working Capital of $3,200,000 at Closing, calculated
    per the definition of "Working Capital" in Section 1.
2.3 Earnout: An additional $5,000,000 shall be payable if the acquired business
    achieves $18,000,000 in Annual Recurring Revenue within the Earnout Period,
    measured in accordance with Schedule B.
2.4 Escrow: $4,200,000 (10% of Base Purchase Price) shall be held in escrow for
    18 months to cover indemnification claims.
2.5 Deferred Consideration: $2,000,000 of the Base Purchase Price shall be withheld
    pending delivery of audited financial statements acceptable to Acquirer. If
    audited financials reveal a revenue recognition discrepancy exceeding 5%,
    the deferred consideration shall be forfeited in its entirety.
""".strip(),

    "representations_warranties": """
REPRESENTATIONS AND WARRANTIES

3.1 Target makes standard representations and warranties regarding: corporate
    organization; authority to execute; capitalization; financial statements
    (prepared in accordance with GAAP); absence of material changes; compliance
    with laws; material contracts; intellectual property; employee matters;
    and litigation.
3.2 Survival: Representations and warranties shall survive Closing for 18 months,
    except for Fundamental Representations which shall survive until the applicable
    statute of limitations.
3.3 Acquirer makes standard representations and warranties regarding its authority,
    financing capability, and regulatory standing.
3.4 Target's IP representations in Section 3.1 are made without reference to or
    qualification by Schedule A. Target affirms that no material IP used in its
    business is subject to open-source copyleft licenses requiring disclosure of
    third-party proprietary code upon distribution.
""".strip(),

    "indemnification": """
INDEMNIFICATION

4.1 Target Indemnification: Target shareholders shall indemnify Acquirer for losses
    arising from breaches of representations, warranties, or covenants.
4.2 Basket: Indemnification claims shall be subject to a tipping basket of $420,000
    (1% of Base Purchase Price). Once the basket is exceeded, claims are recoverable
    from the first dollar.
4.3 Cap: Indemnification claims (excluding Fundamental Representations) shall be
    capped at the Escrow Amount ($4,200,000). Claims for Fundamental Representations
    shall be capped at the Base Purchase Price.
4.4 Sole Remedy: Indemnification shall be the sole and exclusive remedy for breaches
    of representations and warranties, except in cases of fraud.
4.5 Sandbagging: Acquirer's right to indemnification shall not be affected by any
    investigation conducted by Acquirer or any knowledge Acquirer may have acquired
    prior to Closing regarding the accuracy of any representation or warranty.
    Target shall have no defense based on Acquirer's actual or constructive knowledge.
""".strip(),

    "intellectual_property": """
INTELLECTUAL PROPERTY ASSIGNMENT

5.1 At Closing, Target shall assign to Acquirer all rights in the Target IP,
    including patents, trademarks, copyrights, trade secrets, and software.
5.2 Key employees listed in Schedule D shall execute invention assignment and
    non-compete agreements as a condition of Closing.
5.3 Target represents that it has valid ownership or licenses to all IP used in
    its business and that no IP is subject to open-source licenses that would
    require disclosure of Acquirer's proprietary code upon combination or distribution.
    [Note: See Schedule A for IP exceptions disclosed by Target.]
""".strip(),

    "employee_matters": """
EMPLOYEE MATTERS

6.1 Acquirer intends to offer employment to substantially all of Target's employees
    on terms no less favorable than current compensation for a period of ninety (90) days.
6.2 Target's CEO and CTO shall enter into 24-month employment agreements with
    Acquirer as a condition of Closing (see Schedule E for terms).
6.3 All employee obligations, including accrued PTO, severance, and benefits
    through Closing, shall be Target's responsibility.
6.4 Acquirer shall have no obligation to maintain any employee benefit plan currently
    offered by Target. Employees transitioning to Acquirer shall be enrolled in
    Acquirer's standard benefit plans, which may provide materially different coverage.
6.5 For employees not offered employment by Acquirer, Target shall be solely responsible
    for all severance and WARN Act obligations.
""".strip(),

    "conditions_closing": """
CONDITIONS TO CLOSING

7.1 Conditions to Acquirer's obligations:
    (a) Representations and warranties true and correct in all material respects;
    (b) No Material Adverse Effect since the date of this Term Sheet;
    (c) Receipt of all required regulatory approvals;
    (d) Execution of employment agreements by Key Employees;
    (e) Completion of satisfactory due diligence in Acquirer's sole and absolute
        discretion, with no obligation to proceed if Acquirer is not satisfied
        for any reason whatsoever.
7.2 Conditions to Target's obligations:
    (a) Acquirer representations true and correct in all material respects;
    (b) Acquirer has delivered the Purchase Price at Closing.
7.3 Outside Date: If Closing has not occurred within 180 days of the date of this
    Term Sheet, either party may terminate. No break-up fee or reverse termination
    fee is payable upon termination under this Section 7.3.
""".strip(),

    "exclusivity_no_shop": """
EXCLUSIVITY AND NO-SHOP

8.1 Upon execution of this Term Sheet, Target agrees to a 60-day exclusivity period
    during which Target shall not solicit, initiate, or participate in any discussions
    with other potential acquirers.
8.2 This exclusivity obligation is binding and legally enforceable notwithstanding
    the non-binding nature of other provisions of this Term Sheet.
8.3 If Target breaches the exclusivity obligation, Target shall pay Acquirer a
    break-up fee of $2,100,000 (5% of Base Purchase Price) as liquidated damages.
8.4 No reciprocal obligation is imposed on Acquirer. During the exclusivity period,
    Acquirer may continue to negotiate with, and ultimately acquire, other targets
    in the same industry without restriction or disclosure to Target.
""".strip(),

    "financing": """
FINANCING

9.1 Acquirer represents that it has received a financing commitment letter from
    First National Capital sufficient to fund the Base Purchase Price.
9.2 The financing commitment is subject to customary conditions including satisfactory
    due diligence by the lender, absence of a market disruption event as determined
    by the lender in its sole discretion, and final credit committee approval.
9.3 If Acquirer's financing fails for any reason, Acquirer may terminate this
    Agreement with no liability to Target, provided Acquirer gives Target written
    notice of such termination within five (5) Business Days of the financing failure.
9.4 No reverse termination fee or other compensation is payable to Target in the
    event of a financing failure.
""".strip(),

    "tax_matters": """
TAX MATTERS

10.1 The transaction is structured as an asset purchase. Target shareholders shall
     bear all income taxes arising from the transaction.
10.2 Deferred revenue that has been recognized by Target for accounting purposes
     but not yet earned may be treated as taxable income at Closing by the IRS.
     The parties have not agreed on which party bears this deferred revenue tax
     liability, and it is not addressed in the Working Capital definition or
     Fundamental Representations.
10.3 Any transfer taxes arising from the asset purchase shall be shared equally
     by the parties.
10.4 Acquirer shall have sole authority over all tax filings post-Closing, including
     the right to amend any pre-Closing period tax returns, and shall not require
     Target shareholder consent for such amendments.
""".strip(),

    "schedule_a_open_source": """
SCHEDULE A — INTELLECTUAL PROPERTY EXCEPTIONS

A.1 The following components of Target's software stack incorporate open-source
    software licensed under the GNU General Public License v3 (GPLv3):
      - DataSync Engine v2.1 (core data synchronization module)
      - ReportBuilder v1.4 (customer-facing reporting module)

    These components together constitute approximately 34% of Target's codebase
    by lines of code. Under GPLv3, any distribution of software incorporating
    these components may trigger copyleft obligations requiring disclosure of
    Acquirer's proprietary source code.

A.2 Target has not obtained commercial licenses for the above components.
    Target's legal counsel has opined that current use is internal and does
    not trigger distribution obligations. However, if Acquirer distributes
    the combined software to customers (as Acquirer's current business model
    requires), copyleft obligations will likely be triggered.

A.3 Remediation options: (a) obtain commercial licenses from copyright holders
    (estimated cost $180,000–$400,000), or (b) rewrite affected modules
    (estimated 8–14 months of engineering effort).

A.4 Target's IP representations in Section 3.4 of the Term Sheet state that no
    material IP is subject to copyleft licenses. Schedule A contradicts this
    representation. No qualification or cross-reference corrects Section 3.4.
""".strip(),

    "schedule_b_earnout_definition": """
SCHEDULE B — EARNOUT DEFINITIONS

B.1 "Annual Recurring Revenue" (ARR) for purposes of the Earnout shall mean
    the annualized value of recurring subscription contracts in force as of
    the measurement date, excluding:
      (i)   one-time implementation or professional services fees;
      (ii)  contracts with remaining term less than six (6) months;
      (iii) contracts originated through channel partners unless approved
            by Acquirer's CFO in writing prior to contract execution;
      (iv)  any customer contract that Acquirer elects to terminate or
            not renew post-Closing, regardless of the reason for non-renewal.

B.2 ARR shall be calculated by Acquirer in its sole and absolute discretion.
    Target's representative may audit the calculation within 30 days of Acquirer's
    delivery of the ARR statement. Audit findings are advisory only — Acquirer's
    calculation is final and binding.

B.3 During the Earnout period, Acquirer shall not take actions with the primary
    purpose of avoiding the Earnout payment. Acquirer may, however, make ordinary
    course business decisions — including pricing changes, product retirements,
    and go-to-market restructuring — without regard to Earnout impact.

B.4 No interest shall accrue on the Earnout amount during the measurement period.
""".strip(),

    "schedule_c_working_capital": """
SCHEDULE C — WORKING CAPITAL METHODOLOGY

C.1 Working Capital shall be calculated using Acquirer's standard methodology,
    which differs from GAAP in the following respects:
      (a) Deferred revenue shall be included as a current liability at full face
          value, rather than at the GAAP amortized amount;
      (b) Customer deposits held by Target shall be excluded from current assets;
      (c) Unbilled receivables (ARR contracted but not yet invoiced) shall be
          excluded from current assets.

C.2 Target acknowledges that it has not reviewed or approved Acquirer's accounting
    methodology set forth in C.1, and that application of such methodology may
    reduce the calculated Working Capital figure materially compared to Target's
    own GAAP-based calculations.

C.3 If the Working Capital at Closing, calculated per C.1, is below the target
    of $3,200,000, the purchase price shall be reduced dollar-for-dollar. If
    Working Capital exceeds $3,200,000, no upward adjustment shall be made.

C.4 Acquirer's accounting firm shall perform the final Working Capital calculation.
    Target may dispute the calculation within 15 days, but dispute resolution shall
    be by Acquirer's accounting firm's senior partner, whose determination is final.
""".strip(),
}

MA_FAULTS: List[FaultEntry] = [
    # F1 — schedule_a_open_source: GPLv3 copyleft risk not remediated before closing (critical, risky)
    FaultEntry(
        fault_id="F1",
        fault_type="risky_clause",
        section="schedule_a_open_source",
        clause_id="gplv3_copyleft_risk",
        risk_level="critical",
        description=(
            "Schedule A discloses that 34% of Target's codebase uses GPLv3 components "
            "without commercial licenses. Acquirer's distribution model will trigger "
            "copyleft obligations, potentially requiring open-sourcing of Acquirer's "
            "proprietary code. Remediation costs $180K–$400K or 8–14 months of engineering. "
            "No closing condition requires remediation or price adjustment."
        ),
        standard_language=(
            "IP representations should be qualified to disclose Schedule A. A closing "
            "condition should require Target to obtain commercial licenses or complete "
            "rewrites before Closing, with a purchase price adjustment if deferred, "
            "and an indemnification carve-out for this specific pre-identified risk."
        ),
    ),
    # F2 — representations_warranties + schedule_a: cross-section contradiction (critical, risky)
    FaultEntry(
        fault_id="F2",
        fault_type="risky_clause",
        section="representations_warranties",
        clause_id="ip_rep_contradicts_schedule_a",
        risk_level="critical",
        description=(
            "Section 3.4 contains an unqualified representation that no material IP is "
            "subject to copyleft licenses requiring code disclosure — but Schedule A.4 "
            "explicitly discloses that 34% of the codebase is GPLv3 and acknowledges "
            "this representation is inaccurate. The rep is not qualified by reference to "
            "Schedule A, meaning Target is making a representation it knows to be false. "
            "This creates a breach at closing and potential fraud exposure."
        ),
        standard_language=(
            "Section 3.4 should be qualified: '...except as set forth in Schedule A.' "
            "Alternatively, Section 3.4 should be deleted and the GPLv3 exposure "
            "addressed entirely through a specific indemnity and closing condition."
        ),
    ),
    # F3 — schedule_b_earnout_definition: earnout structure manipulable (medium, risky)
    FaultEntry(
        fault_id="F3",
        fault_type="risky_clause",
        section="schedule_b_earnout_definition",
        clause_id="earnout_acquirer_discretion",
        risk_level="medium",
        description=(
            "Schedule B gives Acquirer sole and absolute discretion to calculate ARR, "
            "with audit findings advisory only. The exclusion of channel partner contracts "
            "without CFO pre-approval and customer contracts that Acquirer elects not to "
            "renew (B.1.iv) gives Acquirer structural mechanisms to suppress ARR and "
            "avoid the $5M earnout payment entirely."
        ),
        standard_language=(
            "ARR should be calculated per mutually agreed methodology using an independent "
            "accountant. Acquirer should be prohibited from restructuring sales channels "
            "or declining renewals during the earnout period in ways that reduce ARR. "
            "Audit rights should be binding, not advisory."
        ),
    ),
    # F4 — conditions_closing: no break-up fee / reverse termination fee (medium, missing)
    FaultEntry(
        fault_id="F4",
        fault_type="missing_clause",
        section="conditions_closing",
        clause_id="reverse_termination_fee",
        risk_level="medium",
        description=(
            "Section 7.3 explicitly provides that no break-up fee or reverse termination "
            "fee is payable if the deal fails to close. Combined with the financing "
            "contingency in Section 9 (where Acquirer bears no liability for financing "
            "failure), Target has no financial protection if Acquirer walks away after "
            "Target has been locked up in exclusivity for 60 days and spent significant "
            "resources on the transaction."
        ),
        standard_language=(
            "Acquirer shall pay Target a reverse termination fee of 3–5% of the Base "
            "Purchase Price if Acquirer fails to close when all of Target's conditions "
            "to Closing have been satisfied, including for financing failure. The fee "
            "shall be Target's sole remedy in such circumstances."
        ),
    ),
    # F5 — financing: no-liability financing out (critical, risky)
    FaultEntry(
        fault_id="F5",
        fault_type="risky_clause",
        section="financing",
        clause_id="financing_out_no_liability",
        risk_level="critical",
        description=(
            "Section 9.3 allows Acquirer to terminate for financing failure with no "
            "liability to Target. The financing commitment (Section 9.1) is subject "
            "to lender discretion, a market disruption exception, and final credit "
            "committee approval — all of which are outside Acquirer's control and "
            "potentially outside objective standards. This effectively gives Acquirer "
            "a no-cost option to walk away from the deal at any time before Closing."
        ),
        standard_language=(
            "Acquirer should be required to use reasonable best efforts to obtain and "
            "maintain financing. If financing fails, a reverse termination fee of no less "
            "than 4% of the Base Purchase Price should be payable to Target as liquidated damages."
        ),
    ),
    # F6 — schedule_c_working_capital: non-GAAP WC methodology biased against Target (medium, risky)
    FaultEntry(
        fault_id="F6",
        fault_type="risky_clause",
        section="schedule_c_working_capital",
        clause_id="non_gaap_working_capital_methodology",
        risk_level="medium",
        description=(
            "Schedule C defines Working Capital using Acquirer's non-GAAP methodology, "
            "which inflates current liabilities (full deferred revenue vs. GAAP amortized) "
            "and excludes favorable assets (customer deposits, unbilled receivables). "
            "Target has not reviewed or approved this methodology. A one-sided adjustment "
            "mechanism (downward only, per C.3) ensures only Acquirer benefits from "
            "discrepancies. Dispute resolution is handled by Acquirer's own accounting firm."
        ),
        standard_language=(
            "Working Capital shall be calculated on a consistent basis with Target's "
            "historical GAAP accounting. Any disputes shall be resolved by a mutually "
            "agreed independent accounting firm, whose determination shall be binding on both parties."
        ),
    ),
    # F7 — tax_matters: deferred revenue tax liability unallocated (medium, missing)
    FaultEntry(
        fault_id="F7",
        fault_type="missing_clause",
        section="tax_matters",
        clause_id="deferred_revenue_tax_allocation",
        risk_level="medium",
        description=(
            "Section 10.2 acknowledges that deferred revenue may trigger taxable income "
            "at Closing but expressly states the parties have not agreed on who bears "
            "this liability. It is excluded from Fundamental Representations and not "
            "addressed in the Working Capital definition. For a SaaS business, deferred "
            "revenue tax exposure can be substantial (potentially $1M+). Leaving it "
            "unallocated in the definitive agreement is a significant structural gap."
        ),
        standard_language=(
            "The parties shall agree prior to signing definitive agreements on the "
            "allocation of deferred revenue tax liability. Target shareholders shall "
            "bear pre-Closing deferred revenue tax obligations, with a corresponding "
            "adjustment to the Working Capital target or an indemnification obligation."
        ),
    ),
    # F8 — indemnification: pro-sandbagging provision (medium, risky)
    FaultEntry(
        fault_id="F8",
        fault_type="risky_clause",
        section="indemnification",
        clause_id="pro_sandbagging",
        risk_level="medium",
        description=(
            "Section 4.5 is a strongly pro-sandbagging clause: Acquirer can proceed "
            "to Closing with knowledge of a representation breach (e.g., the GPLv3 "
            "issue disclosed in Schedule A) and still bring an indemnification claim "
            "post-Closing for that known breach. Combined with Section 3.4's unqualified "
            "IP representation, Acquirer could knowingly close with the GPLv3 exposure "
            "and later sue for indemnification based on a rep it knew was false at signing. "
            "This creates perverse incentives and disputes."
        ),
        standard_language=(
            "Acquirer may not bring an indemnification claim for any breach of which "
            "Acquirer had actual knowledge prior to Closing. Known exceptions disclosed "
            "in the Schedules shall be handled through purchase price adjustment or "
            "specific indemnities, not general rep-and-warranty claims."
        ),
    ),
    # F9 — exclusivity_no_shop: asymmetric exclusivity, Acquirer has no reciprocal lock-up (medium, risky)
    FaultEntry(
        fault_id="F9",
        fault_type="risky_clause",
        section="exclusivity_no_shop",
        clause_id="asymmetric_exclusivity",
        risk_level="medium",
        description=(
            "Section 8.4 explicitly allows Acquirer to negotiate with and acquire "
            "competing targets during the exclusivity period without restriction or "
            "disclosure to Target. Target is locked up with a $2.1M break-up fee "
            "obligation and cannot seek alternative buyers, while Acquirer can freely "
            "pursue alternatives. This asymmetry is non-standard and leaves Target "
            "in a highly exposed position."
        ),
        standard_language=(
            "Exclusivity should be mutual: Acquirer should be prohibited from "
            "negotiating the acquisition of any substantially similar competing business "
            "during the exclusivity period. If Acquirer requires one-sided exclusivity, "
            "the break-up fee structure should be reciprocal."
        ),
    ),
    # T1 — TRAP: 1% tipping basket is market standard
    FaultEntry(
        fault_id="T1",
        fault_type="risky_clause",
        section="indemnification",
        clause_id="tipping_basket",
        risk_level="low",
        description=(
            "1% tipping basket ($420,000) is standard for an M&A deal of this size. NOT a red flag."
        ),
        is_trap=True,
    ),
    # T2 — TRAP: 18-month survival is within market range
    FaultEntry(
        fault_id="T2",
        fault_type="risky_clause",
        section="representations_warranties",
        clause_id="survival_period",
        risk_level="low",
        description=(
            "18-month survival for general reps is within market range for a SaaS M&A "
            "of this size. NOT a genuine red flag."
        ),
        is_trap=True,
    ),
    # T3 — TRAP: 10% escrow holdback is standard
    FaultEntry(
        fault_id="T3",
        fault_type="missing_clause",
        section="purchase_price_adjustment",
        clause_id="escrow_percentage",
        risk_level="low",
        description=(
            "10% escrow ($4.2M) for 18 months is entirely standard in M&A transactions "
            "of this size. NOT a red flag — this is the expected market structure."
        ),
        is_trap=True,
    ),
    # T4 — TRAP: Sole remedy clause is standard M&A carve-out
    FaultEntry(
        fault_id="T4",
        fault_type="risky_clause",
        section="indemnification",
        clause_id="sole_remedy_clause",
        risk_level="low",
        description=(
            "Section 4.4 limits remedies to indemnification except for fraud. This is "
            "entirely standard M&A practice and is not adversarial. NOT a red flag."
        ),
        is_trap=True,
    ),
    # T5 — TRAP: Key employee non-competes are expected in M&A
    FaultEntry(
        fault_id="T5",
        fault_type="risky_clause",
        section="intellectual_property",
        clause_id="key_employee_noncompete",
        risk_level="low",
        description=(
            "Requiring Key Employees to sign invention assignment and non-compete "
            "agreements as a Closing condition (Section 5.2) is standard in technology "
            "M&A. NOT a red flag — this is expected deal structure."
        ),
        is_trap=True,
    ),
]


# ================================================================== #
#  Registry
# ================================================================== #

TASK_CONFIGS = {
    "easy": {
        "title": "Mutual NDA — Acme Corp / Beta Ventures",
        "description": (
            "Review a one-page mutual NDA for missing protective clauses, "
            "non-standard terms, and unfavorable provisions before signing. "
            "Faults are distributed across multiple sections."
        ),
        "sections": NDA_SECTIONS,
        "faults": NDA_FAULTS,
        "difficulty": "easy",
        "total_faults": len([f for f in NDA_FAULTS if not f.is_trap]),
    },
    "medium": {
        "title": "SaaS Subscription Agreement — Vendor / Customer",
        "description": (
            "Review an 8-page SaaS agreement for predatory clauses, missing SLA "
            "commitments, non-standard IP terms, and cross-section interactions. "
            "Some clauses appear standard but are traps."
        ),
        "sections": SAAS_SECTIONS,
        "faults": SAAS_FAULTS,
        "difficulty": "medium",
        "total_faults": len([f for f in SAAS_FAULTS if not f.is_trap]),
    },
    "hard": {
        "title": "M&A Term Sheet — Meridian Capital / Nova Systems",
        "description": (
            "Review a 20-page M&A term sheet for risks, missing protections, "
            "cross-section contradictions, and definitional traps. Several clauses "
            "look risky but are market standard — accurate discrimination is required. "
            "Some faults require reading multiple sections together."
        ),
        "sections": MA_SECTIONS,
        "faults": MA_FAULTS,
        "difficulty": "hard",
        "total_faults": len([f for f in MA_FAULTS if not f.is_trap]),
    },
}