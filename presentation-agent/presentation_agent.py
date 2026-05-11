"""Presentation Generator Agent — produces customer-ready documents from runbook + customer data.

Usage:
    python3 presentation_agent.py --type executive_summary --context-file context.md --output output.md
    python3 presentation_agent.py --type phase_status --phase assess --context-file context.md
    python3 presentation_agent.py --type go_nogo --phase mobilize --context-file context.md
    python3 presentation_agent.py --type map_milestone --context-file context.md
    python3 presentation_agent.py --type executive_summary --context-file context.md --model us.anthropic.claude-sonnet-4-20250514-v1:0 --region us-east-1
"""

import argparse
import os
import sys

from strands import Agent
from strands.models.bedrock import BedrockModel

sys.path.insert(0, os.path.dirname(__file__))
from prompt_library.presentation_prompts import (
    get_executive_summary_prompt,
    get_go_nogo_prompt,
    get_map_milestone_prompt,
    get_phase_status_prompt,
)

DEFAULT_MODEL_ID = os.environ.get("MODEL_ID", "us.amazon.nova-pro-v1:0")
DEFAULT_REGION = os.environ.get("AWS_REGION", "us-west-2")
DEFAULT_MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "5000"))


PROMPT_MAP = {
    "executive_summary": get_executive_summary_prompt,
    "phase_status": get_phase_status_prompt,
    "go_nogo": get_go_nogo_prompt,
    "map_milestone": get_map_milestone_prompt,
}


def load_context(context_file: str) -> str:
    """Load context from a file (runbook content, customer data, etc.)."""
    if not os.path.exists(context_file):
        print(f"Error: Context file not found: {context_file}", file=sys.stderr)
        sys.exit(1)
    with open(context_file, "r") as f:
        return f.read()


def build_user_message(doc_type: str, context: str, phase: str | None = None, customer: str | None = None) -> str:
    """Build the user message that provides context to the agent."""
    parts = []
    if customer:
        parts.append(f"Customer: {customer}")
    if phase:
        parts.append(f"Phase: {phase}")
    parts.append(f"Document type requested: {doc_type}")
    parts.append(f"\n--- CONTEXT DATA ---\n{context}\n--- END CONTEXT ---")
    parts.append("\nGenerate the document using the context above. Use only data present in the context.")
    return "\n".join(parts)


def run_agent(doc_type: str, context: str, phase: str | None = None, customer: str | None = None,
              model_id: str = DEFAULT_MODEL_ID, region: str = DEFAULT_REGION, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
    """Run the presentation agent and return the generated document."""
    prompt_fn = PROMPT_MAP.get(doc_type)
    if not prompt_fn:
        raise ValueError(f"Unknown document type: {doc_type}. Choose from: {list(PROMPT_MAP.keys())}")

    system_prompt = prompt_fn()

    try:
        model = BedrockModel(model_id=model_id, region_name=region, max_tokens=max_tokens)
        agent = Agent(system_prompt=system_prompt, model=model)
        user_message = build_user_message(doc_type, context, phase, customer)
        result = agent(user_message)
        return str(result)
    except Exception as e:
        error_msg = str(e)
        if "AccessDeniedException" in error_msg:
            print(f"Error: Access denied to model '{model_id}' in region '{region}'.", file=sys.stderr)
            print("Ensure your IAM role has bedrock:InvokeModel permission and the model is enabled.", file=sys.stderr)
        elif "ValidationException" in error_msg:
            print(f"Error: Model '{model_id}' not available. Try with inference profile prefix 'us.' (e.g., us.amazon.nova-pro-v1:0).", file=sys.stderr)
        elif "ThrottlingException" in error_msg:
            print("Error: Bedrock rate limit exceeded. Wait and retry.", file=sys.stderr)
        else:
            print(f"Error: {error_msg}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Presentation Generator Agent — customer-ready documents from migration data")
    parser.add_argument("--type", required=True, choices=list(PROMPT_MAP.keys()), help="Document type to generate")
    parser.add_argument("--context-file", required=True, help="Path to context file (runbook, CSV, assessment data)")
    parser.add_argument("--phase", choices=["assess", "mobilize", "migrate"], help="Migration phase (for status/go-nogo)")
    parser.add_argument("--customer", default=None, help="Customer name")
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    parser.add_argument("--model", default=DEFAULT_MODEL_ID, help=f"Bedrock model ID (default: {DEFAULT_MODEL_ID})")
    parser.add_argument("--region", default=DEFAULT_REGION, help=f"AWS region (default: {DEFAULT_REGION})")
    parser.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS, help=f"Max output tokens (default: {DEFAULT_MAX_TOKENS})")

    args = parser.parse_args()

    context = load_context(args.context_file)
    result = run_agent(args.type, context, args.phase, args.customer, args.model, args.region, args.max_tokens)

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True) if os.path.dirname(args.output) else None
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Document written to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
