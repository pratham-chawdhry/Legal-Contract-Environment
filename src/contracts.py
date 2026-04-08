"""
contracts.py — Synthetic contract generator with injected fault manifests.
All contracts are entirely fictional. Ground truth is programmatically defined.
"""
from __future__ import annotations
from typing import Dict, List
from src.models import FaultEntry


# ================================================================== #
#  EASY — 1-page NDA
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
either party, whether orally, in writing, or by inspection of tangible
objects, that is designated as confidential or that reasonably should be
understood to be confidential given the nature of the information and
circumstances of disclosure. This includes, but is not limited to, trade
secrets, business plans, financial data, technical specifications, and
customer lists.
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

    "term": """
TERM

This Agreement shall remain in effect for a period of two (2) years from
the Effective Date, unless earlier terminated by either party upon thirty
(30) days written notice.
""".strip(),

    "governing_law": """
GOVERNING LAW

This Agreement shall be governed by and construed in accordance with the
laws of the State of Delaware, without regard to its conflict of law provisions.
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
    FaultEntry(
        fault_id="F1",
        fault_type="missing_clause",
        section="obligations",
        clause_id="liability_cap",
        risk_level="critical",
        description=(
            "No liability cap exists. The indemnification clause in section "
            "'obligations' is unlimited — the Receiving Party bears infinite "
            "financial exposure for any breach."
        ),
        standard_language=(
            "IN NO EVENT SHALL EITHER PARTY'S TOTAL LIABILITY EXCEED "
            "THE GREATER OF (A) $50,000 OR (B) AMOUNTS PAID IN THE "
            "PRIOR 12 MONTHS UNDER THIS AGREEMENT."
        ),
    ),
    FaultEntry(
        fault_id="F2",
        fault_type="risky_clause",
        section="obligations",
        clause_id="unlimited_indemnity",
        risk_level="critical",
        description=(
            "The indemnification clause (section 'obligations', paragraph starting "
            "'The Receiving Party shall defend...') imposes unlimited, one-sided "
            "indemnity with no carve-outs, no notice requirement, and no right to "
            "control defense. This is non-standard and highly unfavorable."
        ),
        standard_language=(
            "Each party shall indemnify the other for direct damages caused by its "
            "material breach, subject to the liability cap in Section X, provided "
            "the indemnified party gives prompt written notice and cooperates in defense."
        ),
    ),
]


# ================================================================== #
#  MEDIUM — 8-page SaaS Agreement
# ================================================================== #

SAAS_SECTIONS: Dict[str, str] = {
    "definitions": """
DEFINITIONS

1.1 "Agreement" means this Software as a Service Agreement including all Schedules.
1.2 "Authorized Users" means employees of Customer permitted to access the Service.
1.3 "Customer Data" means all data submitted by Customer through the Service.
1.4 "Documentation" means the user guides and technical specifications provided by Vendor.
1.5 "Service" means Vendor's cloud-based platform described in Schedule A.
1.6 "Subscription Term" means the Initial Term and any Renewal Terms as further described
    in Section 9.2. Unless Customer provides written notice of non-renewal no less than
    thirty (30) days prior to the end of the then-current Subscription Term, this Agreement
    shall automatically renew for successive one (1) year periods at Vendor's then-current
    list price, which may be increased by up to fifteen percent (15%) upon renewal without
    further notice.
""".strip(),

    "license_grant": """
LICENSE GRANT

2.1 Subject to the terms of this Agreement and payment of applicable fees, Vendor grants
    Customer a non-exclusive, non-transferable, limited license to access and use the
    Service during the Subscription Term solely for Customer's internal business purposes.
2.2 Customer may not: (a) sublicense, sell, or transfer the Service; (b) reverse engineer
    or attempt to derive source code; (c) use the Service to build a competing product.
""".strip(),

    "fees_payment": """
FEES AND PAYMENT

3.1 Customer shall pay all fees set forth in Schedule B within thirty (30) days of invoice.
3.2 All fees are non-refundable except as expressly set forth herein.
3.3 Vendor reserves the right to suspend access upon thirty (30) days written notice for
    past due amounts exceeding sixty (60) days.
3.4 Fees are exclusive of taxes; Customer is responsible for all applicable taxes.
""".strip(),

    "data_privacy": """
DATA PRIVACY AND SECURITY

4.1 Vendor shall implement and maintain reasonable administrative, technical, and physical
    safeguards designed to protect Customer Data.
4.2 Vendor shall notify Customer of any confirmed security breach affecting Customer Data
    within seventy-two (72) hours of Vendor becoming aware of such breach.
4.3 Vendor may use Customer Data in aggregated, anonymized form to improve its services.
4.4 Upon termination, Vendor shall delete Customer Data within ninety (90) days unless
    legally required to retain it.
""".strip(),

    "intellectual_property": """
INTELLECTUAL PROPERTY

5.1 Vendor retains all right, title, and interest in the Service and Documentation.
5.2 Customer retains all right, title, and interest in Customer Data.
5.3 Customer hereby grants Vendor a worldwide, royalty-free license to use Customer Data
    to provide and improve the Service. This license is irrevocable and survives termination
    of this Agreement, and Vendor may sublicense this right to third-party processors
    without restriction or Customer consent.
5.4 Any feedback or suggestions provided by Customer may be used by Vendor without
    restriction or compensation.
""".strip(),

    "warranties": """
WARRANTIES AND DISCLAIMERS

6.1 Vendor warrants that the Service will perform materially in accordance with the
    Documentation during the Subscription Term.
6.2 EXCEPT AS EXPRESSLY SET FORTH IN SECTION 6.1, THE SERVICE IS PROVIDED "AS IS."
    VENDOR DISCLAIMS ALL OTHER WARRANTIES, EXPRESS OR IMPLIED.
""".strip(),

    "limitation_liability": """
LIMITATION OF LIABILITY

7.1 NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL
    DAMAGES.
7.2 VENDOR'S TOTAL AGGREGATE LIABILITY SHALL NOT EXCEED THE FEES PAID BY CUSTOMER
    IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.
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
""".strip(),

    "general": """
GENERAL PROVISIONS

9.1 Governing Law: This Agreement shall be governed by the laws of California.
9.2 Entire Agreement: This Agreement constitutes the entire agreement between the parties.
9.3 Amendments: No amendment shall be valid unless in writing signed by both parties.
9.4 Waiver: Failure to enforce any provision shall not constitute a waiver.
9.5 Severability: If any provision is unenforceable, remaining provisions continue.
""".strip(),
}

SAAS_FAULTS: List[FaultEntry] = [
    FaultEntry(
        fault_id="F1",
        fault_type="risky_clause",
        section="definitions",
        clause_id="auto_renewal_buried",
        risk_level="medium",
        description=(
            "Auto-renewal with price escalation of up to 15% is buried inside "
            "Section 1.6 (Definitions — 'Subscription Term'), not in the Term & "
            "Termination section where Customer would expect it. The 30-day "
            "non-renewal notice window is also very tight. This is a common "
            "predatory drafting pattern."
        ),
        standard_language=(
            "Auto-renewal terms and price change provisions must appear in the "
            "Term & Termination section with at least 60 days notice of non-renewal "
            "and 90 days advance notice of any price increase."
        ),
    ),
    FaultEntry(
        fault_id="F2",
        fault_type="risky_clause",
        section="intellectual_property",
        clause_id="irrevocable_data_license",
        risk_level="critical",
        description=(
            "Section 5.3 grants Vendor an irrevocable, sublicensable license to "
            "Customer Data that survives termination without restriction or consent. "
            "This is an extraordinarily broad grant — Customer cannot revoke it even "
            "after leaving the platform."
        ),
        standard_language=(
            "Any license to Customer Data should be limited to what is necessary to "
            "provide the Service, non-sublicensable without consent, and must terminate "
            "upon contract expiration with data return/deletion obligations."
        ),
    ),
    FaultEntry(
        fault_id="F3",
        fault_type="missing_clause",
        section="data_privacy",
        clause_id="sla_uptime",
        risk_level="medium",
        description=(
            "No SLA or uptime commitment exists anywhere in the agreement. Section 4 "
            "references 'reasonable safeguards' but makes no commitment to service "
            "availability, and there is no remedies section for downtime."
        ),
        standard_language=(
            "Vendor commits to 99.9% monthly uptime (excluding scheduled maintenance). "
            "For each hour of excess downtime, Customer receives a service credit of "
            "1/720th of monthly fees, up to 30% of monthly fees."
        ),
    ),
]


# ================================================================== #
#  HARD — 20-page M&A Term Sheet
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
""".strip(),

    "purchase_price_adjustment": """
PURCHASE PRICE AND ADJUSTMENTS

2.1 Base Purchase Price: $42,000,000, subject to adjustment as set forth herein.
2.2 Working Capital Adjustment: Purchase price shall be adjusted dollar-for-dollar
    for deviations from Target Working Capital of $3,200,000 at Closing.
2.3 Earnout: An additional $5,000,000 shall be payable if the acquired business
    achieves $18,000,000 in Annual Recurring Revenue within 24 months of Closing,
    measured in accordance with Schedule B.
2.4 Escrow: $4,200,000 (10% of Base Purchase Price) shall be held in escrow for
    18 months to cover indemnification claims.
""".strip(),

    "representations_warranties": """
REPRESENTATIONS AND WARRANTIES

3.1 Target makes standard representations and warranties regarding: corporate
    organization; authority to execute; capitalization; financial statements;
    absence of material changes; compliance with laws; material contracts;
    intellectual property; employee matters; and litigation.
3.2 Survival: Representations and warranties shall survive Closing for 18 months,
    except for Fundamental Representations (title, authority, capitalization, taxes,
    and fraud) which shall survive until the applicable statute of limitations.
3.3 Acquirer makes standard representations and warranties regarding its authority,
    financing capability, and regulatory standing.
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
""".strip(),

    "intellectual_property": """
INTELLECTUAL PROPERTY ASSIGNMENT

5.1 At Closing, Target shall assign to Acquirer all rights in the Target IP,
    including patents, trademarks, copyrights, trade secrets, and software.
5.2 Key employees listed in Schedule D shall execute invention assignment and
    non-compete agreements as a condition of Closing.
5.3 Target represents that it has valid ownership or licenses to all IP used in
    its business and that no IP is subject to open-source licenses that would
    require disclosure of Acquirer's proprietary code upon combination.
""".strip(),

    "employee_matters": """
EMPLOYEE MATTERS

6.1 Acquirer intends to offer employment to substantially all of Target's employees
    on terms no less favorable than current compensation for a period of 90 days.
6.2 Target's CEO and CTO shall enter into 24-month employment agreements with
    Acquirer as a condition of Closing (see Schedule E for terms).
6.3 All employee obligations, including accrued PTO, severance, and benefits
    through Closing, shall be Target's responsibility.
""".strip(),

    "conditions_closing": """
CONDITIONS TO CLOSING

7.1 Conditions to Acquirer's obligations:
    (a) Representations and warranties true and correct in all material respects;
    (b) No Material Adverse Effect since the date of this Term Sheet;
    (c) Receipt of all required regulatory approvals;
    (d) Execution of employment agreements by Key Employees;
    (e) Completion of satisfactory due diligence in Acquirer's sole discretion.
7.2 Conditions to Target's obligations:
    (a) Acquirer representations true and correct in all material respects;
    (b) Acquirer has delivered the Purchase Price at Closing.
""".strip(),

    "exclusivity_no_shop": """
EXCLUSIVITY AND NO-SHOP

8.1 Upon execution of this Term Sheet, Target agrees to a 60-day exclusivity period
    during which Target shall not solicit, initiate, or participate in any discussions
    with other potential acquirers.
8.2 This exclusivity obligation is binding and legally enforceable notwithstanding
    the non-binding nature of other provisions of this Term Sheet.
""".strip(),

    "schedule_a_open_source": """
SCHEDULE A — INTELLECTUAL PROPERTY EXCEPTIONS

A.1 The following components of the Target's software stack incorporate open-source
    software licensed under the GNU General Public License v3 (GPLv3):
      - DataSync Engine v2.1 (core data synchronization module)
      - ReportBuilder v1.4 (customer-facing reporting module)
    
    These components together constitute approximately 34% of Target's codebase
    by lines of code. Under GPLv3, any distribution of software incorporating
    these components may trigger copyleft obligations requiring disclosure of
    Acquirer's proprietary source code.

A.2 Target has not obtained commercial licenses for the above components.
    Target's legal counsel has opined that current use is internal and does
    not trigger distribution obligations, however, if Acquirer distributes
    the combined software to customers (as Acquirer's current business model
    requires), copyleft obligations may be triggered.

A.3 Remediation options: (a) obtain commercial licenses from copyright holders
    (estimated cost $180,000–$400,000), or (b) rewrite affected modules
    (estimated 8–14 months engineering effort).
""".strip(),

    "schedule_b_earnout_definition": """
SCHEDULE B — EARNOUT DEFINITIONS

B.1 "Annual Recurring Revenue" (ARR) for purposes of the Earnout shall mean
    the annualized value of recurring subscription contracts in force as of
    the measurement date, excluding:
      (i)   one-time implementation or professional services fees;
      (ii)  contracts with remaining term less than 6 months;
      (iii) contracts originated through channel partners unless approved
            by Acquirer's CFO in writing.

B.2 ARR shall be calculated by Acquirer in its sole discretion, subject to
    audit by Target's representative within 30 days of Acquirer's delivery
    of the ARR statement.

B.3 During the Earnout period, Acquirer shall not take actions with the
    primary purpose of avoiding the Earnout payment, but Acquirer may make
    ordinary course business decisions without regard to Earnout impact.

B.4 No interest shall accrue on the Earnout amount during the measurement period.
""".strip(),
}

MA_FAULTS: List[FaultEntry] = [
    FaultEntry(
        fault_id="F1",
        fault_type="risky_clause",
        section="schedule_a_open_source",
        clause_id="gplv3_copyleft_risk",
        risk_level="critical",
        description=(
            "Schedule A reveals that 34% of Target's codebase uses GPLv3-licensed "
            "components without commercial licenses. Acquirer's distribution model "
            "would trigger copyleft obligations, potentially requiring disclosure of "
            "Acquirer's proprietary source code. Remediation costs $180K–$400K or "
            "8–14 months of engineering. This is buried in Schedule A, not flagged "
            "in the IP section."
        ),
        standard_language=(
            "IP representations in Section 5.3 should be qualified to disclose "
            "Schedule A exceptions. Closing condition should require Target to either "
            "obtain commercial licenses or complete module rewrites before Closing, "
            "with a price adjustment if deferred."
        ),
    ),
    FaultEntry(
        fault_id="F2",
        fault_type="risky_clause",
        section="schedule_b_earnout_definition",
        clause_id="earnout_acquirer_discretion",
        risk_level="medium",
        description=(
            "Schedule B gives Acquirer 'sole discretion' to calculate ARR for the "
            "$5M earnout, with the audit right limited to 30 days after delivery. "
            "The exclusion of channel partner contracts without Acquirer CFO approval "
            "effectively lets Acquirer suppress ARR by redirecting deals through "
            "unapproved channels. This structure makes earnout payment avoidable."
        ),
        standard_language=(
            "ARR calculation should use a mutually agreed methodology with joint "
            "calculation rights. Acquirer should be prohibited from restructuring "
            "sales channels during the earnout period in ways that reduce measured ARR."
        ),
    ),
    FaultEntry(
        fault_id="F3",
        fault_type="missing_clause",
        section="conditions_closing",
        clause_id="rep_warranty_insurance",
        risk_level="medium",
        description=(
            "No R&W (Representations and Warranties) insurance is mentioned. For a "
            "$42M deal, R&W insurance is market standard and would allow escrow to "
            "be reduced. Its absence means the 10% escrow holdback ($4.2M) is the "
            "sole protection mechanism and sellers are exposed for the full 18-month "
            "escrow tail."
        ),
        standard_language=(
            "Acquirer shall obtain Representations and Warranties insurance covering "
            "breaches of Target's representations with a policy limit of no less than "
            "the Escrow Amount. Upon policy issuance, Escrow may be reduced to 5%."
        ),
    ),
    FaultEntry(
        fault_id="F4",
        fault_type="risky_clause",
        section="indemnification",
        clause_id="tipping_basket",
        risk_level="low",
        description=(
            "1% tipping basket ($420,000) is market standard for a deal of this size. "
            "This clause is NOT actually problematic — it is a normal M&A provision."
        ),
        is_trap=True,   # false-positive bait
    ),
    FaultEntry(
        fault_id="F5",
        fault_type="risky_clause",
        section="representations_warranties",
        clause_id="survival_period",
        risk_level="low",
        description=(
            "18-month survival for general reps is on the shorter end but within "
            "market range for a deal this size. NOT a genuine red flag — many "
            "SaaS acquisitions use 12–18 month survival periods."
        ),
        is_trap=True,   # false-positive bait
    ),
]


# ================================================================== #
#  Registry
# ================================================================== #

TASK_CONFIGS = {
    "easy": {
        "title": "Mutual NDA — Acme Corp / Beta Ventures",
        "description": (
            "Review a one-page mutual NDA for missing protective clauses "
            "and non-standard terms before signing."
        ),
        "sections": NDA_SECTIONS,
        "faults": NDA_FAULTS,
        "difficulty": "easy",
        "total_faults": len([f for f in NDA_FAULTS if not f.is_trap]),
    },
    "medium": {
        "title": "SaaS Subscription Agreement — Vendor / Customer",
        "description": (
            "Review an 8-page SaaS agreement for predatory clauses, "
            "missing SLA commitments, and non-standard IP terms."
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
            "and traps. Some clauses look risky but are market standard — "
            "accurate discrimination is required."
        ),
        "sections": MA_SECTIONS,
        "faults": MA_FAULTS,
        "difficulty": "hard",
        "total_faults": len([f for f in MA_FAULTS if not f.is_trap]),
    },
}
