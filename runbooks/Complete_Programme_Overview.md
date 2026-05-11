# AWS MAP Migration — Complete Programme Overview

## AnyCompany Healthcare | Cloud Transformation

---

## Programme at a Glance

| Item | Detail |
|------|--------|
| Customer | AnyCompany (Healthcare) |
| Partner | AnyTech Cloud Solutions |
| Programme | AWS Migration Acceleration Program (MAP) |
| Applications | 20 (7 Critical, 8 High, 5 Medium) |
| Infrastructure | 20 servers, 800TB+ storage (VMware) |
| Duration | 14 months (migration) + ongoing managed services |
| Investment | $4.0M (migration) |
| 5-Year ROI | 285% ($4.9M net benefit) |
| Payback | 18 months |
| Annual Savings | $1.4M–$1.8M (Year 2+) |
| ARR (Partner) | $835,500/year |

---

## Migration Drivers

- 5 legacy/EOL applications (Java 8, COBOL, ASP.NET 4.8) — security and maintenance risk
- HIPAA compliance — manual controls insufficient for audit requirements
- Scalability — fixed capacity cannot handle clinical workload peaks
- Cost optimisation — VMware licensing + hardware refresh due ($2.2M)
- Innovation — no ML/AI capability for clinical decision support

---

## Programme Phases

```
Phase 1: ASSESS (Weeks 1–8)
    │
    ├── Portfolio discovery (20 apps, 20 servers)
    ├── MRA scored 3.1/5.0 (Moderate Readiness)
    ├── Business case approved
    ├── 6Rs classification complete
    ├── Wave plan agreed
    └── MAP funding approved
    │
    ▼ GO/NO-GO → CONDITIONAL GO
    │
Phase 2: MOBILIZE (Weeks 9–20)
    │
    ├── Landing zone deployed (8 AWS accounts)
    ├── Security baseline (HIPAA, BAA executed)
    ├── Direct Connect + VPN connectivity
    ├── Migration tools configured (MGN, DMS, DataSync)
    ├── 37 certifications programme launched
    ├── 2–3 pilot apps migrated successfully
    └── Detailed wave plans with cutover runbooks
    │
    ▼ GO/NO-GO → GO
    │
Phase 3: MIGRATE & MODERNIZE (Weeks 21–64)
    │
    ├── Wave 1 (Weeks 7–14):  4 low-risk apps
    ├── Wave 2 (Weeks 15–26): 6 Tier-2 clinical apps
    ├── Wave 3 (Weeks 27–40): 5 core platform apps
    ├── Wave 4 (Weeks 41–56): 5 mission-critical apps
    ├── Post-migration optimisation (Weeks 56–60)
    ├── Decommissioning (Weeks 60–64)
    └── Modernization roadmap initiated
    │
    ▼ PROGRAMME CLOSURE → STEADY STATE
```

---

## 6Rs Strategy

| R-Type | Apps | % | Key Applications |
|--------|------|---|-----------------|
| Replatform | 11 | 55% | EHR, Patient Portal, HIE, Revenue Cycle, Clinical Decision Support |
| Refactor | 5 | 25% | Claims Processing (COBOL), Clinical Data Warehouse, EHR Analytics, LIS, Supply Chain |
| Rehost | 2 | 10% | Pharmacy Mgmt (McKesson), Medical Imaging (Agfa) |
| Retire | 1 | 5% | Patient Discharge System |
| Retain | 1 | 5% | (SaaS — already cloud-based) |

---

## Wave Plan Summary

| Wave | Weeks | Apps | Strategy | Key Risk |
|------|-------|------|----------|----------|
| 0 | 1–6 | — | Foundation (landing zone, tooling, training) | Direct Connect lead time |
| 1 | 7–14 | 4 | Low-risk: build team confidence | Java 8 modernisation |
| 2 | 15–26 | 6 | Tier-2 clinical: vendor coordination | 500TB DICOM imaging transfer |
| 3 | 27–40 | 5 | Core platform: MSK, hybrid EHR | Cross-network latency |
| 4 | 41–56 | 5 | Mission-critical: EHR, COBOL | Highest risk — 12+ dependencies |

---

## Financial Summary

### Investment vs. Return

| Metric | Value |
|--------|-------|
| Total Investment | $4,002,000 |
| 5-Year Savings | $9,153,000 |
| 5-Year Net Benefit | $4,931,000 |
| ROI | 285% |
| Payback Period | 18 months |
| Cost Reduction (Year 2+) | 38% vs. current state |

### AWS Steady-State Costs

| Category | Monthly | Annual |
|----------|---------|--------|
| Compute (ECS + EC2) | $6,600 | $79,200 |
| Databases (Aurora + RDS + DocumentDB) | $12,700 | $152,400 |
| Storage (S3 + EFS — 500TB) | $5,700 | $68,400 |
| Analytics (EMR + Redshift) | $4,300 | $51,600 |
| Streaming, Caching, Networking, Security | $8,100 | $97,200 |
| **Total** | **$37,400** | **$448,800** |

### MAP Milestone

- $50K cumulative spend achieved: **Migrate Month 1**
- Confidence: **High**

---

## Training & Certification Programme

| Phase | Focus | Certifications |
|-------|-------|---------------|
| Assess | Cloud literacy (all 42 staff) | 15 Cloud Practitioner |
| Mobilize | Hands-on skills (architects, DevOps, DBAs) | 12 Associate/Specialty |
| Migrate | Operational mastery + independence | 10 Professional/Specialty |
| **Total** | | **37 certifications** |

### Partner-to-Customer Handover

| Wave | Partner Effort | Customer Effort |
|------|---------------|-----------------|
| Wave 1 | 80% (leads) | 20% (shadows) |
| Wave 2 | 50% | 50% |
| Wave 3 | 20% | 80% (leads) |
| Wave 4 | 10% (complex only) | 90% |

---

## Compliance & Security

| Requirement | AWS Solution |
|-------------|-------------|
| HIPAA | BAA executed, dedicated HIPAA account, encryption (KMS), Macie for PHI |
| HL7 FHIR R4 | API Gateway + ECS microservices, MSK for event streaming |
| DICOM 3.0 | S3 for imaging storage, DocumentDB for metadata |
| EDI X12 | Amazon MQ + Step Functions for claims processing |
| Audit | CloudTrail (org-wide), Config conformance packs, Security Hub |

---

## Key Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| EHR cutover failure | Critical | Full dress rehearsal, 4-hour rollback window, 3-week hypercare |
| COBOL modernisation delays | High | Start Week 41, hybrid approach (transpile + manual rewrite) |
| 800TB data transfer overrun | Medium | Start in Mobilize, run DataSync continuously in background |
| Vendor non-cooperation | High | Written confirmation before cutover from McKesson, Agfa, Sectra, Cerner |
| Team skills gap | High | 37 certifications, progressive handover model |

---

## Deliverables Produced

| Document | Purpose |
|----------|---------|
| Phase 1: Assess Runbook | Portfolio discovery, MRA, 6Rs, wave plan methodology |
| Phase 2: Mobilize Runbook | Landing zone, tooling, pilot migration, operating model |
| Phase 3: Migrate & Modernize Runbook | Wave execution, cutover procedures, modernization roadmap |
| Training Plan | 42-person, 3-phase, 37-certification programme |
| Customer Onboarding Checklist | Data collection requirements + recommended tools |
| ARR Calculation | Partner revenue model ($835K/year recurring) |
| ROI Report (C-Suite) | 5-year financial projection, 285% ROI |
| AWS Pricing Calculator Guide | Service-by-service configuration for $448K/year estimate |
| Presentation Generator Agent | AI agent producing customer-ready documents from CSV data |

---

## Agentic Tooling

| Component | Purpose |
|-----------|---------|
| `preprocess.py` | Converts raw CSVs → structured context |
| `presentation_agent.py` | Generates executive summaries, status reports, GO/NO-GO packs, MAP milestone docs |
| `prompt_library/` | Customisable prompts per document type |
| Model | Amazon Nova Pro (us-west-2) via Strands Agents SDK |

**Partner workflow:**
```
Customer CSVs → preprocess.py → context.md → presentation_agent.py → Customer-ready documents
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Applications migrated | 20/20 |
| Total downtime | < 24 hours cumulative |
| Data loss | Zero |
| EHR availability (post-migration) | 99.95% |
| Cost reduction vs. on-premises | ≥ 38% |
| MAP $50K milestone | Achieved by Month 4 |
| Certifications | 37 |
| Customer operational independence | By Week 64 |
| On-premises decommissioned | By Week 75 |

---

## Next Steps

1. **Customer:** Provide application portfolio CSV, infrastructure CSV, and scope document
2. **Partner:** Run agentic tooling to generate initial deliverables
3. **Joint:** Review and customise outputs for customer context
4. **Partner:** Submit MAP application via AWS Partner Central
5. **Joint:** Execute Phase 1 (Assess) kickoff

---

*This document consolidates the complete migration programme. Detailed execution guidance is in the individual phase runbooks.*
