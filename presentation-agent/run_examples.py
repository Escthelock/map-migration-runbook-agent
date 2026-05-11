"""Sample invocation — demonstrates how partners use the Presentation Generator Agent.

This script shows all 4 document types using AnyCompany sample data.
Run: python run_examples.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from presentation_agent import run_agent

# --- Sample context (AnyCompany healthcare migration) ---

ANYCOMPANY_CONTEXT = """
Customer: AnyCompany (Healthcare)
Partner: AnyTech Cloud Solutions
Programme: AWS MAP Migration — 20 applications, 800TB+ data, 14-month programme

## Portfolio Summary
- 20 applications total
- Critical/Tier 1: 7 (EHR, Patient Portal, Clinical Data Warehouse, Revenue Cycle, HIE, EHR Analytics, Claims Processing, Medical Device Hub)
- High/Tier 2: 8 (Pharmacy Mgmt, RIS, LIS, Patient Scheduling, Medical Imaging, Clinical Decision Support, Telemedicine, Compliance & Audit)
- Medium/Tier 3: 5 (Medical Supply Chain, Nurse Workforce, Research Data Repo, Patient Discharge, DEV/TEST)

## Infrastructure
- 20 servers (VMware virtualised), 244 vCPU, 1.5TB RAM (production)
- Storage: SAN 100TB, NAS 200TB, Object (MinIO) 500TB = 800TB+ total
- 3 shared infrastructure concentration risks identified

## MRA Scores
- Business & Strategy: 4.5/5.0
- People & Process: 2.8/5.0
- Platform & Architecture: 2.5/5.0
- Security & Compliance: 3.0/5.0
- Operations & Management: 3.5/5.0
- Migration Experience: 2.0/5.0
- Overall: 3.1/5.0 (Moderate Readiness)

## 6Rs Distribution
- Replatform: 11 apps (55%)
- Refactor: 5 apps (25%)
- Rehost: 2 apps (10%)
- Retire: 1 app (5%)
- Retain: 1 app (5%)

## Wave Plan
- Wave 0 (Weeks 1-6): Foundation — landing zone, tooling, training
- Wave 1 (Weeks 7-14): 4 low-risk apps (Medical Supply Chain, Patient Discharge, Telemedicine DEV, Research Data Repo DEV)
- Wave 2 (Weeks 15-26): 6 Tier-2 clinical apps (Pharmacy, Medical Imaging, RIS, LIS, Patient Scheduling, Nurse Workforce)
- Wave 3 (Weeks 27-40): 5 core platform apps (Patient Portal, HIE, Clinical Decision Support, Compliance & Audit, Medical Device Hub)
- Wave 4 (Weeks 41-56): 5 mission-critical apps (EHR, Revenue Cycle, Claims Processing, Clinical Data Warehouse, EHR Analytics)

## MAP Funding
- MAP application submitted and approved
- $50K milestone projected: Migrate Month 1 (cumulative $63K)
- Monthly spend projection: $8K → $12K → $18K → $25K → $30K+

## Migration Drivers
- 5 legacy/EOL applications (Java 8, COBOL, ASP.NET 4.8, C# 6.0/.NET 4.6)
- HIPAA compliance and data sovereignty
- Scalability for clinical workloads
- Cost optimisation (VMware licensing, hardware refresh)

## Compliance Requirements
- HIPAA (patient data protection)
- HL7 FHIR R4 / HL7 v2.8 (clinical interoperability)
- DICOM 3.0 (medical imaging)
- EDI X12 (claims and billing)

## Current Phase: Assess (Complete)
- All deliverables complete
- MRA submitted to AWS
- Business case approved by executive sponsor
- GO decision achieved — proceeding to Mobilize
"""


def example_executive_summary():
    """Generate an executive summary for AnyCompany."""
    print("=" * 60)
    print("EXAMPLE 1: Executive Summary")
    print("=" * 60)
    result = run_agent("executive_summary", ANYCOMPANY_CONTEXT, customer="AnyCompany")
    print(result)
    print()


def example_phase_status():
    """Generate a phase status report for the Assess phase."""
    print("=" * 60)
    print("EXAMPLE 2: Phase Status Report (Assess)")
    print("=" * 60)
    result = run_agent("phase_status", ANYCOMPANY_CONTEXT, phase="assess", customer="AnyCompany")
    print(result)
    print()


def example_go_nogo():
    """Generate a GO/NO-GO decision pack for Assess → Mobilize gate."""
    print("=" * 60)
    print("EXAMPLE 3: GO/NO-GO Decision Pack (Assess → Mobilize)")
    print("=" * 60)
    result = run_agent("go_nogo", ANYCOMPANY_CONTEXT, phase="assess", customer="AnyCompany")
    print(result)
    print()


def example_map_milestone():
    """Generate a MAP milestone tracking document."""
    print("=" * 60)
    print("EXAMPLE 4: MAP Milestone Tracking")
    print("=" * 60)
    result = run_agent("map_milestone", ANYCOMPANY_CONTEXT, customer="AnyCompany")
    print(result)
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run presentation agent examples")
    parser.add_argument("--example", choices=["all", "executive", "status", "gonogo", "milestone"], default="all")
    args = parser.parse_args()

    examples = {
        "executive": example_executive_summary,
        "status": example_phase_status,
        "gonogo": example_go_nogo,
        "milestone": example_map_milestone,
    }

    if args.example == "all":
        for fn in examples.values():
            fn()
    else:
        examples[args.example]()
