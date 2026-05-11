# How I Built an AI Agent That Generates AWS MAP Migration Deliverables in 30 Seconds

**Tags:** migration, MAP, generative-ai, strands-agents, modernization, bedrock, partner

---

Every AWS Migration Acceleration Program (MAP) engagement produces the same set of documents: portfolio assessments, wave plans, executive summaries, GO/NO-GO decision packs, cutover runbooks, and MAP milestone reports. For a 20-application healthcare migration I was working on, the documentation alone was tracking toward 3–4 weeks of consultant effort across three phases.

I built an AI agent that generates these documents from raw CSV data in under 30 seconds. Here's how it works, what I learned, and how you can use it.

## The Problem: Documentation Bottleneck

MAP engagements follow a predictable structure — Assess, Mobilize, Migrate & Modernize. Each phase requires specific deliverables with consistent formatting, data-driven content, and MAP methodology alignment. The work is:

- **Repetitive** — same document types for every customer
- **Data-dependent** — content comes from portfolio inventories and infrastructure data
- **Iterative** — scope changes mean regenerating documents multiple times
- **Time-consuming** — 2–3 days per executive summary, 1–2 weeks per phase runbook

The insight: if the structure is consistent and the content is derived from data, an AI agent can do the heavy lifting.

## The Solution: A Two-Stage Pipeline

I built a pipeline with two components:

```
Customer CSVs → Preprocessor → Structured Context → AI Agent → Customer-Ready Document
```

**Stage 1: Preprocessor** — A Python script that parses application portfolio and infrastructure CSVs, extracts key metrics (criticality distribution, 6Rs classification, technology landscape, EOL risks, resource totals), and outputs a structured markdown context file.

**Stage 2: Presentation Agent** — A Strands Agents SDK agent with document-type-specific system prompts that takes the context and generates a formatted deliverable. Each document type has its own prompt defining the exact section structure, tone, and audience.

The agent runs on Amazon Bedrock (Amazon Nova Pro or Claude), keeping all data within AWS infrastructure.

## What It Generates

I built four document types that cover the most common partner-to-customer deliverables:

| Document | Audience | What It Contains |
|----------|----------|-----------------|
| Executive Summary | C-suite | Situation, findings table, programme overview, recommendation, next steps |
| Phase Status Report | Steering committee | RAG status, progress table, risks, metrics, next period plan |
| GO/NO-GO Decision Pack | Decision-makers | Criteria assessment (mandatory + recommended), risk matrix, recommendation with conditions |
| MAP Milestone Report | AWS PDM | Cumulative spend tracking, $50K prediction, compliance checklist |

Each generates in 20–40 seconds and produces structured markdown with tables, bullet points, and clear section headings — ready to paste into a slide deck or deliver as-is.

## Building the Agent

### The Prompt Library

The key to consistent, high-quality output is the system prompt. Each document type has a dedicated prompt that enforces:

- Exact section headings (the agent must use them verbatim)
- Output format rules (tables for metrics, bullets for recommendations)
- Data-only content ("Use only data present in the context — never fabricate")
- Audience-appropriate tone

For example, the GO/NO-GO prompt specifies:

```
Be objective — present facts, not opinions
Clearly separate mandatory criteria (must-have) from recommended (should-have)
Use checkmarks for met criteria, crosses for unmet
Provide a clear recommendation with rationale
```

This means the agent produces a consistent structure every time, regardless of the customer data fed in.

### The Preprocessor

Raw CSVs vary wildly between customers — different column names, formats, delimiters. The preprocessor handles this with fuzzy column matching:

```python
def find_col(row, candidates):
    for c in candidates:
        for key in row.keys():
            if c.lower() in key.lower():
                return key
    return None
```

It looks for "Criticality" or "SLA_Tier" or "Priority" — whatever the customer used. It also auto-detects EOL technologies by scanning tech stack fields for patterns like "java 8", "cobol", ".net 4.6", flagging them as risk signals.

### Data Validation

Before generating documents, I added a validation step that catches data quality issues:

```bash
python3 validate.py --app-csv portfolio.csv --infra-csv servers.csv
```

Output:
```
QUALITY SCORE: 95/100  ✅ READY — proceed with document generation

🟡 MEDIUM
   [Technology Stack] Tech stack missing version numbers
     Affected: 29 apps

ℹ️ INFO
   [EOL Detection] End-of-life technologies detected: vb6
     Affected: 1 apps
```

This prevents garbage-in/garbage-out — the biggest risk with AI-generated documents. If criticality ratings are missing, the wave plan will be wrong. If tech stacks lack version numbers, EOL detection fails. The validator catches these before they become problems in customer-facing documents.

### Error Handling

Production use means handling real-world failures gracefully:

```python
try:
    result = agent(user_message)
except Exception as e:
    if "AccessDeniedException" in str(e):
        print("Error: Access denied. Ensure bedrock:InvokeModel permission is granted.")
    elif "ThrottlingException" in str(e):
        print("Error: Rate limit exceeded. Wait and retry.")
```

The agent also accepts `--model` and `--region` CLI flags so partners in different regions don't need to edit source code.

## Worked Example: Healthcare Migration

I tested this with a realistic healthcare scenario: 20 applications (7 Critical/Tier-1, including an EHR system with 12+ dependencies), 20 VMware servers, 800TB+ storage, HIPAA compliance requirements, and 5 legacy/EOL applications including a COBOL claims processing system.

**Input:** Three files — `health_app.csv`, `health_infra.csv`, `scope.txt`

**Command:**
```bash
python3 preprocess.py --app-csv health_app.csv --infra-csv health_infra.csv --scope scope.txt --customer "AnyCompany" --output context.md
python3 presentation_agent.py --type go_nogo --phase assess --context-file context.md --output decision.md
```

**Output (GO/NO-GO excerpt):**

The agent correctly identified all 8 mandatory criteria as met (portfolio complete, MRA submitted, business case approved, MAP funding confirmed), flagged 3 recommended criteria below threshold (People & Process 2.8/5.0, Platform & Architecture 2.5/5.0, Migration Experience 2.0/5.0), and recommended **CONDITIONAL GO** with four specific remediation conditions:

1. Training programme launched within 2 weeks
2. AWS Solutions Architect engaged for landing zone review
3. Pilot migration must succeed before Wave 1 production cutover
4. CCoE established with defined RACI within 3 weeks

This is exactly what a senior consultant would produce — but it took 30 seconds instead of a day.

## Security Considerations

Customer metadata (application names, tech stacks, criticality ratings, server specs) is sent to Amazon Bedrock for inference. Key security properties:

- **No training on customer data** — Bedrock does not use inputs/outputs to train models
- **No persistence** — data is not stored after inference
- **No third-party sharing** — data stays within AWS, not sent to model providers
- **Encryption in transit** — TLS 1.2+
- **Region control** — data stays in the region you specify (`--region` flag)
- **HIPAA eligible** — Bedrock is covered under AWS BAA

The agent sends metadata only — not patient data, credentials, or PII. The preprocessor controls exactly what enters the context file, and partners should review it before running the agent.

For additional hardening: use a VPC endpoint for Bedrock (traffic never hits the public internet), scope IAM to `bedrock:InvokeModel` on the specific model ARN, and disable invocation logging if prompt content is sensitive.

## Beyond Document Generation

I also built complete MAP-aligned runbooks covering all three phases:

- **Phase 1: Assess** — Portfolio discovery methodology, MRA scoring, 6Rs classification, wave planning, GO/NO-GO criteria
- **Phase 2: Mobilize** — Landing zone design (8-account structure), security baseline, migration tooling, pilot execution, training plan
- **Phase 3: Migrate & Modernize** — Wave-by-wave execution plans, cutover templates with rollback procedures, EHR-specific detailed cutover (minute-by-minute), COBOL modernisation approach, post-migration optimisation, decommissioning

Plus supporting artefacts: a 37-certification training plan spanning all phases, ROI report (285% over 5 years), ARR calculation for partner revenue modelling, AWS Pricing Calculator configuration guide, and a customer onboarding checklist with recommended discovery tools by maturity level.

## Results

| Metric | Manual | AI-Assisted | Improvement |
|--------|--------|-------------|-------------|
| Executive summary | 2–3 days | 30 seconds | 99% |
| GO/NO-GO pack | 1–2 days | 30 seconds | 99% |
| Phase status report | 4–6 hours | 30 seconds | 99% |
| Full runbook set (3 phases) | 3–4 weeks | 2–3 hours (review) | 90% |
| Iteration on scope change | 1–2 days | 30 seconds | 99% |

The 2–3 hours for the full runbook set is review time — the generation itself takes minutes. The real value is iteration speed: when a customer adds 5 applications to scope mid-engagement, regenerating all documents takes seconds instead of days.

## How to Use It

The complete solution is open source:

**Repository:** [github.com/Escthelock/map-migration-runbook-agent](https://github.com/Escthelock/map-migration-runbook-agent)

```bash
git clone https://github.com/Escthelock/map-migration-runbook-agent.git
cd map-migration-runbook-agent/presentation-agent
pip install -r requirements.txt

# Validate data quality
python3 validate.py --app-csv ../sample-data/health_app.csv --infra-csv ../sample-data/health_infra.csv

# Generate context from CSVs
python3 preprocess.py --app-csv ../sample-data/health_app.csv --infra-csv ../sample-data/health_infra.csv --scope ../sample-data/scope.txt --customer "AnyCompany" --output context.md

# Generate documents
python3 presentation_agent.py --type executive_summary --context-file context.md --output summary.md
```

**Prerequisites:** Python 3.11+, AWS account with Bedrock access (Nova Pro or Claude), `strands-agents` package.

The prompt library is fully customisable — edit `prompt_library/presentation_prompts.py` to match your partner methodology, add new document types, or adjust the output structure. CSV templates are included for customer onboarding.

## What I'd Build Next

The natural extensions are:

1. **Live AWS integration** — Pull Cost Explorer spend and Migration Hub status as agent tools for real-time status reports
2. **Multi-agent pipeline** — Chain Discovery → 6Rs → Wave Planning → Presentation agents so CSVs produce the full deliverable set in one command
3. **Web UI** — FastAPI + React frontend for partners who prefer clicking over CLI
4. **RAG over runbooks** — Index all documentation into Bedrock Knowledge Bases for conversational Q&A ("What's the rollback plan for the EHR cutover?")

## Conclusion

The documentation overhead of MAP engagements is a solved problem. With structured prompts, a data preprocessor, and Amazon Bedrock, partners can generate customer-ready deliverables in seconds — freeing consultants to focus on architecture decisions, stakeholder alignment, and hands-on migration execution.

The code is ready to use: [github.com/Escthelock/map-migration-runbook-agent](https://github.com/Escthelock/map-migration-runbook-agent)

---

*Built with [Strands Agents SDK](https://github.com/strands-agents/sdk-python) and Amazon Bedrock.*
