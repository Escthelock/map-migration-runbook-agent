# Security FAQ — MAP Migration Presentation Agent

---

## Q: What data is sent to the AI model?

Application and infrastructure **metadata** from the preprocessed context file is sent to Amazon Bedrock for document generation. This includes:

- Application names, technology stacks, criticality ratings
- Server names, OS versions, CPU/RAM/storage specifications
- Business unit and team names
- Compliance framework labels (e.g., "HIPAA", "PCI-DSS")
- Migration drivers and scope text

**Not sent:** Raw CSV files, credentials, secrets, patient data, PII, or anything outside the context file you explicitly provide.

---

## Q: Is customer data used to train AI models?

**No.** Amazon Bedrock does not use customer inputs or outputs to train, improve, or fine-tune foundation models. This is contractually guaranteed by AWS.

---

## Q: Is data shared with third-party model providers (Anthropic, Meta, etc.)?

**No.** When using Amazon Bedrock, customer data remains within AWS infrastructure. It is not sent to model providers and is not accessible to them.

---

## Q: Is data stored or persisted after generation?

**No.** Amazon Bedrock does not store prompts or responses after inference completes. Data exists only for the duration of the API call.

---

## Q: Is data encrypted?

**Yes.**
- **In transit:** TLS 1.2+ between the agent and Amazon Bedrock
- **At rest:** Not applicable — Bedrock does not persist inference data
- **Context files on disk:** Customer responsibility — encrypt at rest using OS-level or S3 encryption

---

## Q: Where does the data reside?

Data remains in the AWS region where Bedrock is invoked. You control this via the `--region` CLI flag or `AWS_REGION` environment variable (default: `us-west-2`). Data does not leave that region during processing.

---

## Q: Is Amazon Bedrock HIPAA-eligible?

**Yes.** Amazon Bedrock is a HIPAA-eligible service. Customers can include it in their BAA (Business Associate Agreement) with AWS. However:

- Ensure only metadata (not PHI) is included in prompts
- If PHI must be processed, confirm BAA coverage and implement additional controls
- Use VPC endpoints to keep traffic off the public internet

---

## Q: What compliance certifications does Bedrock hold?

| Certification | Status |
|---------------|--------|
| HIPAA | Eligible (requires BAA) |
| SOC 1, 2, 3 | ✅ |
| ISO 27001 | ✅ |
| ISO 27017 | ✅ |
| ISO 27018 | ✅ |
| PCI DSS | ✅ |
| FedRAMP | Moderate (select regions) |

---

## Q: Can prompts or responses be logged?

By default, Bedrock invocation logging is **disabled**. If enabled via CloudTrail or Bedrock model invocation logging:

- Prompts and responses are written to S3 or CloudWatch
- Encrypt logs with a customer-managed KMS key
- Restrict access to logs via IAM policies
- Disable invocation logging if prompt content is sensitive

---

## Q: How do we prevent sensitive data from being sent?

The preprocessor (`preprocess.py`) controls what enters the context file. Recommended controls:

1. **Review the context file** before running the agent — it's a readable markdown file
2. **Strip unnecessary columns** — remove fields containing names, emails, IP addresses if not needed for document generation
3. **Add a data classification step** — flag potential PII/PHI before processing
4. **Use allowlists** — only include columns explicitly needed (app name, tech stack, criticality, environment)

---

## Q: Can someone intercept the data in transit?

**No** (under normal conditions). The agent communicates with Bedrock via the AWS SDK over TLS 1.2+. To further harden:

- **Use a VPC endpoint** for Bedrock (`com.amazonaws.<region>.bedrock-runtime`) — traffic stays on the AWS private network
- **Enable AWS PrivateLink** — eliminates public internet traversal entirely
- **Restrict security groups** — limit outbound to Bedrock endpoint only

---

## Q: What IAM permissions are required?

Minimum required:

```json
{
  "Effect": "Allow",
  "Action": "bedrock:InvokeModel",
  "Resource": "arn:aws:bedrock:<region>::foundation-model/us.amazon.nova-pro-v1:0"
}
```

**Do not** grant `bedrock:*`. Scope to the specific model and region used.

---

## Q: What about prompt injection attacks?

The risk is low but present. Customer CSV data is treated as context, not instructions. Mitigations:

- The system prompt is fixed (defined in `prompt_library/`)
- Customer data is wrapped in clearly delimited context blocks
- The agent is instructed to use only data present in the context
- Validate CSV content before processing (no executable code, no instruction-like text)

---

## Q: Is the agent code itself secure?

| Aspect | Status |
|--------|--------|
| No hardcoded credentials | ✅ Uses AWS SDK credential chain |
| No outbound calls except Bedrock | ✅ No third-party APIs |
| No data persistence | ✅ Output written to local file only |
| No network listeners | ✅ CLI tool, not a server |
| Open source / auditable | ✅ Full source in repository |

---

## Q: What should we tell the customer?

Suggested disclosure statement:

> "Application metadata (names, technology stacks, criticality ratings, infrastructure specifications) is sent to Amazon Bedrock for document generation. Bedrock does not store, log, or use this data for model training. Data remains within your AWS account's region and is encrypted in transit via TLS 1.2+. No PHI, PII, or credentials are included in prompts — only infrastructure and application metadata. Amazon Bedrock is HIPAA-eligible and holds SOC 1/2/3, ISO 27001, and PCI DSS certifications."

---

## Q: Summary — what are the real risks?

| Risk | Severity | Mitigation |
|------|----------|------------|
| Sensitive data in CSV (PII/PHI) accidentally included | Medium | Review context file before running; strip unnecessary columns |
| Over-permissive IAM | Medium | Scope to `bedrock:InvokeModel` on specific model ARN only |
| Invocation logging captures prompts | Low | Disable logging or encrypt with CMK |
| Shared AWS account exposure | Low | Use dedicated account for migration tooling |
| Prompt injection from malicious CSV content | Low | Validate CSV input; system prompt is fixed |
| Data exfiltration via model output | Very Low | Model cannot make outbound calls; output is local file only |

---

*For the latest Amazon Bedrock security documentation, see: https://docs.aws.amazon.com/bedrock/latest/userguide/security.html*
