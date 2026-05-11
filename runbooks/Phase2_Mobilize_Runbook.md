# AWS MAP Migration Runbook — Phase 2: Mobilize

## Partner Delivery Guide | AWS Migration Acceleration Program

---

## Document Control

| Item | Detail |
|------|--------|
| Phase | 2 — Mobilize |
| Duration | 6–12 weeks |
| MAP Milestone | Landing zone operational, pilot migration complete |
| Audience | Customer-facing delivery teams |
| Worked Example | AnyCompany (Healthcare) |
| Prerequisite | Phase 1: Assess — GO decision achieved |

---

## 1. Phase Objectives

The Mobilize phase prepares the organisation and technical environment for at-scale migration. By the end of this phase:

- AWS landing zone deployed, secured, and validated
- Migration tooling configured and tested
- Operating model defined (CCoE, RACI, support processes)
- Team trained and certified on AWS fundamentals
- 1–3 pilot applications migrated end-to-end
- Detailed wave plans with cutover runbooks documented
- GO/NO-GO decision to proceed to Migrate phase

---

## 2. MAP Funding — Mobilize Phase

### Funding Activation

Once MAP is approved during Assess, credits become available during Mobilize:

| Activity | MAP Funding Applicability |
|----------|--------------------------|
| Landing zone build | Partner professional services — eligible |
| Migration tooling setup | AWS service usage — credits apply |
| Training & certification | AWS Training credits may be available |
| Pilot migration | AWS service consumption — credits apply |

### $50,000 Cumulative Spend Milestone

The MAP programme tracks cumulative AWS spend toward the $50,000 milestone:

- **Why it matters:** Reaching $50K cumulative spend unlocks additional MAP credits and validates programme momentum
- **When to track:** Begin tracking from first AWS resource provisioned (landing zone)
- **Acceleration levers:** Provision non-production environments early, run pilot workloads, enable logging/monitoring services

#### Worked Example — AnyCompany Spend Projection

| Phase | Monthly AWS Spend (Est.) | Cumulative | Milestone Status |
|-------|-------------------------|-----------|-----------------|
| Mobilize Month 1 (Landing zone) | $8,000 | $8,000 | — |
| Mobilize Month 2 (Tooling + Dev) | $12,000 | $20,000 | — |
| Mobilize Month 3 (Pilot migration) | $18,000 | $38,000 | — |
| Migrate Month 1 (Wave 1) | $25,000 | $63,000 | **$50K milestone achieved** |

**Acceleration Strategy (if milestone at risk):**
- Provision dev/test environments for Wave 1 apps during Mobilize
- Enable AWS CloudTrail, Config, GuardDuty, Security Hub across all accounts early
- Run performance/load testing for pilot apps on production-sized infrastructure
- Migrate non-production workloads (AnyCompany has 3 DEV/TEST apps) ahead of schedule

---

## 3. Landing Zone Setup

### 3.1 Multi-Account Strategy

**Objective:** Establish AWS account structure following AWS best practices for isolation, security, and governance.

#### Recommended Account Structure (AnyCompany)

| Account | Purpose | Key Services |
|---------|---------|-------------|
| Management Account | AWS Organizations root, billing, SCPs | Organizations, SSO, Billing |
| Security Account | Centralised logging, security tooling | CloudTrail, Config, GuardDuty, Security Hub |
| Network Account | Shared networking, connectivity | Transit Gateway, VPN, Direct Connect |
| Shared Services Account | CI/CD, artifact repos, DNS | CodePipeline, ECR, Route 53 |
| Production Account | Production workloads | ECS/EKS, RDS, S3 |
| Non-Production Account | Dev, Test, Staging | Same services, smaller sizing |
| Data Account | Analytics, data lake | Redshift, Glue, EMR, S3 Data Lake |
| HIPAA/Compliance Account | PHI workloads requiring isolation | EHR, Patient Portal, Claims (isolated) |

#### Service Control Policies (SCPs)

| Policy | Scope | Purpose |
|--------|-------|---------|
| Deny non-approved regions | All accounts | Restrict to approved regions only (data sovereignty) |
| Deny root user actions | All except Management | Prevent root credential usage |
| Require encryption | All accounts | Enforce EBS/S3/RDS encryption |
| Deny public S3 | All accounts | Prevent accidental public exposure of PHI |
| Require MFA for destructive actions | All accounts | Protect against accidental deletion |

### 3.2 Network Architecture

#### Connectivity Design (AnyCompany)

```
On-Premises (VMware DC)
    │
    ├── AWS Direct Connect (primary) — 1 Gbps dedicated
    ├── Site-to-Site VPN (backup) — IPSec tunnels
    │
    └── Transit Gateway (hub)
            ├── Production VPC (10.1.0.0/16)
            ├── Non-Production VPC (10.2.0.0/16)
            ├── Data VPC (10.3.0.0/16)
            ├── Shared Services VPC (10.4.0.0/16)
            └── HIPAA VPC (10.5.0.0/16)
```

#### VPC Design Pattern

| Subnet Tier | Purpose | Example CIDR | AZs |
|-------------|---------|-------------|-----|
| Public | Load balancers, NAT Gateways | 10.1.1.0/24, 10.1.2.0/24 | 2+ |
| Private (App) | Application containers/instances | 10.1.10.0/24, 10.1.11.0/24 | 2+ |
| Private (Data) | Databases, caches | 10.1.20.0/24, 10.1.21.0/24 | 2+ |
| Isolated | No internet — sensitive workloads | 10.1.30.0/24, 10.1.31.0/24 | 2+ |

#### Hybrid Connectivity Considerations (AnyCompany)

| Requirement | Solution | Notes |
|-------------|----------|-------|
| 800TB data transfer | AWS DataSync + Direct Connect | Phased transfer over weeks, not big-bang |
| HL7/FHIR integration (on-prem ↔ AWS) | Transit Gateway + VPN | Maintain connectivity during co-existence |
| DICOM imaging transfer | Direct Connect (high bandwidth) | Medical imaging = large file sizes |
| Active Directory integration | AWS Managed AD + AD Connector | Hybrid identity during transition |

### 3.3 Security Baseline

#### Identity and Access Management

| Component | Implementation | AnyCompany Context |
|-----------|---------------|-------------------|
| Identity Provider | AWS IAM Identity Center (SSO) | Federate with existing Active Directory |
| MFA | Enforce on all human users | Hardware tokens for admin, virtual MFA for users |
| Service accounts | IAM Roles (no long-lived keys) | Application workloads use instance/task roles |
| Privileged access | Temporary elevated access (breakglass) | Time-limited admin access with approval workflow |
| Least privilege | Permission boundaries per account | Scope by account, service, and resource |

#### HIPAA Compliance Controls

| Control | AWS Service | Configuration |
|---------|-------------|--------------|
| Encryption at rest | KMS (CMK) | All EBS, S3, RDS encrypted with customer-managed keys |
| Encryption in transit | ACM + TLS 1.2+ | ALB/NLB terminate TLS, internal service mesh encryption |
| Audit logging | CloudTrail (all regions) | Organisation trail, log file validation enabled |
| Access monitoring | GuardDuty + Security Hub | Automated findings, SNS alerting |
| Configuration compliance | AWS Config | HIPAA conformance pack rules |
| Data classification | Macie | Scan S3 for PHI/PII exposure |
| Backup & recovery | AWS Backup | Automated backup policies, cross-region copy |
| Network isolation | Security Groups + NACLs | Deny-all default, explicit allow rules |

#### BAA (Business Associate Agreement)

- Execute AWS BAA before any PHI touches AWS services
- Document HIPAA-eligible services only for PHI workloads
- Maintain inventory of PHI data flows across accounts

### 3.4 Logging and Monitoring Baseline

| Service | Purpose | Scope |
|---------|---------|-------|
| CloudTrail | API audit logging | Organisation-wide, all regions |
| AWS Config | Resource configuration compliance | All accounts, HIPAA conformance pack |
| GuardDuty | Threat detection | All accounts |
| Security Hub | Centralised security findings | Aggregated in Security account |
| CloudWatch | Operational monitoring | Per-account, centralised dashboards |
| VPC Flow Logs | Network traffic analysis | All VPCs |

---

## 4. Migration Tooling Setup

### 4.1 Tool Selection Matrix

| Migration Pattern | Recommended Tool | Use Case (AnyCompany) |
|-------------------|-----------------|----------------------|
| Server rehost (lift & shift) | AWS Application Migration Service (MGN) | Pharmacy Mgmt, Medical Imaging servers |
| Database migration | AWS Database Migration Service (DMS) | Oracle → RDS, PostgreSQL → Aurora, SQL Server → RDS |
| Large data transfer | AWS DataSync / Transfer Family | 800TB storage migration (SAN/NAS/MinIO → S3/EFS) |
| Container migration | Docker + ECR + ECS/EKS | 11 Replatform apps → containerised |
| Application modernisation | Refactoring (manual + tooling) | Claims Processing (COBOL), LIS (Java 8) |
| Progress tracking | AWS Migration Hub | Central dashboard for all migration streams |

### 4.2 Tool Configuration Checklist

| Tool | Configuration Steps | Validation |
|------|-------------------|-----------|
| MGN | Install replication agent on source servers, configure replication settings, set launch template | Test replication for 1 non-critical server |
| DMS | Create replication instance, configure source/target endpoints, create migration tasks | Run validation on test database |
| DataSync | Deploy agent on-premises, create source/destination locations, configure transfer tasks | Transfer 1TB test dataset, verify integrity |
| Migration Hub | Enable in target region, configure discovery connectors, link MGN/DMS | Verify all tools report status |

---

## 5. Operating Model Design

### 5.1 Cloud Centre of Excellence (CCoE)

#### Structure (AnyCompany)

| Role | Responsibility | Staffing |
|------|---------------|----------|
| CCoE Lead | Programme governance, stakeholder management | 1 (Customer) |
| Cloud Architect | Architecture standards, design reviews | 1 (Partner) + 1 (Customer) |
| Security Lead | Security controls, compliance validation | 1 (Partner) + 1 (Customer) |
| Migration Lead | Wave execution, cutover coordination | 1 (Partner) |
| DevOps Engineer | CI/CD, IaC, automation | 2 (Partner) + 1 (Customer) |
| Database Specialist | DMS, database migration, optimisation | 1 (Partner) |
| Application Teams | App-specific migration execution | Customer teams (per wave) |

### 5.2 RACI — Mobilize Phase

| Activity | Partner | Customer IT | Customer Exec | AWS |
|----------|---------|-------------|---------------|-----|
| Landing zone design & build | R, A | C | I | C |
| Security baseline implementation | R, A | R, C | I | C |
| Migration tool setup | R, A | C | I | I |
| Operating model design | R | R, A | A (approve) | C |
| Training delivery | R | R (attend) | I | C |
| Pilot app selection | C | R, A | I | I |
| Pilot migration execution | R, A | R, C | I | I |
| Wave plan detailing | R, A | C | I | C |
| GO/NO-GO decision | C | R | A (decide) | I |

### 5.3 Support Model

| Tier | Scope | Team | SLA |
|------|-------|------|-----|
| L1 | Monitoring alerts, basic triage | Customer NOC | 15 min response |
| L2 | Application/infrastructure troubleshooting | Customer IT + Partner | 1 hour response |
| L3 | Architecture, complex issues, AWS escalation | Partner + AWS Support | 4 hour response |
| Vendor | Third-party application issues (McKesson, Agfa, Sectra, Cerner) | Vendor support | Per vendor SLA |

### 5.4 Change Management Process

| Stage | Activity | Approval |
|-------|----------|----------|
| RFC Submission | Document change, impact, rollback plan | Requestor |
| Review | Technical review by CCoE | Cloud Architect |
| Approval | CAB approval for production changes | CCoE Lead + Customer IT Lead |
| Implementation | Execute change within maintenance window | Migration team |
| Validation | Post-change verification | Application owner |
| Closure | Document outcome, update CMDB | Migration Lead |

---

## 6. Skills Development

### 6.1 Training Plan (AnyCompany)

| Track | Target Audience | Content | Duration |
|-------|----------------|---------|----------|
| AWS Cloud Practitioner | All IT staff (30+) | Cloud fundamentals, AWS services overview | 1 week |
| Solutions Architect Associate | Architects, senior engineers (10) | Design, deploy, operate on AWS | 2 weeks |
| DevOps Engineer | DevOps team (5) | CI/CD, IaC, monitoring, automation | 2 weeks |
| Security Specialty | Security team (3) | IAM, encryption, compliance, incident response | 2 weeks |
| Database Specialty | DBA team (4) | RDS, Aurora, DMS, migration patterns | 2 weeks |
| Container/ECS/EKS | Application teams (8) | Docker, ECS task definitions, EKS basics | 1 week |

### 6.2 Certification Targets

| Certification | Target Count | Timeline |
|---------------|-------------|----------|
| Cloud Practitioner | 15 | End of Mobilize |
| Solutions Architect Associate | 5 | End of Mobilize |
| DevOps Engineer Associate | 3 | During Wave 1 |
| Security Specialty | 2 | During Wave 1 |
| Database Specialty | 2 | During Wave 1 |

### 6.3 Knowledge Transfer Activities

| Activity | Frequency | Delivered By |
|----------|-----------|-------------|
| Architecture design sessions | Weekly during Mobilize | Partner Architect |
| IaC workshops (hands-on) | 3 sessions | Partner DevOps |
| Security controls walkthrough | 2 sessions | Partner Security Lead |
| Migration tool training (MGN, DMS) | 2 sessions | Partner Migration Lead |
| Incident response simulation | 1 session | Partner + Customer |
| Pilot migration shadowing | During pilot | Partner (lead), Customer (shadow) |

---

## 7. Pilot Migration

### 7.1 Pilot Application Selection Criteria

| Criterion | Rationale |
|-----------|-----------|
| Low criticality (Tier 3) | Minimise business risk during learning |
| Few dependencies | Reduce coordination complexity |
| Representative technology | Validate tooling for broader portfolio |
| Non-production acceptable | Allow extended testing without business pressure |
| Willing application owner | Ensure cooperation and feedback |

### 7.2 Recommended Pilot Applications (AnyCompany)

| Application | Rationale | Migration Pattern |
|-------------|-----------|-------------------|
| Research Data Repository (APP-HC-017) | DEV environment, Python/PostgreSQL/MongoDB — representative of Replatform pattern, low risk | Containerise → ECS, PostgreSQL → Aurora, MongoDB → DocumentDB |
| Telemedicine Platform (APP-HC-014) | DEV environment, React/Node.js/PostgreSQL — validates container pipeline, modern stack | Containerise → ECS, PostgreSQL → Aurora |
| Nurse Workforce Management (APP-HC-016) | TEST environment, .NET 7/SQL Server — validates Windows/.NET migration path | Containerise → ECS, SQL Server → RDS SQL Server |

### 7.3 Pilot Execution Steps

| Step | Activity | Duration | Success Criteria |
|------|----------|----------|-----------------|
| 1 | Provision target infrastructure (IaC) | 2 days | Infrastructure deployed via CloudFormation/Terraform |
| 2 | Configure migration tooling | 2 days | DMS replication running, MGN agent installed |
| 3 | Migrate data | 3–5 days | Data validated — row counts, checksums match |
| 4 | Deploy application | 2 days | Application running on AWS, health checks passing |
| 5 | Integration testing | 3 days | All integrations functional, no errors |
| 6 | Performance testing | 2 days | Response times within baseline ±10% |
| 7 | Security validation | 2 days | Vulnerability scan clean, encryption verified |
| 8 | UAT sign-off | 2 days | Application owner confirms functionality |
| 9 | Document lessons learned | 1 day | Runbook updated, issues catalogued |

**Total pilot duration:** 3–4 weeks per application (run in parallel where possible)

### 7.4 Pilot Success Criteria

| Metric | Target |
|--------|--------|
| Application functional | 100% of test cases pass |
| Data integrity | Zero data loss, checksums validated |
| Performance | Within 10% of on-premises baseline |
| Security | No critical/high vulnerabilities |
| Availability | No unplanned downtime during pilot |
| Rollback tested | Successful rollback executed and validated |
| Team confidence | Team self-reports readiness to proceed |

### 7.5 Lessons Learned Template

| Category | Question | Capture |
|----------|----------|---------|
| Tooling | Did MGN/DMS/DataSync work as expected? | Issues, workarounds, configuration changes |
| Process | Were runbook steps sufficient? | Missing steps, unclear instructions |
| Timeline | Was the estimate accurate? | Actual vs. planned per step |
| Dependencies | Were all dependencies identified? | Missed integrations, unexpected failures |
| Rollback | Did rollback work cleanly? | Time to rollback, data consistency |
| Communication | Were stakeholders informed appropriately? | Gaps in notification, unclear ownership |

---

## 8. Detailed Wave Planning

### 8.1 Wave Plan Refinement

Using pilot lessons, refine the high-level wave plan from Assess into detailed execution plans:

#### Wave 0 — Foundation (Weeks 1–6 of Mobilize)

| Activity | Owner | Duration | Dependency |
|----------|-------|----------|-----------|
| Landing zone deployment | Partner Architect | 2 weeks | — |
| Security baseline implementation | Partner Security | 2 weeks | Landing zone |
| Network connectivity (Direct Connect/VPN) | Partner + Customer Network | 3 weeks | Landing zone |
| Migration tool setup (MGN, DMS, DataSync) | Partner Migration Lead | 1 week | Landing zone + connectivity |
| CI/CD pipeline setup | Partner DevOps | 2 weeks | Landing zone |
| Monitoring & alerting baseline | Partner DevOps | 1 week | Landing zone |
| Training programme launch | Partner | Ongoing | — |

#### Wave 1 — Low-Risk Applications (Weeks 7–14)

| Application | R-Type | Target Architecture | Key Risks |
|-------------|--------|-------------------|-----------|
| Medical Supply Chain (APP-HC-012) | Refactor | Java 8 → Java 17, JBoss → Spring Boot, MySQL → Aurora MySQL | Java 8 EOL code changes |
| Patient Discharge (APP-HC-019) | Retire/Replace | ASP.NET 4.8 → integrate into EHR module | Data migration to EHR |
| Telemedicine Platform (APP-HC-014) | Replatform | Containerise (ECS), PostgreSQL → Aurora | DEV only — low risk |
| Research Data Repository (APP-HC-017) | Replatform | Containerise (ECS), PostgreSQL → Aurora, MinIO → S3 | DEV only — low risk |

#### Wave 2 — Tier-2 Clinical Systems (Weeks 15–26)

| Application | R-Type | Target Architecture | Key Risks |
|-------------|--------|-------------------|-----------|
| Pharmacy Management (APP-HC-004) | Rehost | Lift & shift (McKesson) to EC2, Oracle → RDS Oracle | Vendor support validation |
| Medical Imaging & PACS (APP-HC-009) | Rehost | Lift & shift (Agfa) to EC2, MongoDB → DocumentDB | 500TB+ imaging data transfer |
| Radiology Information System (APP-HC-005) | Replatform | .NET 4.6 → .NET 8, SQL Server → RDS SQL Server | Legacy code upgrade |
| Laboratory Information System (APP-HC-006) | Refactor | Java 8 → Java 17, WebLogic → Spring Boot, SQL Server → RDS | Complex middleware replacement |
| Patient Scheduling (APP-HC-008) | Replatform | Containerise (ECS), PostgreSQL → Aurora | Circular dependency with EHR |
| Nurse Workforce Management (APP-HC-016) | Replatform | Containerise (ECS), SQL Server → RDS | TEST environment — lower risk |

#### Wave 3 — Core Platform (Weeks 27–40)

| Application | R-Type | Target Architecture | Key Risks |
|-------------|--------|-------------------|-----------|
| Patient Portal (APP-HC-002) | Replatform | Containerise (ECS), PostgreSQL → Aurora, Redis → ElastiCache | High user count (Tier 1) |
| Health Information Exchange (APP-HC-011) | Replatform | Containerise (ECS), Kafka → MSK, PostgreSQL → Aurora | Integration hub — many consumers |
| Clinical Decision Support (APP-HC-010) | Replatform | Containerise (ECS/EKS), PostgreSQL → Aurora, MongoDB → DocumentDB | Real-time clinical dependency |
| Compliance & Audit (APP-HC-018) | Replatform | Containerise (ECS), PostgreSQL → Aurora | Regulatory — must maintain audit trail |
| Medical Device Hub (APP-HC-020) | Replatform | Containerise (ECS), Kafka → MSK, Cassandra → Keyspaces, InfluxDB → Timestream | IoT/real-time — latency sensitive |

#### Wave 4 — Mission Critical (Weeks 41–56)

| Application | R-Type | Target Architecture | Key Risks |
|-------------|--------|-------------------|-----------|
| Electronic Health Records (APP-HC-001) | Replatform | Containerise (ECS/EKS), Oracle → RDS Oracle (then Aurora), Kafka → MSK | Central hub — highest risk, most dependencies |
| Revenue Cycle Management (APP-HC-007) | Replatform | Containerise (ECS), Oracle → Aurora PostgreSQL, Kafka → MSK | Financial system — zero data loss required |
| Claims Processing (APP-HC-015) | Refactor | COBOL → Java 17/Spring Boot, Oracle → Aurora, WebLogic eliminated | Most complex — COBOL modernisation |
| Clinical Data Warehouse (APP-HC-003) | Refactor | Spark → EMR/Glue, Hadoop → S3 Data Lake, PostgreSQL → Redshift | Big data platform rebuild |
| EHR Analytics Platform (APP-HC-013) | Refactor | Spark → EMR, Airflow → MWAA, Hadoop → S3, Cassandra → Keyspaces | Large data volumes, ML pipelines |

### 8.2 Cutover Runbook Template

For each wave, prepare a cutover runbook following this structure:

| Section | Content |
|---------|---------|
| **Pre-Migration Checklist** | Environment readiness, backups verified, stakeholder sign-off, change approval |
| **Replication & Staging** | DMS/MGN replication status, data sync validation, staging environment ready |
| **Test Cutover** | Rehearsal steps, duration per step, Go/No-Go criteria |
| **Cutover Execution** | Timestamped steps (T+0, T+30min, etc.), DNS changes, service switchover |
| **Rollback Plan** | Triggers (what constitutes failure), rollback steps, maximum rollback window |
| **Post-Migration Validation** | Health checks, performance tests, data integrity, integration tests |
| **Hypercare** | 1–2 week enhanced support, monitoring thresholds, escalation paths |
| **Communication Plan** | Who to notify, when, via what channel |

---

## 9. Data Migration Strategy

### 9.1 Storage Migration Plan (AnyCompany — 800TB+)

| Source | Size | Target | Method | Duration (Est.) |
|--------|------|--------|--------|----------------|
| SAN (block) | 100 TB | EBS (gp3/io2) | MGN replication + DataSync | 2–3 weeks |
| NAS (file) | 200 TB | EFS / FSx | DataSync (incremental) | 3–4 weeks |
| MinIO (object) | 500 TB | S3 (Standard + IA + Glacier) | DataSync + S3 Transfer Acceleration | 4–6 weeks |

### 9.2 Database Migration Plan

| Source Database | Target | Method | Downtime Strategy |
|----------------|--------|--------|-------------------|
| Oracle 19c (RAC) | RDS Oracle → Aurora PostgreSQL (future) | DMS CDC (continuous replication) | Minimal — final sync + cutover |
| MS SQL Server 2019/2022 | RDS SQL Server | DMS CDC | Minimal — final sync + cutover |
| PostgreSQL 15 | Aurora PostgreSQL | DMS CDC or native logical replication | Near-zero — logical replication |
| MySQL 8.0 | Aurora MySQL | DMS CDC | Minimal — final sync + cutover |
| MongoDB 6.0 | DocumentDB | DMS or mongodump/mongorestore | Planned window (hours) |
| Cassandra 4.1 | Amazon Keyspaces | Custom ETL or DMS | Planned window |
| InfluxDB 2.7 | Amazon Timestream | Custom migration script | Planned window |

### 9.3 Data Validation Framework

| Check | Method | Frequency |
|-------|--------|-----------|
| Row count comparison | Source vs. target count queries | After each sync cycle |
| Checksum validation | MD5/SHA-256 on sample records | Daily during replication |
| Referential integrity | FK constraint validation on target | Post-migration |
| Application-level validation | Run application test suite against target DB | Pre-cutover |
| PHI data audit | Verify encryption, access controls on target | Post-migration |

---

## 10. Phase Exit Criteria — GO/NO-GO to Migrate

### Mandatory (Must Have)

- [ ] Landing zone deployed and security-validated
- [ ] Network connectivity operational (Direct Connect/VPN)
- [ ] Migration tools configured and tested
- [ ] At least 1 pilot application migrated successfully
- [ ] Rollback procedure tested and documented
- [ ] Operating model documented and agreed
- [ ] Core team trained (minimum Cloud Practitioner level)
- [ ] Detailed Wave 1 plan with cutover runbook complete
- [ ] Change management process operational
- [ ] HIPAA BAA executed with AWS

### Recommended (Should Have)

- [ ] 2–3 pilot applications migrated
- [ ] CI/CD pipeline operational for IaC deployments
- [ ] Monitoring and alerting baseline active
- [ ] All wave plans detailed (Waves 1–4)
- [ ] Vendor coordination confirmed (McKesson, Agfa, Sectra, Cerner)
- [ ] DR/backup strategy validated
- [ ] Cost baseline established for MAP milestone tracking

### Decision Gate

| Outcome | Criteria | Next Step |
|---------|----------|-----------|
| **GO** | All mandatory items complete, pilot successful | Proceed to Phase 3: Migrate & Modernize |
| **CONDITIONAL GO** | 1–2 items incomplete, clear remediation plan | Proceed with parallel remediation (2 weeks max) |
| **NO-GO** | Pilot failed, security gaps unresolved, or team not ready | Extend Mobilize, address blockers |

---

## 11. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Direct Connect provisioning delay | Medium | High | Order early (Week 1), use VPN as interim |
| Pilot migration failure | Low | Medium | Select lowest-risk app, have rollback ready |
| Skills gap persists after training | Medium | High | Embed partner engineers in customer team, pair programming |
| Vendor non-cooperation (McKesson, Agfa) | Low | High | Engage vendors in Week 1, document support requirements |
| HIPAA compliance gap in landing zone | Medium | Critical | Security review before any PHI migration, engage AWS HIPAA specialist |
| 800TB data transfer timeline overrun | High | Medium | Start DataSync early, run in parallel with other activities |
| Scope creep (additional apps added) | Medium | Medium | Strict change control, defer to future waves |

---

## 12. Timeline Summary

```
Week 1–2:   Landing zone design & deployment, Direct Connect order
Week 2–3:   Security baseline, IAM, encryption, compliance controls
Week 3–4:   Network connectivity validation, migration tool setup
Week 4–5:   CI/CD pipeline, monitoring baseline, training kickoff
Week 5–8:   Pilot migration execution (2–3 apps in parallel)
Week 8–9:   Pilot validation, lessons learned, runbook refinement
Week 9–11:  Detailed wave planning, cutover runbook development
Week 11–12: GO/NO-GO review, stakeholder sign-off, Migrate phase kickoff
```

---

## 13. Deliverables Checklist

| # | Deliverable | Format | Owner |
|---|-------------|--------|-------|
| 1 | Landing Zone (deployed) | AWS accounts + IaC templates | Partner Architect |
| 2 | Network Design Document | Architecture diagram + config | Partner Network |
| 3 | Security Baseline Document | Controls matrix + evidence | Partner Security |
| 4 | Migration Tool Configuration | Runbook + validation results | Partner Migration Lead |
| 5 | Operating Model Document | RACI, support model, processes | Partner + Customer |
| 6 | Training Completion Report | Certifications, attendance | Partner Training |
| 7 | Pilot Migration Report | Results, lessons learned, metrics | Partner Migration Lead |
| 8 | Detailed Wave Plans (1–4) | Spreadsheet + Gantt | Programme Manager |
| 9 | Cutover Runbook (Wave 1) | Step-by-step document | Partner Migration Lead |
| 10 | Data Migration Strategy | Plan + validation framework | Partner DBA |
| 11 | GO/NO-GO Presentation | Executive summary | Engagement Manager |

---

*End of Phase 2: Mobilize Runbook*
