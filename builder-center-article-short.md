# AI-Powered MAP Migration Deliverables in 30 Seconds

Every AWS MAP engagement produces the same documents — executive summaries, GO/NO-GO packs, wave plans, milestone reports. For a 20-app healthcare migration, this was tracking toward 3–4 weeks of documentation effort.

I built an AI agent that generates these from raw CSV data in under 30 seconds.

## How It Works

```
Customer CSVs → Preprocessor → AI Agent (Bedrock) → Customer-Ready Document
```

1. **Validate** — checks CSV quality (missing fields, no version numbers, duplicates)
2. **Preprocess** — parses CSVs into structured context (criticality, 6Rs, EOL risks)
3. **Generate** — Strands Agents SDK + Amazon Bedrock produces formatted deliverables

Four document types: Executive Summary, Phase Status Report, GO/NO-GO Decision Pack, MAP Milestone Report. Each has a dedicated prompt enforcing consistent structure.

## Results

| Document | Manual | AI-Assisted |
|----------|--------|-------------|
| Executive summary | 2–3 days | 30 seconds |
| GO/NO-GO pack | 1–2 days | 30 seconds |
| Full runbook set | 3–4 weeks | 2–3 hours (review) |

The real value is iteration — when scope changes, regeneration takes seconds instead of days.

## Security

Customer metadata goes to Amazon Bedrock (not patient data or PII). Bedrock doesn't store inputs, doesn't train on them, and data stays in your chosen region. HIPAA eligible.

## Try It

```bash
git clone https://github.com/Escthelock/map-migration-runbook-agent.git
cd map-migration-runbook-agent/presentation-agent
pip install -r requirements.txt
python3 validate.py --app-csv ../sample-data/health_app.csv
python3 presentation_agent.py --type executive_summary --context-file context.md --output summary.md
```

Includes complete MAP-aligned runbooks (Assess, Mobilize, Migrate), training plan, ROI report, and customer onboarding checklist.

**Repo:** [github.com/Escthelock/map-migration-runbook-agent](https://github.com/Escthelock/map-migration-runbook-agent)

---

*Built with Strands Agents SDK and Amazon Bedrock.*
