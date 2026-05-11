# AWS MAP Migration Runbook — Phase 1: Assess

## Partner Delivery Guide | AWS Migration Acceleration Program

---

## Document Control

| Item | Detail |
|------|--------|
| Phase | 1 — Assess |
| Duration | 4–8 weeks |
| MAP Milestone | Migration Readiness Assessment (MRA) completion |
| Audience | Customer-facing delivery teams |
| Worked Example | AnyCompany (Healthcare) |

---

## 1. Phase Objectives

The Assess phase establishes the factual foundation for the entire migration programme. By the end of this phase, the delivery team must have:

- A complete application portfolio inventory with criticality classification
- An infrastructure inventory with dependency mapping
- A validated business case with TCO/ROI analysis
- A Migration Readiness Assessment (MRA) with scored dimensions
- A high-level migration strategy with 6Rs classification and wave plan
- Executive GO/NO-GO decision to proceed to Mobilize

---

## 2. MAP Funding Eligibility — Assess Phase

### What Qualifies

AWS MAP provides funding to offset migration costs. During the Assess phase:

- **Migration Readiness Assessment (MRA)** — Completing the MRA through the AWS Partner Central MAP portal is a prerequisite for MAP funding eligibility
- **Business case development** — Documented TCO analysis demonstrating cost savings supports the MAP application
- **Portfolio discovery** — Comprehensive inventory of workloads intended for migration establishes the MAP scope

### Partner Actions Required

1. Register the opportunity in AWS Partner Central under MAP
2. Complete the MRA using the AWS MAP MRA tool (or equivalent methodology documented below)
3. Submit the MRA results and business case to the AWS Partner Development Manager (PDM)
4. Obtain MAP approval before proceeding to Mobilize to unlock funding credits

### Funding Thresholds

| Criteria | Requirement |
|----------|-------------|
| Minimum qualifying workloads | Varies by programme tier — confirm with PDM |
| Annual AWS spend commitment | Typically $50,000+ cumulative within first year |
| MRA completion | Mandatory |
| Business case | Mandatory |

> **Note:** MAP terms evolve. Always confirm current eligibility criteria with your AWS PDM before committing timelines to the customer.

---

## 3. Delivery Activities

### 3.1 Application Portfolio Discovery

**Objective:** Catalogue every application in scope with sufficient metadata to classify, prioritise, and plan migration.

#### Data Collection Template

Collect the following fields for each application:

| Field | Description | Example (AnyCompany) |
|-------|-------------|---------------------|
| App ID | Unique identifier | APP-HC-001 |
| App Name | Application name | Electronic Health Records (EHR) |
| Category | Home Grown / Legacy / Third Party / SaaS | Home Grown |
| Type | Web App / Batch / Microservices / Monolith | Web Application |
| Business Function | Primary business capability | Clinical Operations |
| Primary Language | Tech stack | Java 17 / Angular 14 |
| Database | Database dependencies | Oracle 19c |
| Middleware | Middleware dependencies | JBoss EAP 7.4 / Apache Kafka 3.2 |
| Integrations | Integration protocols | REST API / HL7 FHIR R4 |
| Environment | Prod / Dev / Test | PRODUCTION |
| Business Unit | Owning department | Clinical Services |
| Criticality | Critical / High / Medium / Low | Critical |
| SLA Tier | Tier 1 / 2 / 3 | Tier 1 |
| Owner Team | Responsible team | Clinical IT |

#### Worked Example — AnyCompany Portfolio Summary

From the AnyCompany healthcare discovery:

| Classification | Count | Examples |
|---------------|-------|----------|
| Home Grown | 12 | EHR, Patient Portal, Revenue Cycle Management, Clinical Decision Support |
| Legacy | 5 | Radiology Information System (C# 6.0/.NET 4.6), Laboratory Information System (Java 8), Claims Processing (COBOL), Medical Supply Chain (Java 8 J2EE), Patient Discharge (ASP.NET 4.8) |
| Third Party | 2 | Pharmacy Management (McKesson), Medical Imaging & PACS (Agfa) |
| SaaS | 1 | (None in scope — third-party vendors retained) |

**Criticality Distribution:**

| Tier | Count | Applications |
|------|-------|-------------|
| Critical / Tier 1 | 7 | EHR, Patient Portal, Clinical Data Warehouse, Revenue Cycle, HIE, EHR Analytics, Claims Processing, Medical Device Hub |
| High / Tier 2 | 8 | Pharmacy Mgmt, RIS, LIS, Patient Scheduling, Medical Imaging, Clinical Decision Support, Telemedicine, Compliance & Audit |
| Medium / Tier 3 | 5 | Medical Supply Chain, Nurse Workforce Mgmt, Research Data Repository, Patient Discharge, (DEV/TEST environments) |

#### Risk Signal Identification

Flag applications with End-of-Life (EOL) or high-risk technology:

| Risk Signal | Applications Affected | Impact |
|-------------|----------------------|--------|
| Java 8 (EOL runtime) | Laboratory Information System, Medical Supply Chain, Claims Processing | Requires replatform or refactor — no vendor patches |
| COBOL | Claims Processing System | Critical legacy — limited developer availability |
| ASP.NET 4.8 / .NET 4.6 | Patient Discharge System, Radiology Information System | Windows-only, no cross-platform support |
| WebLogic 12c (aging middleware) | Laboratory Information System, Claims Processing | Licensing cost, limited cloud support |
| IBM MQ 9.2 | Pharmacy Mgmt, LIS, Supply Chain, Claims Processing | Requires integration redesign or managed alternative |

---

### 3.2 Infrastructure Inventory

**Objective:** Document all physical and virtual infrastructure supporting in-scope applications.

#### Data Collection Template

| Field | Description | Example (AnyCompany) |
|-------|-------------|---------------------|
| Infra ID | Unique identifier | INFRA-HC-002 |
| Server Name | Hostname | hlth-ora-rac-prod-01 |
| CPU Cores | vCPU count | 32 |
| Memory (MB) | RAM allocation | 262,144 (256 GB) |
| Storage (GB) | Provisioned disk | 4,096 |
| Virtual? | Yes/No | Yes |
| Hypervisor | VMware / Hyper-V / Bare Metal | VMware |
| Workload Type | DB / Web / Big Data / Storage | Database Server |
| Operating System | OS and version | Oracle Linux 8 (64-bit) |
| Environment | Prod / Dev / Test | PRODUCTION |

#### Worked Example — AnyCompany Infrastructure Summary

| Category | Count | Total Resources |
|----------|-------|----------------|
| Production Servers | 15 | 244 vCPU, 1.5 TB RAM |
| Dev/Test Servers | 5 | 52 vCPU, 229 GB RAM |
| Storage (SAN) | 1 | 100 TB block |
| Storage (NAS) | 1 | 200 TB file |
| Storage (Object/MinIO) | 1 | 500 TB object |
| **Total Storage** | — | **800+ TB** |

**Shared Infrastructure Concentration Risk:**

| Server | Hosted Applications | Risk |
|--------|-------------------|------|
| hlth-ora-rac-prod-01 (INFRA-HC-002) | EHR, Pharmacy Mgmt, Revenue Cycle, Claims Processing | **Critical** — 4 Tier-1/Tier-2 apps share one Oracle RAC cluster |
| hlth-pgsql-primary-prod-01 (INFRA-HC-004) | Patient Portal, Patient Scheduling, HIE, Compliance & Audit | **High** — 4 apps on single PostgreSQL primary |
| hlth-mssql-prod-01 (INFRA-HC-003) | RIS, LIS | **Medium** — 2 clinical apps share SQL Server |

---

### 3.3 Dependency Mapping

**Objective:** Map application-to-application and application-to-infrastructure dependencies to identify migration constraints.

#### Approach

1. Parse integration fields from the application inventory (Integration_Dependencies, Integrated_Apps)
2. Build a directed dependency graph
3. Identify circular dependencies (co-migration groups)
4. Calculate complexity scores based on dependency count and criticality

#### Worked Example — AnyCompany Key Dependencies

**High-Dependency Applications (Hub Systems):**

| Application | Depends On | Depended On By | Complexity |
|-------------|-----------|----------------|------------|
| EHR (APP-HC-001) | — | Patient Portal, Clinical Data Warehouse, Pharmacy, RIS, LIS, Revenue Cycle, Patient Scheduling, Clinical Decision Support, HIE, Compliance, Patient Discharge, Medical Device Hub | **Very High** — central hub |
| Apache Kafka (middleware) | — | EHR, Revenue Cycle, Clinical Decision Support, HIE, EHR Analytics, Medical Device Hub | **High** — event backbone |
| Oracle 19c (INFRA-HC-002) | — | EHR, Pharmacy, Revenue Cycle, Claims Processing | **High** — shared database tier |

**Circular Dependencies (Co-Migration Groups):**

| Cycle | Applications | Migration Impact |
|-------|-------------|-----------------|
| Cycle 1 | EHR ↔ Patient Portal ↔ Patient Scheduling | Must migrate together or implement abstraction layer |
| Cycle 2 | EHR ↔ Revenue Cycle ↔ Claims Processing | Financial systems tightly coupled — parallel cutover required |
| Cycle 3 | Clinical Decision Support ↔ EHR ↔ Medical Device Hub | Real-time clinical data flow — cannot break chain |

---

### 3.4 Business Case Development

**Objective:** Quantify the financial justification for migration to support executive approval and MAP funding application.

#### TCO Analysis Framework

| Cost Category | On-Premises (Annual) | AWS Projected (Annual) | Savings |
|--------------|---------------------|----------------------|---------|
| Compute (servers, virtualisation) | Current VMware + hardware costs | EC2/ECS/Lambda equivalent | Estimate 30–40% |
| Storage (800+ TB) | SAN/NAS/MinIO licensing + hardware | S3/EBS/EFS/FSx | Estimate 40–60% |
| Database licensing | Oracle, SQL Server, middleware | RDS/Aurora/managed services | Estimate 30–50% |
| Facilities & power | Data centre OpEx | Eliminated | 100% |
| Staff (operations) | Current headcount | Reduced with managed services | Estimate 20–30% |
| **Total** | **Baseline** | **Projected** | **Target 35–45%** |

#### Business Drivers (AnyCompany Example)

| Driver | Current Pain | Expected Outcome |
|--------|-------------|-----------------|
| Legacy/EOL applications | 5 apps on unsupported platforms — security risk, no patches | Modernised on supported, managed services |
| HIPAA compliance | Manual compliance controls, audit burden | Automated compliance with AWS Config, CloudTrail, GuardDuty |
| Scalability | Fixed capacity — cannot handle clinical workload spikes | Auto-scaling for EHR, analytics, telemedicine |
| Cost optimisation | VMware licensing, 800TB storage hardware refresh due | Pay-as-you-go, tiered storage (S3 Glacier for archives) |
| Innovation | No ML/AI capability for clinical decision support | Amazon Bedrock, SageMaker for clinical analytics |

---

### 3.5 Migration Readiness Assessment (MRA)

**Objective:** Score organisational readiness across six dimensions to identify gaps that must be addressed in Mobilize.

#### MRA Dimensions and Scoring

Score each dimension 1–5 (1 = Not Ready, 5 = Fully Ready):

| Dimension | Score | Key Findings (AnyCompany Example) |
|-----------|-------|----------------------------------|
| Business & Strategy | 4.5 | Strong executive sponsorship, clear ROI, well-defined drivers |
| People & Process | 2.8 | Limited cloud skills (15% have basic AWS), waterfall methodology, manual deployments |
| Platform & Architecture | 2.5 | Legacy monoliths (80%), aging middleware, 800TB data challenge |
| Security & Compliance | 3.0 | HIPAA controls exist but manual, fragmented identity management, limited encryption |
| Operations & Management | 3.5 | 24/7 NOC exists, ITIL processes, but reactive monitoring and manual deployments |
| Migration Experience | 2.0 | No prior cloud migration, limited SaaS adoption only |
| **Overall** | **3.1** | **Moderate Readiness — proceed to Mobilize with targeted remediation** |

#### Gap Analysis and Remediation Plan

| Gap | Severity | Remediation Required (Mobilize Phase) |
|-----|----------|--------------------------------------|
| Cloud skills deficit | High | AWS training programme for 30+ staff, 15 certifications target |
| No IaC capability | High | Implement CloudFormation/Terraform, CI/CD pipelines |
| Manual compliance controls | Medium | Automate with AWS Config rules, Security Hub |
| Monolithic architecture | Medium | Containerisation strategy for Home Grown apps |
| No migration tooling experience | High | Pilot migration with MGN/DMS in Mobilize |
| Fragmented identity | Medium | Consolidate to AWS IAM Identity Center |

---

### 3.6 Migration Strategy — 6Rs Classification

**Objective:** Assign a migration strategy (R-type) to every in-scope application.

#### Classification Criteria

| R-Type | When to Apply | Effort | Timeline |
|--------|--------------|--------|----------|
| **Rehost** | Stable apps, tight timeline, no business case for change | Low | 1–3 months |
| **Replatform** | Apps benefiting from managed services (DB, caching, LB) | Medium | 2–4 months |
| **Refactor** | Business-critical apps needing cloud-native architecture | High | 6–18 months |
| **Repurchase** | Standard functions with SaaS alternatives | Medium | 3–6 months |
| **Retire** | Redundant, unused, or EOL with replacement available | Low | 1–2 months |
| **Retain** | Compliance constraints, recent investment, not ready | None | Revisit 6–12 months |

#### Worked Example — AnyCompany 6Rs Assignment

| Application | R-Type | Rationale |
|-------------|--------|-----------|
| Electronic Health Records (EHR) | Replatform | Critical system — move to managed DB (RDS Oracle), containerise app tier. Too risky to refactor immediately. |
| Patient Portal | Replatform | Modern stack (React/Node.js) — containerise on ECS, move PostgreSQL to Aurora |
| Clinical Data Warehouse | Refactor | Migrate Hadoop/Spark to EMR/Glue/Redshift — cloud-native analytics |
| Pharmacy Management (McKesson) | Rehost | Third-party vendor — lift and shift, maintain vendor support |
| Radiology Information System | Replatform | Legacy .NET 4.6 — upgrade to .NET 8, move SQL Server to RDS |
| Laboratory Information System | Refactor | Java 8 + WebLogic EOL — must modernise to supported stack |
| Revenue Cycle Management | Replatform | Modern microservices (Java 17/Spring Boot) — containerise, move to Aurora |
| Patient Scheduling | Replatform | Python/Django — containerise, move PostgreSQL to Aurora |
| Medical Imaging & PACS | Rehost | Third-party (Agfa) — lift and shift, large storage footprint |
| Clinical Decision Support | Replatform | Modern microservices — containerise on ECS/EKS |
| Health Information Exchange | Replatform | Modern stack — containerise, leverage managed Kafka (MSK) |
| Medical Supply Chain | Refactor | Java 8 J2EE + JBoss 6.4 EOL — must modernise |
| EHR Analytics Platform | Refactor | Big data platform — migrate to EMR/Glue/Athena/SageMaker |
| Telemedicine Platform | Replatform | Modern stack (React/Node.js/WebRTC) — containerise, currently DEV |
| Claims Processing | Refactor | COBOL + WebLogic — critical legacy requiring full modernisation |
| Nurse Workforce Management | Replatform | .NET 7 — containerise on ECS, move to RDS SQL Server |
| Research Data Repository | Replatform | Python — containerise, move to S3/Aurora, currently DEV |
| Compliance & Audit System | Replatform | Java 17/Angular — containerise, move PostgreSQL to Aurora |
| Patient Discharge & Transfer | Retire/Refactor | ASP.NET 4.8 legacy — replace with modern module in EHR |
| Medical Device Integration Hub | Replatform | Modern microservices (Java 17/Python) — containerise, move to managed Kafka + Timestream |

**Distribution Summary:**

| R-Type | Count | Percentage |
|--------|-------|-----------|
| Replatform | 11 | 55% |
| Refactor | 5 | 25% |
| Rehost | 2 | 10% |
| Retire | 1 | 5% |
| Retain | 1 | 5% |
| **Total** | **20** | **100%** |

---

### 3.7 High-Level Wave Plan

**Objective:** Group applications into migration waves based on dependency constraints, criticality, and risk tolerance.

#### Wave Planning Strategy

For AnyCompany, the recommended wave planning approach combines:
1. **Dependency Chain Depth** — Migrate providers before consumers
2. **Business Criticality** — Lower-risk apps first to build confidence
3. **Shared Infrastructure** — Co-located apps migrate together

#### Proposed Wave Structure

| Wave | Timeframe | Applications | Strategy | Rationale |
|------|-----------|-------------|----------|-----------|
| Wave 0 | Weeks 1–6 | Foundation (no apps) | Landing zone, tooling, training | Pre-requisites |
| Wave 1 | Weeks 7–14 | Medical Supply Chain, Patient Discharge, Telemedicine (DEV), Research Data Repo (DEV) | Refactor, Retire, Replatform | Low-risk, non-critical — build team confidence |
| Wave 2 | Weeks 15–26 | Pharmacy Mgmt, Medical Imaging, RIS, LIS, Patient Scheduling, Nurse Workforce | Rehost, Replatform, Refactor | Tier-2 apps, resolve shared infra (MSSQL) |
| Wave 3 | Weeks 27–40 | Patient Portal, HIE, Clinical Decision Support, Compliance & Audit, Medical Device Hub | Replatform | Tier-1/2 apps with EHR dependencies |
| Wave 4 | Weeks 41–56 | EHR, Revenue Cycle, Claims Processing, Clinical Data Warehouse, EHR Analytics | Replatform, Refactor | Most critical, most complex — team fully experienced |

---

## 4. Phase Exit Criteria — GO/NO-GO to Mobilize

### Mandatory (Must Have)

- [ ] Application portfolio inventory complete (all in-scope apps documented)
- [ ] Infrastructure inventory complete (all servers, storage, network documented)
- [ ] Dependency map validated with application owners
- [ ] Business case approved by executive sponsor
- [ ] MRA completed and submitted to AWS (MAP portal)
- [ ] 6Rs classification assigned to every application
- [ ] High-level wave plan agreed with stakeholders
- [ ] MAP funding application submitted

### Recommended (Should Have)

- [ ] Risk register created with mitigation strategies
- [ ] Skills gap analysis completed
- [ ] Compliance requirements documented per application
- [ ] Data classification completed (HIPAA PHI identification)
- [ ] Network connectivity requirements documented
- [ ] Estimated timeline and budget approved

### Decision Gate

| Outcome | Criteria | Next Step |
|---------|----------|-----------|
| **GO** | All mandatory items complete, MRA score ≥ 2.5 overall | Proceed to Phase 2: Mobilize |
| **CONDITIONAL GO** | 1–2 mandatory items incomplete but in progress | Proceed with time-boxed remediation (2 weeks max) |
| **NO-GO** | MRA score < 2.0 in any dimension, or business case not approved | Extend Assess phase, address critical gaps |

---

## 5. Deliverables Checklist

| # | Deliverable | Format | Owner |
|---|-------------|--------|-------|
| 1 | Application Portfolio Inventory | CSV/Spreadsheet | Delivery Lead |
| 2 | Infrastructure Inventory | CSV/Spreadsheet | Infrastructure Architect |
| 3 | Dependency Map | Diagram + Matrix | Solutions Architect |
| 4 | Business Case Document | PDF/Presentation | Engagement Manager |
| 5 | Migration Readiness Assessment | MRA Report (MAP portal) | Delivery Lead |
| 6 | 6Rs Classification Matrix | Spreadsheet | Solutions Architect |
| 7 | High-Level Wave Plan | Document + Gantt | Programme Manager |
| 8 | Risk Register | Spreadsheet | Programme Manager |
| 9 | Executive Presentation | PowerPoint/PDF | Engagement Manager |
| 10 | MAP Funding Application | AWS Partner Central | Partner Development |

---

## 6. RACI Matrix — Assess Phase

| Activity | Partner Delivery | Customer IT | Customer Exec | AWS PDM |
|----------|-----------------|-------------|---------------|---------|
| Portfolio Discovery | R, A | C, I | I | I |
| Infrastructure Inventory | R, A | R, C | I | I |
| Dependency Mapping | R, A | C | I | I |
| Business Case | R, A | C | A (approver) | C |
| MRA Execution | R, A | C | I | C |
| 6Rs Classification | R, A | C | I | I |
| Wave Planning | R, A | C | I | C |
| MAP Application | R | I | I | A |

R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## 7. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Incomplete application inventory (shadow IT) | Medium | High | Cross-reference with network discovery, interview all business units |
| Stakeholder availability for interviews | High | Medium | Schedule 2 weeks ahead, provide questionnaires as fallback |
| Underestimated dependencies | Medium | High | Validate with network traffic analysis, not just documentation |
| Business case rejected | Low | Critical | Engage CFO early, align with existing budget cycles |
| MAP eligibility criteria change | Low | Medium | Confirm with PDM at project start, build flexibility into timeline |
| HIPAA data handling during discovery | Medium | High | Use anonymised data in shared documents, restrict PHI access |

---

## 8. Timeline Summary

```
Week 1–2:  Kickoff, stakeholder interviews, data collection templates distributed
Week 2–4:  Application portfolio discovery, infrastructure inventory
Week 3–5:  Dependency mapping, risk signal identification
Week 4–6:  Business case development, TCO analysis
Week 5–7:  MRA execution (6 dimensions), 6Rs classification
Week 6–8:  Wave planning, executive presentation, GO/NO-GO decision
Week 7–8:  MAP application submission, Mobilize planning
```

---

*End of Phase 1: Assess Runbook*
