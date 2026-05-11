# MAP Migration Runbook & Presentation Agent

AI-powered migration runbook generator and presentation agent for AWS Migration Acceleration Program (MAP) engagements.

## Overview

This solution provides:

1. **Migration Runbooks** — Complete phase-by-phase delivery guides (Assess, Mobilize, Migrate & Modernize) aligned to AWS MAP
2. **Presentation Generator Agent** — AI agent that produces customer-ready documents from raw CSV data
3. **Supporting Artefacts** — Training plan, ROI report, ARR model, pricing guide, onboarding checklist

## Architecture

```
Customer CSVs → preprocess.py → context.md → presentation_agent.py → Customer-ready documents
                                                    │
                                              Amazon Bedrock
                                           (Claude / Nova Pro)
```

## Repository Structure

```
├── presentation-agent/          # AI agent code
│   ├── presentation_agent.py    # Main CLI agent
│   ├── preprocess.py            # CSV → structured context converter
│   ├── run_examples.py          # Sample invocations
│   ├── requirements.txt
│   └── prompt_library/          # Customisable system prompts
├── runbooks/                    # Migration delivery guides
│   ├── Complete_Programme_Overview.md
│   ├── Phase1_Assess_Runbook.md
│   ├── Phase2_Mobilize_Runbook.md
│   ├── Phase3_Migrate_Modernize_Runbook.md
│   ├── Training_Plan.md
│   ├── Customer_Onboarding_Checklist.md
│   ├── ARR_Calculation.md
│   ├── ROI_Report_CSuite.md
│   └── AWS_Pricing_Calculator_Guide.md
├── sample-data/                 # Example customer data (healthcare)
│   ├── health_app.csv
│   ├── health_infra.csv
│   └── scope.txt
└── LICENSE
```

## Prerequisites

- Python 3.11+
- AWS account with Amazon Bedrock access
- Model enabled: Claude Sonnet 4 or Amazon Nova Pro
- AWS credentials configured

## Quick Start

```bash
# Install
cd presentation-agent
pip install -r requirements.txt

# Preprocess customer CSVs
python3.11 preprocess.py \
  --app-csv ../sample-data/health_app.csv \
  --infra-csv ../sample-data/health_infra.csv \
  --scope ../sample-data/scope.txt \
  --customer "AnyCompany" \
  --output context.md

# Generate documents
python3.11 presentation_agent.py --type executive_summary --context-file context.md --output summary.md
python3.11 presentation_agent.py --type go_nogo --phase assess --context-file context.md --output decision.md
python3.11 presentation_agent.py --type map_milestone --context-file context.md --output milestone.md
python3.11 presentation_agent.py --type phase_status --phase assess --context-file context.md --output status.md
```

## Document Types

| Type | Command | Audience |
|------|---------|----------|
| Executive Summary | `--type executive_summary` | C-suite |
| Phase Status | `--type phase_status --phase <phase>` | Steering committee |
| GO/NO-GO Pack | `--type go_nogo --phase <phase>` | Decision-makers |
| MAP Milestone | `--type map_milestone` | AWS PDM |

## Customisation

Edit prompts in `presentation-agent/prompt_library/presentation_prompts.py` to match your partner methodology, branding, or terminology.

## Security

- No customer data is stored or transmitted beyond the Bedrock API call
- All processing is local — CSVs never leave the execution environment
- Use IAM least-privilege for Bedrock access
- Do not commit customer data to version control

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
