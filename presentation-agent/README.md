# Presentation Generator Agent

AI agent that generates customer-ready presentation documents from migration runbook content and customer data.

## Output Types

| Type | Use Case | Audience |
|------|----------|----------|
| `executive_summary` | Programme overview for C-suite | Executive sponsors, board |
| `phase_status` | Weekly/bi-weekly progress report | Steering committee |
| `go_nogo` | Phase gate decision pack | Executive decision-makers |
| `map_milestone` | MAP $50K spend tracking | AWS PDM, partner development |

## Setup

```bash
pip install -r requirements.txt
export AWS_REGION=us-east-1
# Ensure AWS credentials are configured (aws configure or env vars)
```

## Usage

### CLI — Single Document

```bash
# Executive summary from a context file
python3 presentation_agent.py --type executive_summary --context-file my_data.md --customer "AnyCompany" --output summary.md

# Phase status report
python3 presentation_agent.py --type phase_status --phase assess --context-file my_data.md --output status.md

# GO/NO-GO decision pack
python3 presentation_agent.py --type go_nogo --phase mobilize --context-file my_data.md --output decision.md

# MAP milestone tracking
python3 presentation_agent.py --type map_milestone --context-file my_data.md --output milestone.md
```

### Run All Examples (AnyCompany Sample Data)

```bash
python3 run_examples.py --example all        # All 4 document types
python3 run_examples.py --example executive   # Executive summary only
python3 run_examples.py --example gonogo      # GO/NO-GO pack only
```

## Context File

The `--context-file` should contain any relevant migration data:
- Runbook content (from Phase 1/2/3 runbooks)
- Application portfolio data
- MRA scores
- Wave plan details
- Cost projections
- Current status and progress

The agent extracts relevant information and formats it into the requested document type.

## Customisation

Edit prompts in `prompt_library/presentation_prompts.py` to:
- Adjust output structure
- Add partner branding guidelines
- Change terminology or language
- Add/remove sections

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_ID` | `us.anthropic.claude-sonnet-4-20250514-v1:0` | Bedrock model ID |
| `AWS_REGION` | `us-east-1` | AWS region for Bedrock |
| `MAX_TOKENS` | `8192` | Maximum output tokens |
