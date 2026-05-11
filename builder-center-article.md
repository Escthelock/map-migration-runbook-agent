# Accelerating AWS MAP Migrations with AI-Powered Runbook Generation

## Using Generative AI to Automate Partner Delivery for the AWS Migration Acceleration Program

---

**Tags:** migration, MAP, generative-ai, strands-agents, modernization, bedrock, partner

**Level:** 300 — Advanced

**Services:** Amazon Bedrock, AWS Migration Hub, AWS Application Discovery Service

---

## Introduction

Delivering an AWS Migration Acceleration Program (MAP) engagement requires partners to produce dozens of structured documents — portfolio assessments, wave plans, cutover runbooks, executive summaries, GO/NO-GO decision packs, and MAP milestone reports. For a typical 20-application migration, this documentation effort can consume 2–4 weeks of consultant time per phase.

This article demonstrates how to use Generative AI (Amazon Bedrock + Strands Agents SDK) to automate the generation of customer-ready migration deliverables directly from raw inventory data. The approach reduces document creation from weeks to minutes while maintaining MAP methodology alignment.

**Full source code, runbooks, and sample data:** [github.com/Escthelock/map-migration-runbook-agent](https://github.com/Escthelock/map-migration-runbook-agent)

## The Problem

Partners executing MAP engagements face a repeatable challenge:

1. **Data collection** — Gather application portfolios, infrastructure inventories, and dependency maps
2. **Analysis** — Classify applications (6Rs), score readiness (MRA), plan waves
3. **Documentation** — Produce phase-specific runbooks, executive presentations, and decision packs
4. **Iteration** — Regenerate documents as scope changes or new data arrives

Steps 3 and 4 are highly repetitive and follow consistent templates. They're ideal candidates for AI automation.

## Solution Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  Customer CSVs  │────▶│ Preprocessor │────▶│  Presentation   │────▶│  Customer-Ready  │
│  (App + Infra)  │     │ (preprocess) │     │     Agent       │     │   Documents      │
└─────────────────┘     └──────────────┘     └────────┬────────┘     └──────────────────┘
                                                      │
                                               ┌──────▼──────┐
                                               │   Amazon    │
                                               │   Bedrock   │
                                               │ (Nova Pro)  │
                                               └─────────────┘
```

**Components:**

- **Preprocessor** — Python script that parses application and infrastructure CSVs into structured markdown context
- **Presentation Agent** — Strands Agents SDK agent with specialised prompts for each document type
- **Prompt Library** — Customisable system prompts defining output structure per document type
- **Amazon Bedrock** — Foundation model inference (Amazon Nova Pro or Claude)

## What It Produces

| Document Type | Audience | Generated From |
|---------------|----------|---------------|
| Executive Summary | C-suite stakeholders | Portfolio data + MRA scores |
| Phase Status Report | Steering committee | Current progress + metrics |
| GO/NO-GO Decision Pack | Executive decision-makers | Phase criteria + risk assessment |
| MAP Milestone Report | AWS Partner Development Manager | Spend tracking + compliance |

Additionally, the repository includes complete migration runbooks covering all three MAP phases:

- **Phase 1: Assess** — Portfolio discovery, MRA, 6Rs classification, wave planning
- **Phase 2: Mobilize** — Landing zone, tooling, pilot migration, operating model
- **Phase 3: Migrate & Modernize** — Wave execution, cutover procedures, modernization roadmap

Plus supporting artefacts: training plan, ROI report, ARR model, AWS pricing guide, and customer onboarding checklist.

## Implementation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Escthelock/map-migration-runbook-agent.git
cd map-migration-runbook-agent/presentation-agent
pip install -r requirements.txt
```

### Step 2: Validate Customer Data

Before generating documents, validate the CSV quality:

```bash
python3 validate.py \
  --app-csv ../sample-data/health_app.csv \
  --infra-csv ../sample-data/health_infra.csv
```

The validator checks for missing criticality ratings, tech stacks without version numbers, duplicate IDs, orphaned servers, and EOL technologies. It outputs a quality score (0–100) with a clear READY / ACCEPTABLE / NOT READY verdict.

### Step 3: Preprocess Customer Data

The preprocessor converts raw CSVs into structured context that the AI agent can reason over:

```bash
python3 preprocess.py \
  --app-csv ../sample-data/health_app.csv \
  --infra-csv ../sample-data/health_infra.csv \
  --scope ../sample-data/scope.txt \
  --customer "AnyCompany" \
  --output context.md
```

It automatically extracts:
- Criticality distribution
- 6Rs classification (if present)
- Technology landscape and EOL risk signals
- Infrastructure resource totals
- Wave plan structure

### Step 3: Generate Documents

```bash
python3 presentation_agent.py \
  --type executive_summary \
  --context-file context.md \
  --customer "AnyCompany" \
  --output executive_summary.md
```

Available document types:

```bash
# Executive summary for C-suite
python3 presentation_agent.py --type executive_summary --context-file context.md --output summary.md

# GO/NO-GO decision pack
python3 presentation_agent.py --type go_nogo --phase assess --context-file context.md --output decision.md

# MAP milestone tracking
python3 presentation_agent.py --type map_milestone --context-file context.md --output milestone.md

# Phase status report
python3 presentation_agent.py --type phase_status --phase mobilize --context-file context.md --output status.md
```

### Step 4: Review and Deliver

The partner reviews the generated document, makes any customer-specific adjustments, and delivers. Regeneration takes seconds if data changes.

You can also specify model and region via CLI flags for different environments:

```bash
python3 presentation_agent.py \
  --type executive_summary \
  --context-file context.md \
  --model us.anthropic.claude-sonnet-4-20250514-v1:0 \
  --region us-east-1 \
  --output summary.md
```

## Worked Example: Healthcare Migration

Using a sample healthcare organisation (20 applications, 800TB storage, HIPAA compliance):

**Input:** Application portfolio CSV + infrastructure inventory CSV + scope document

**Output (Executive Summary excerpt):**

> AnyCompany is currently operating with a mix of legacy and modern applications, including five end-of-life applications that require immediate modernisation. The organisation faces challenges related to healthcare compliance, data sovereignty, and the need for scalable infrastructure to support growing clinical workloads.

> | Area | Finding | Impact | Recommendation |
> |------|---------|--------|----------------|
> | Application Portfolio | 20 apps: 7 Critical, 8 High, 5 Medium | EOL risk | Prioritise critical apps first |
> | Legacy Systems | 5 apps on Java 8, COBOL, ASP.NET 4.8 | Security vulnerabilities | Modernise to current standards |
> | Scalability | Fixed capacity for clinical workloads | Cannot handle peaks | Implement auto-scaling |
> | Cost | VMware licensing + hardware refresh due | $2.2M CapEx exposure | Migrate to pay-as-you-go |

**Output (GO/NO-GO excerpt):**

The agent correctly identified all mandatory criteria as met, flagged 3 recommended criteria below threshold (People & Process 2.8, Platform 2.5, Migration Experience 2.0), and recommended **CONDITIONAL GO** with specific remediation conditions and timelines.

## Repository Contents

```
map-migration-runbook-agent/
├── presentation-agent/          # AI agent code
│   ├── presentation_agent.py    # Main CLI agent
│   ├── preprocess.py            # CSV → structured context
│   ├── run_examples.py          # Sample invocations
│   └── prompt_library/          # Customisable prompts
├── runbooks/                    # Complete MAP-aligned runbooks
│   ├── Complete_Programme_Overview.md
│   ├── Phase1_Assess_Runbook.md
│   ├── Phase2_Mobilize_Runbook.md
│   ├── Phase3_Migrate_Modernize_Runbook.md
│   ├── Training_Plan.md
│   ├── Customer_Onboarding_Checklist.md
│   ├── ARR_Calculation.md
│   ├── ROI_Report_CSuite.md
│   └── AWS_Pricing_Calculator_Guide.md
├── sample-data/                 # Healthcare example data
└── LICENSE                      # MIT-0
```

Browse the full repository: [github.com/Escthelock/map-migration-runbook-agent](https://github.com/Escthelock/map-migration-runbook-agent)

## Extending the Approach

The prompt library is fully customisable. Partners can:

- **Add document types** — Wave runbooks, risk registers, training plans, cost comparisons
- **Customise branding** — Adjust tone, terminology, section structure per partner methodology
- **Chain agents** — Feed discovery agent output into strategy agent into presentation agent
- **Add live data** — Pull AWS Cost Explorer data for real-time MAP milestone tracking
- **Multi-context input** — Combine multiple data sources for cross-phase reporting

## MAP Alignment

The solution maps directly to MAP phases:

| MAP Phase | Agent Outputs |
|-----------|--------------|
| Assess | Portfolio assessment, MRA report, business case, 6Rs classification |
| Mobilize | Landing zone design, pilot report, wave plans, GO/NO-GO pack |
| Migrate & Modernize | Wave status reports, cutover runbooks, MAP milestone tracking |

## Results

For the AnyCompany healthcare engagement (20 applications, 14-month programme):

| Metric | Manual Approach | AI-Assisted | Improvement |
|--------|----------------|-------------|-------------|
| Executive summary creation | 2–3 days | 30 seconds | 99% faster |
| GO/NO-GO pack | 1–2 days | 30 seconds | 99% faster |
| Phase status report | 4–6 hours | 30 seconds | 99% faster |
| Full runbook set (3 phases) | 3–4 weeks | 2–3 hours (review) | 90% faster |
| Iteration on changes | 1–2 days | 30 seconds | 99% faster |

## Prerequisites

- AWS account with Amazon Bedrock access (Amazon Nova Pro or Claude Sonnet)
- Python 3.11+
- `strands-agents` package
- Customer data in CSV format (application portfolio + infrastructure inventory)

## Get Started

```bash
git clone https://github.com/Escthelock/map-migration-runbook-agent.git
cd map-migration-runbook-agent/presentation-agent
pip install -r requirements.txt
python3 run_examples.py --example all
```

## Conclusion

By combining structured data collection with AI-powered document generation, partners can dramatically reduce the documentation overhead of MAP engagements while maintaining quality and consistency. The approach frees consultants to focus on what matters — architecture decisions, stakeholder alignment, and hands-on migration execution — rather than formatting documents.

The complete solution is open source and ready to use: [github.com/Escthelock/map-migration-runbook-agent](https://github.com/Escthelock/map-migration-runbook-agent)

---

*Built with [Strands Agents SDK](https://github.com/strands-agents/sdk-python) and Amazon Bedrock.*
