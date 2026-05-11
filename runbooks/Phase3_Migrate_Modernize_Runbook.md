# AWS MAP Migration Runbook — Phase 3: Migrate & Modernize

## Partner Delivery Guide | AWS Migration Acceleration Program

---

## Document Control

| Item | Detail |
|------|--------|
| Phase | 3 — Migrate & Modernize |
| Duration | 12–14 months (Waves 1–4) |
| MAP Milestone | $50K spend achieved, workloads operational in AWS |
| Audience | Customer-facing delivery teams |
| Worked Example | AnyCompany (Healthcare) |
| Prerequisite | Phase 2: Mobilize — GO decision achieved, pilot complete |

---

## 1. Phase Objectives

The Migrate & Modernize phase executes the wave plan at scale and transitions workloads to optimised cloud-native architectures. By the end of this phase:

- All in-scope applications migrated to AWS (20 applications across 4 waves)
- On-premises infrastructure decommissioned
- Post-migration optimisation complete (right-sizing, Savings Plans)
- Modernization roadmap initiated for refactored applications
- MAP $50K cumulative spend milestone achieved and reported
- Operational steady-state established

---

## 2. MAP Funding — Migrate & Modernize Phase

### $50K Milestone Achievement

| Month | Activity | Monthly Spend (Est.) | Cumulative | Status |
|-------|----------|---------------------|-----------|--------|
| Mobilize M1 | Landing zone, security services | $8,000 | $8,000 | — |
| Mobilize M2 | Tooling, dev environments | $12,000 | $20,000 | — |
| Mobilize M3 | Pilot migrations | $18,000 | $38,000 | — |
| Migrate M1 (Wave 1) | 4 apps migrated, storage transfer begins | $25,000 | $63,000 | **Milestone achieved** |
| Migrate M2 | Wave 2 begins | $30,000 | $93,000 | — |

### Post-Milestone Actions

1. Report milestone achievement to AWS PDM via Partner Central
2. Submit evidence: AWS Cost Explorer screenshot showing cumulative spend
3. Unlock additional MAP credits (amount per programme tier)
4. Apply credits to ongoing migration compute and storage costs

### Ongoing Cost Tracking

| Metric | Tool | Frequency |
|--------|------|-----------|
| Monthly spend by account | AWS Cost Explorer | Weekly |
| Spend by service | Cost Explorer + Cost Allocation Tags | Weekly |
| Budget alerts | AWS Budgets | Automated (80%, 100% thresholds) |
| MAP credit utilisation | Partner Central | Monthly |
| Forecast vs. actual | Cost Explorer forecast | Bi-weekly |

---

## 3. Wave Execution Framework

### 3.1 Wave Lifecycle (Repeat for Each Wave)

Each wave follows a consistent lifecycle:

```
Pre-Migration → Replication & Staging → Test Cutover → Cutover Execution → Post-Migration → Hypercare → Closure
```

| Stage | Duration | Key Activities |
|-------|----------|---------------|
| Pre-Migration | 1–2 weeks | Readiness checks, backups, approvals, communication |
| Replication & Staging | 1–3 weeks | Data sync, environment provisioning, agent setup |
| Test Cutover | 3–5 days | Rehearsal, timing validation, Go/No-Go |
| Cutover Execution | 4–12 hours | DNS switch, service cutover, validation |
| Post-Migration | 1 week | Health checks, performance, integration testing |
| Hypercare | 2 weeks | Enhanced monitoring, rapid response, issue resolution |
| Closure | 2–3 days | Decommission source, documentation, lessons learned |

### 3.2 Pre-Migration Checklist (Universal)

| # | Check | Owner | Evidence |
|---|-------|-------|----------|
| 1 | Target infrastructure provisioned and validated | Cloud Architect | IaC deployment successful |
| 2 | Data replication running and in sync | DBA / Migration Lead | DMS/DataSync status = healthy |
| 3 | Application code deployed to target | DevOps | CI/CD pipeline green |
| 4 | Security controls validated | Security Lead | Scan results clean |
| 5 | Rollback plan documented and tested | Migration Lead | Rollback runbook signed off |
| 6 | Backup of source system taken | DBA | Backup verification log |
| 7 | Stakeholder communication sent | Programme Manager | Email/Slack confirmation |
| 8 | Change approval obtained | CCoE Lead | CAB approval record |
| 9 | Monitoring and alerting configured | DevOps | Dashboard + alert test |
| 10 | Vendor notified (if third-party) | Engagement Manager | Vendor acknowledgement |

### 3.3 Cutover Execution Template

| Time | Step | Action | Owner | Rollback Trigger |
|------|------|--------|-------|-----------------|
| T-60min | Final sync | Trigger final DMS/DataSync incremental sync | DBA | Sync failure |
| T-30min | Source freeze | Stop writes to source application | App Owner | — |
| T-15min | Validation | Verify target data matches source (row counts, checksums) | DBA | Data mismatch > 0.01% |
| T+0 | DNS cutover | Update DNS records to point to AWS endpoints | Network Engineer | — |
| T+5min | Service start | Start application services on AWS | DevOps | Application fails to start |
| T+10min | Smoke test | Execute critical path test cases | QA Lead | >2 test failures |
| T+20min | Traffic validation | Confirm user traffic flowing to AWS | Network Engineer | No traffic after 10min |
| T+30min | Go/No-Go | Confirm cutover successful or trigger rollback | Migration Lead | Any rollback trigger hit |
| T+60min | Notify stakeholders | Send cutover complete notification | Programme Manager | — |

### 3.4 Rollback Procedure

| Trigger | Action | Maximum Window |
|---------|--------|---------------|
| Application fails to start on AWS | Revert DNS to source, restart source services | 4 hours post-cutover |
| Data integrity failure detected | Revert DNS, restore source from pre-cutover backup | 2 hours post-cutover |
| Performance degradation > 50% | Revert DNS, investigate root cause | 4 hours post-cutover |
| Critical integration failure | Revert DNS, restore source connectivity | 4 hours post-cutover |
| After rollback window expires | Forward-fix only (no rollback) | — |

**Rollback Steps:**
1. Revert DNS records to on-premises endpoints (TTL should be set low pre-cutover: 60s)
2. Restart source application services
3. Verify source application healthy
4. Stop DMS replication (prevent data conflicts)
5. Notify stakeholders of rollback
6. Conduct root cause analysis
7. Schedule re-attempt with fixes

---

## 4. Wave 1 — Low-Risk Applications (Weeks 7–14)

### 4.1 Scope

| Application | R-Type | Current Stack | Target Architecture |
|-------------|--------|--------------|-------------------|
| Medical Supply Chain (APP-HC-012) | Refactor | Java 8 J2EE, JBoss 6.4, MySQL 8.0 | Java 17 / Spring Boot → ECS Fargate, MySQL → Aurora MySQL |
| Patient Discharge (APP-HC-019) | Retire | ASP.NET 4.8, SQL Server 2019 | Decommission — functionality absorbed into EHR (Wave 4) |
| Telemedicine Platform (APP-HC-014) | Replatform | React/Node.js, PostgreSQL 15 (DEV) | Containerise → ECS Fargate, PostgreSQL → Aurora PostgreSQL |
| Research Data Repository (APP-HC-017) | Replatform | Python, PostgreSQL/MongoDB (DEV) | Containerise → ECS Fargate, PostgreSQL → Aurora, MongoDB → DocumentDB, MinIO → S3 |

### 4.2 Wave 1 Execution Plan

| Week | Activity | Applications | Owner |
|------|----------|-------------|-------|
| Week 7 | Provision target infrastructure (IaC) | All Wave 1 | Cloud Architect |
| Week 7–8 | Code modernisation (Java 8 → 17) | Medical Supply Chain | App Dev Team |
| Week 8 | Configure DMS for MySQL, PostgreSQL, MongoDB | All Wave 1 | DBA |
| Week 8–9 | Containerise applications, build CI/CD pipelines | Telemedicine, Research Data Repo | DevOps |
| Week 9–10 | Data replication running, integration testing | All Wave 1 | Migration Lead |
| Week 11 | Test cutover rehearsal | All Wave 1 | Migration Lead |
| Week 12 | **Cutover execution** | Telemedicine, Research Data Repo | Migration Lead |
| Week 13 | **Cutover execution** | Medical Supply Chain | Migration Lead |
| Week 13 | **Decommission** | Patient Discharge (retire) | App Owner |
| Week 14 | Hypercare, lessons learned | All Wave 1 | Migration Lead |

### 4.3 Wave 1 Success Criteria

| Metric | Target |
|--------|--------|
| Applications migrated | 3 migrated + 1 retired |
| Data integrity | Zero data loss |
| Downtime | < 2 hours per application |
| Performance | Within 10% of baseline |
| Rollback events | 0 |
| Team confidence to proceed | Confirmed |

### 4.4 Wave 1 — Patient Discharge Retirement Process

| Step | Action | Owner |
|------|--------|-------|
| 1 | Identify all data in Patient Discharge system | App Owner + DBA |
| 2 | Archive data to S3 (encrypted, lifecycle policy) | DBA |
| 3 | Validate data accessible from archive | App Owner |
| 4 | Redirect users to alternative workflow (manual/EHR) | Business Owner |
| 5 | Decommission application and infrastructure | Infrastructure Team |
| 6 | Terminate licenses | Procurement |
| 7 | Update CMDB and documentation | Migration Lead |

---

## 5. Wave 2 — Tier-2 Clinical Systems (Weeks 15–26)

### 5.1 Scope

| Application | R-Type | Current Stack | Target Architecture |
|-------------|--------|--------------|-------------------|
| Pharmacy Management (APP-HC-004) | Rehost | Java 11, Oracle 19c, Tomcat 9, IBM MQ (McKesson) | EC2 (lift & shift), RDS Oracle, Amazon MQ |
| Medical Imaging & PACS (APP-HC-009) | Rehost | C++/Python, MongoDB 6.0 (Agfa) | EC2 (lift & shift), DocumentDB, S3 for DICOM |
| Radiology Info System (APP-HC-005) | Replatform | C# 6.0/.NET 4.6, SQL Server 2019 (Sectra) | .NET 8 → ECS Fargate, RDS SQL Server |
| Laboratory Info System (APP-HC-006) | Refactor | Java 8, WebLogic 12c, SQL Server 2017, IBM MQ (Cerner) | Java 17 / Spring Boot → ECS, RDS SQL Server, Amazon MQ |
| Patient Scheduling (APP-HC-008) | Replatform | Python/Django, PostgreSQL 15, Redis 7.0 | ECS Fargate, Aurora PostgreSQL, ElastiCache Redis |
| Nurse Workforce Mgmt (APP-HC-016) | Replatform | .NET 7, SQL Server 2022 (TEST) | ECS Fargate, RDS SQL Server |

### 5.2 Wave 2 Key Considerations

**Shared Infrastructure Resolution:**
- INFRA-HC-003 (hlth-mssql-prod-01) hosts both RIS and LIS — migrate together to avoid split-brain
- INFRA-HC-002 (Oracle RAC) hosts Pharmacy Mgmt — but also EHR/Revenue Cycle (Wave 4). Migrate Pharmacy to separate RDS Oracle instance first

**Vendor Coordination:**
| Vendor | Application | Action Required | Timeline |
|--------|-------------|----------------|----------|
| McKesson | Pharmacy Management | Validate support for AWS hosting, obtain updated license | 4 weeks before cutover |
| Sectra | Radiology Information System | Confirm .NET 8 compatibility, test on AWS | 6 weeks before cutover |
| Agfa HealthCare | Medical Imaging & PACS | Validate EC2 hosting support, DICOM storage on S3 | 4 weeks before cutover |
| Cerner | Laboratory Information System | Confirm support for modernised stack | 6 weeks before cutover |

**Data Migration — Medical Imaging (500TB+):**

| Phase | Data Volume | Method | Duration |
|-------|-------------|--------|----------|
| Historical archive (>2 years) | ~350 TB | DataSync → S3 Glacier Deep Archive | 4–5 weeks (parallel) |
| Recent archive (6mo–2yr) | ~100 TB | DataSync → S3 Standard-IA | 2 weeks |
| Active data (<6 months) | ~50 TB | DataSync → S3 Standard + DocumentDB | 1 week |
| Final sync (cutover) | Delta only | DataSync incremental | Hours |

### 5.3 Wave 2 Execution Plan

| Week | Activity | Applications | Owner |
|------|----------|-------------|-------|
| Week 15–16 | Provision target infrastructure, begin DICOM data transfer | All Wave 2 | Cloud Architect + DBA |
| Week 16–18 | Code modernisation (RIS .NET upgrade, LIS Java 8→17) | RIS, LIS | App Dev Teams |
| Week 17–19 | DMS replication setup for Oracle, SQL Server, PostgreSQL | All Wave 2 | DBA |
| Week 19–20 | Containerise Patient Scheduling, Nurse Workforce | Patient Scheduling, Nurse Workforce | DevOps |
| Week 20–22 | Integration testing (HL7, DICOM, IBM MQ → Amazon MQ) | All Wave 2 | QA + Migration Lead |
| Week 22–23 | Test cutover rehearsal | All Wave 2 | Migration Lead |
| Week 23–24 | **Cutover: Nurse Workforce, Patient Scheduling** | Low-risk first | Migration Lead |
| Week 24–25 | **Cutover: RIS + LIS** (together — shared MSSQL) | Co-migration group | Migration Lead |
| Week 25–26 | **Cutover: Pharmacy Mgmt, Medical Imaging** | Vendor apps | Migration Lead |
| Week 26+ | Hypercare (2 weeks) | All Wave 2 | Migration Lead |

### 5.4 Wave 2 Success Criteria

| Metric | Target |
|--------|--------|
| Applications migrated | 6 |
| DICOM imaging accessible | 100% of studies retrievable |
| HL7/FHIR integrations functional | All message flows validated |
| Vendor support confirmed | All 4 vendors acknowledge AWS hosting |
| Downtime per application | < 4 hours |
| Data integrity | Zero data loss |

---

## 6. Wave 3 — Core Platform (Weeks 27–40)

### 6.1 Scope

| Application | R-Type | Current Stack | Target Architecture |
|-------------|--------|--------------|-------------------|
| Patient Portal (APP-HC-002) | Replatform | React 18/Node.js 18, PostgreSQL 15, Redis 7.0 | ECS Fargate, Aurora PostgreSQL, ElastiCache, CloudFront |
| Health Info Exchange (APP-HC-011) | Replatform | Java 17/Spring Boot, PostgreSQL 15, Kafka 3.2, MuleSoft | ECS Fargate, Aurora PostgreSQL, MSK, API Gateway |
| Clinical Decision Support (APP-HC-010) | Replatform | Python/FastAPI, PostgreSQL 15, MongoDB 6.0, Kafka, Redis | ECS Fargate, Aurora, DocumentDB, MSK, ElastiCache |
| Compliance & Audit (APP-HC-018) | Replatform | Java 17/Angular, PostgreSQL 15 | ECS Fargate, Aurora PostgreSQL, S3 (audit archives) |
| Medical Device Hub (APP-HC-020) | Replatform | Java 17/Python, Cassandra 4.1, InfluxDB 2.7, Kafka | ECS/EKS, Amazon Keyspaces, Timestream, MSK |

### 6.2 Wave 3 Key Considerations

**EHR Dependency Management:**
- Patient Portal, HIE, Clinical Decision Support, and Medical Device Hub all integrate with EHR (still on-premises in Wave 3)
- **Strategy:** Maintain hybrid connectivity via Transit Gateway. Applications on AWS call EHR via on-premises endpoints until Wave 4 completes
- **Risk:** Latency increase for cross-network calls. Mitigate with caching and async patterns where possible

**Kafka Migration to MSK:**
- 4 applications in Wave 3 depend on Apache Kafka 3.2
- Migrate to Amazon MSK (Managed Streaming for Kafka) as shared service
- Deploy MSK cluster in Data VPC, accessible from Production VPC via Transit Gateway
- Run dual-write during transition: on-prem Kafka + MSK in parallel, then cut consumers over

**Real-Time Requirements:**
| Application | Latency Requirement | Mitigation |
|-------------|-------------------|-----------|
| Medical Device Hub | < 100ms (IoT telemetry) | Deploy in same AZ as consumers, use Timestream for time-series |
| Clinical Decision Support | < 500ms (clinical alerts) | ElastiCache for hot data, async processing for non-critical |
| Patient Portal | < 2s (user-facing) | CloudFront CDN, Aurora read replicas |

### 6.3 Wave 3 Execution Plan

| Week | Activity | Applications | Owner |
|------|----------|-------------|-------|
| Week 27–28 | Deploy MSK cluster, provision Aurora/DocumentDB/Keyspaces | All Wave 3 | Cloud Architect |
| Week 28–30 | Containerise all 5 applications, build ECS task definitions | All Wave 3 | DevOps |
| Week 29–31 | DMS replication for PostgreSQL, MongoDB, Cassandra | All Wave 3 | DBA |
| Week 30–32 | InfluxDB → Timestream migration (custom ETL) | Medical Device Hub | Data Engineer |
| Week 31–33 | Integration testing (HL7 FHIR, MQTT, hybrid EHR connectivity) | All Wave 3 | QA + Migration Lead |
| Week 33–34 | Kafka dual-write setup (on-prem + MSK) | HIE, Clinical Decision, Device Hub | DevOps |
| Week 34–35 | Test cutover rehearsal | All Wave 3 | Migration Lead |
| Week 35–36 | **Cutover: Compliance & Audit** (lowest dependency) | Compliance & Audit | Migration Lead |
| Week 36–37 | **Cutover: Patient Portal + HIE** (co-dependent) | Patient Portal, HIE | Migration Lead |
| Week 38–39 | **Cutover: Clinical Decision Support + Medical Device Hub** | Clinical Decision, Device Hub | Migration Lead |
| Week 39–40 | Hypercare, decommission on-prem Kafka consumers | All Wave 3 | Migration Lead |

### 6.4 Wave 3 Success Criteria

| Metric | Target |
|--------|--------|
| Applications migrated | 5 |
| MSK operational | All consumers reading from MSK |
| Hybrid EHR connectivity | < 50ms additional latency |
| Medical device telemetry | < 100ms end-to-end |
| HIPAA compliance validated | Security Hub findings = 0 critical |
| Downtime per application | < 4 hours |

---

## 7. Wave 4 — Mission Critical (Weeks 41–56)

### 7.1 Scope

| Application | R-Type | Current Stack | Target Architecture |
|-------------|--------|--------------|-------------------|
| Electronic Health Records (APP-HC-001) | Replatform | Java 17/Angular, Oracle 19c RAC, JBoss EAP 7.4, Kafka | ECS/EKS, RDS Oracle Multi-AZ → Aurora PostgreSQL (future), MSK |
| Revenue Cycle Management (APP-HC-007) | Replatform | Java 17/Spring Boot, Oracle 19c, PostgreSQL 15, Kafka, Redis | ECS Fargate, Aurora PostgreSQL, MSK, ElastiCache |
| Claims Processing (APP-HC-015) | Refactor | COBOL/Java 11, Oracle 19c, IBM MQ, WebLogic 12c | Java 17/Spring Boot → ECS, Aurora PostgreSQL, Amazon MQ, Step Functions |
| Clinical Data Warehouse (APP-HC-003) | Refactor | Python/Scala, PostgreSQL 15, MongoDB 6.0, Spark 3.4, NiFi, Hadoop | EMR/Glue, Aurora, DocumentDB, S3 Data Lake, Redshift, MWAA |
| EHR Analytics Platform (APP-HC-013) | Refactor | Python/Scala/R, MongoDB 6.0, Cassandra 4.1, Spark, Airflow, Hadoop | EMR/Glue, Keyspaces, S3 Data Lake, MWAA, SageMaker |

### 7.2 Wave 4 Key Considerations

**EHR Migration — Highest Risk:**
- Central hub system — 12+ applications depend on it
- By Wave 4, all consumers already on AWS (Waves 1–3 complete)
- Oracle 19c RAC → RDS Oracle Multi-AZ initially (minimise change)
- Future state: migrate to Aurora PostgreSQL (separate modernisation initiative post-migration)

**Claims Processing — COBOL Modernisation:**

| Approach | Description | Timeline | Risk |
|----------|-------------|----------|------|
| Automated refactoring | Use COBOL-to-Java transpilation tooling | 8–12 weeks | Medium — generated code quality |
| Manual rewrite | Rewrite business logic in Java 17/Spring Boot | 12–16 weeks | Low — clean code, but slower |
| **Recommended: Hybrid** | Transpile core logic, manually rewrite interfaces and integration layer | 10–14 weeks | Balanced |

**Big Data Platform Migration:**

| Component | Source | Target | Method |
|-----------|--------|--------|--------|
| HDFS (8TB+) | Hadoop 3.3 | S3 (Data Lake) | DistCp to S3 via DataSync |
| Spark jobs | Spark 3.4 (on-prem) | EMR Serverless / Glue | Refactor Spark scripts for EMR |
| Airflow DAGs | Airflow 2.7 (self-managed) | MWAA (Managed Airflow) | Migrate DAGs, update connections |
| NiFi flows | NiFi 1.21 | Glue / Step Functions / MWAA | Redesign data pipelines |
| ML models | Custom Python/R | SageMaker | Repackage models for SageMaker endpoints |

### 7.3 Wave 4 Execution Plan

| Week | Activity | Applications | Owner |
|------|----------|-------------|-------|
| Week 41–43 | COBOL analysis and transpilation (Claims Processing) | Claims Processing | App Dev + Specialist |
| Week 41–44 | Big data platform build (EMR, Glue, MWAA, Redshift, S3 Data Lake) | CDW, EHR Analytics | Data Engineer |
| Week 42–44 | Provision RDS Oracle Multi-AZ, Aurora PostgreSQL clusters | EHR, Revenue Cycle | DBA |
| Week 43–46 | HDFS → S3 data migration, Spark job refactoring | CDW, EHR Analytics | Data Engineer |
| Week 44–46 | DMS replication for Oracle RAC → RDS Oracle | EHR, Revenue Cycle, Claims | DBA |
| Week 45–47 | Containerise EHR, Revenue Cycle; build Claims Processing microservices | EHR, Revenue Cycle, Claims | DevOps + App Dev |
| Week 47–49 | Integration testing (all 20 apps end-to-end on AWS) | All | QA + Migration Lead |
| Week 49–50 | Test cutover rehearsal (full dress rehearsal) | All Wave 4 | Migration Lead |
| Week 50–51 | **Cutover: Clinical Data Warehouse + EHR Analytics** | CDW, EHR Analytics | Migration Lead |
| Week 52–53 | **Cutover: Revenue Cycle + Claims Processing** | Revenue Cycle, Claims | Migration Lead |
| Week 54–55 | **Cutover: EHR** (final — all dependencies now on AWS) | EHR | Migration Lead |
| Week 55–56 | Hypercare (extended: 3 weeks for EHR) | All Wave 4 | Migration Lead |

### 7.4 EHR Cutover — Detailed Plan

Given EHR is the most critical system, a detailed cutover plan:

| Time | Step | Action | Rollback Trigger |
|------|------|--------|-----------------|
| T-7 days | Rehearsal | Full dress rehearsal with production-like data | — |
| T-48hr | Communication | Notify all clinical staff of planned maintenance window | — |
| T-24hr | Final backup | Full Oracle RAC backup + verify restore | Backup failure |
| T-4hr | Reduce traffic | Enable maintenance page for non-critical functions | — |
| T-2hr | Final DMS sync | Trigger final CDC sync, verify lag = 0 | Lag > 5 minutes |
| T-1hr | Source freeze | Stop all writes to on-prem EHR | — |
| T-30min | Data validation | Row counts, checksum on critical tables (patients, encounters, orders) | Mismatch > 0 |
| T+0 | DNS cutover | Update DNS to AWS ALB endpoint | — |
| T+5min | Service start | Start EHR containers on ECS/EKS | Containers fail health check |
| T+10min | Smoke test | Login, patient lookup, order entry, HL7 message flow | Any critical function fails |
| T+20min | Integration test | Verify all 12 dependent apps communicate with EHR | Integration failure |
| T+30min | Clinical validation | Clinical staff verify patient data, workflows | Clinical staff report issues |
| T+60min | Go/No-Go | Final decision — proceed or rollback | Any rollback trigger |
| T+2hr | Full traffic | Remove maintenance page, full clinical operations | — |
| T+24hr | Checkpoint | 24-hour stability review | — |

**EHR Rollback Window:** 4 hours (after which forward-fix only due to data divergence)

### 7.5 Wave 4 Success Criteria

| Metric | Target |
|--------|--------|
| Applications migrated | 5 (all mission-critical) |
| EHR availability post-cutover | 99.95% (first 30 days) |
| Claims processing accuracy | 100% (financial data — zero tolerance) |
| Data lake operational | All Spark jobs running on EMR/Glue |
| Oracle RAC decommissioned | Within 30 days post-cutover |
| Total programme downtime | < 24 hours cumulative across all waves |

---

## 8. Post-Migration Optimisation

### 8.1 Immediate Optimisation (Weeks 1–4 Post-Migration)

| Activity | Target | Expected Savings |
|----------|--------|-----------------|
| Right-sizing instances | Analyse CloudWatch metrics, downsize over-provisioned | 20–30% compute cost reduction |
| Storage tiering | Move cold data to S3-IA/Glacier, EBS gp3 optimisation | 40–50% storage cost reduction |
| Reserved Instances / Savings Plans | Commit to 1-year Compute Savings Plan for steady-state | 30–40% vs. on-demand |
| Unused resource cleanup | Delete orphaned EBS volumes, unused EIPs, idle load balancers | Variable |
| Database optimisation | Aurora Serverless for variable workloads, read replicas | 20–30% database cost reduction |

### 8.2 Right-Sizing Process

| Step | Action | Tool |
|------|--------|------|
| 1 | Collect 2 weeks of CloudWatch metrics (CPU, memory, network) | CloudWatch |
| 2 | Identify instances with avg CPU < 20% or memory < 30% | AWS Compute Optimizer |
| 3 | Recommend smaller instance type | Compute Optimizer |
| 4 | Test with new instance type in non-production | Manual |
| 5 | Apply change in production during maintenance window | IaC update |
| 6 | Monitor for 1 week post-change | CloudWatch alarms |

### 8.3 Cost Allocation and Tagging

| Tag Key | Purpose | Example Values |
|---------|---------|---------------|
| Environment | Cost split by environment | production, staging, development |
| Application | Cost per application | ehr, patient-portal, claims-processing |
| Wave | Track migration wave costs | wave-1, wave-2, wave-3, wave-4 |
| CostCenter | Business unit chargeback | clinical-services, finance, radiology |
| MAPTracking | MAP milestone tracking | map-eligible, map-non-eligible |

---

## 9. Modernization Roadmap

### 9.1 Post-Migration Modernization Priorities

After all 20 applications are migrated, pursue modernization in priority order:

| Priority | Initiative | Applications | Target State | Timeline |
|----------|-----------|-------------|-------------|----------|
| 1 | Oracle → Aurora PostgreSQL | EHR (post-stabilisation) | Eliminate Oracle licensing | Months 3–9 post-migration |
| 2 | Serverless adoption | Patient Scheduling, Compliance & Audit | Lambda + API Gateway | Months 2–6 post-migration |
| 3 | Container orchestration upgrade | All ECS apps | ECS → EKS (where beneficial) | Months 4–8 post-migration |
| 4 | ML/AI integration | Clinical Decision Support, EHR Analytics | SageMaker endpoints | Months 6–12 post-migration |
| 5 | Event-driven architecture | Revenue Cycle, Claims Processing | EventBridge + Step Functions | Months 6–12 post-migration |

### 9.2 Modernization Pattern — Oracle to Aurora PostgreSQL (EHR)

| Phase | Activity | Duration | Risk |
|-------|----------|----------|------|
| Assessment | Schema analysis, PL/SQL inventory, compatibility check | 4 weeks | Low |
| Schema conversion | AWS SCT (Schema Conversion Tool) | 4 weeks | Medium |
| Application changes | Update queries, stored procedures, ORM mappings | 8 weeks | High |
| Data migration | DMS full load + CDC from RDS Oracle → Aurora PostgreSQL | 2 weeks | Medium |
| Testing | Full regression, performance, integration | 4 weeks | Medium |
| Cutover | Switch application to Aurora PostgreSQL | 1 day | Medium |
| Decommission | Terminate RDS Oracle instance | Post-stabilisation | Low |

**Expected benefit:** Eliminate Oracle licensing costs (significant annual savings)

### 9.3 Modernization Pattern — Serverless Adoption

For suitable applications (stateless, event-driven, variable load):

| Component | Current | Target | Benefit |
|-----------|---------|--------|---------|
| Compute | ECS Fargate (always-on) | Lambda (event-driven) | Pay-per-invocation, zero idle cost |
| API | ALB + ECS | API Gateway + Lambda | Managed scaling, built-in throttling |
| Orchestration | Application code | Step Functions | Visual workflows, error handling |
| Scheduling | Celery/Redis | EventBridge Scheduler | Managed, no infrastructure |

### 9.4 Well-Architected Framework Reviews

Schedule Well-Architected reviews at key milestones:

| Review | Timing | Focus |
|--------|--------|-------|
| Post-Wave 2 | Week 28 | Operational Excellence, Security |
| Post-Wave 4 | Week 58 | All 6 pillars — full review |
| Quarterly (ongoing) | Every 13 weeks | Rotating focus pillar |

---

## 10. Decommissioning

### 10.1 Source Infrastructure Decommission Plan

| Step | Action | Timeline | Owner |
|------|--------|----------|-------|
| 1 | Confirm all applications operational on AWS (30-day stability) | +30 days post-cutover | Migration Lead |
| 2 | Verify no traffic to source systems (network monitoring) | +30 days | Network Engineer |
| 3 | Take final archive backup of source systems | +30 days | DBA |
| 4 | Store archive in S3 Glacier Deep Archive (7-year retention for HIPAA) | +30 days | DBA |
| 5 | Power down source servers (soft decommission) | +45 days | Infrastructure Team |
| 6 | Wait period (30 days powered off, available for emergency) | +45–75 days | Infrastructure Team |
| 7 | Terminate VMware licenses | +75 days | Procurement |
| 8 | Physical hardware disposal (secure wipe) | +90 days | Facilities |
| 9 | Update CMDB, close change records | +90 days | Migration Lead |
| 10 | Data centre contract termination (if applicable) | Per contract terms | Procurement |

### 10.2 License Termination

| License | Current Cost (Annual) | Termination Date | Action |
|---------|----------------------|-----------------|--------|
| VMware vSphere Enterprise | Significant | +75 days post-final wave | Cancel renewal |
| Oracle Database Enterprise | Significant | After Aurora PostgreSQL migration | Cancel or reduce |
| IBM MQ | Moderate | After Amazon MQ validated | Cancel |
| WebLogic | Moderate | After LIS/Claims refactored | Cancel |
| Windows Server (datacentre) | Moderate | After all Windows workloads migrated | Cancel |
| NetApp ONTAP | Moderate | After SAN data migrated to EBS/S3 | Cancel |

---

## 11. Communication Plan

### 11.1 Stakeholder Communication Matrix

| Audience | Content | Channel | Frequency | Owner |
|----------|---------|---------|-----------|-------|
| Executive Steering | Programme status, risks, decisions | Presentation | Bi-weekly | Programme Manager |
| Clinical Leadership | Clinical system impact, downtime windows | Email + Meeting | Weekly during waves | Engagement Manager |
| IT Operations | Technical status, cutover schedules | Slack/Teams + Stand-up | Daily during cutover | Migration Lead |
| End Users (Clinical Staff) | Maintenance windows, what's changing | Email + Intranet | Per cutover event | Communications Lead |
| Vendors (McKesson, Agfa, etc.) | Migration schedule, support requirements | Email + Call | Monthly + pre-cutover | Engagement Manager |
| AWS PDM | MAP milestone progress, spend tracking | Partner Central + Call | Monthly | Partner Development |

### 11.2 Cutover Communication Template

**Pre-Cutover (T-7 days):**
> Subject: Planned Maintenance — [Application Name] Migration to AWS
> 
> [Application Name] will be migrated to AWS on [Date]. Expected maintenance window: [Start Time] to [End Time] ([Duration]).
> 
> Impact: [Description of user impact]
> Action required: [Any user actions needed]
> Support: Contact [helpdesk] for issues during/after migration

**Post-Cutover (T+1 hour):**
> Subject: Migration Complete — [Application Name] Now Running on AWS
> 
> [Application Name] has been successfully migrated. All services are operational.
> 
> If you experience any issues, contact [helpdesk] immediately. Enhanced support is available for the next 2 weeks.

---

## 12. Governance and Reporting

### 12.1 Migration Metrics Dashboard

| Metric | Target | Tracking |
|--------|--------|----------|
| Applications migrated (cumulative) | 20 total | Weekly |
| Migration velocity | 2–3 apps/month (accelerating) | Monthly |
| Planned vs. actual downtime | < 100% of planned window | Per cutover |
| Rollback events | 0 | Per cutover |
| Critical incidents post-migration | 0 | Weekly |
| AWS spend vs. budget | Within 10% | Weekly |
| MAP milestone progress | $50K by Month 4 | Monthly |
| Team certifications achieved | 27 total | Monthly |

### 12.2 Escalation Matrix

| Severity | Definition | Response Time | Escalation Path |
|----------|-----------|---------------|----------------|
| P1 — Critical | Production down, patient safety risk | 15 minutes | Migration Lead → CCoE Lead → Executive Sponsor |
| P2 — High | Degraded performance, workaround available | 1 hour | Migration Lead → CCoE Lead |
| P3 — Medium | Non-critical issue, no patient impact | 4 hours | Migration Lead |
| P4 — Low | Cosmetic, documentation, minor | Next business day | Assigned engineer |

---

## 13. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| EHR cutover failure | Low | Critical | Full dress rehearsal, 4-hour rollback window, extended hypercare |
| COBOL modernisation delays | Medium | High | Start early (Week 41), have manual rewrite as fallback |
| 800TB data transfer overrun | Medium | Medium | Start in Wave 2, run continuously in background |
| Oracle RAC migration complexity | Medium | High | Rehost first (RDS Oracle), modernise to Aurora later |
| Clinical workflow disruption | Low | Critical | Clinical staff UAT before every cutover, hypercare team on-site |
| Vendor non-support on AWS | Low | High | Written confirmation before cutover, fallback to on-prem if needed |
| MAP credit expiry | Low | Medium | Track monthly, accelerate spend if at risk |
| Team fatigue (14-month programme) | Medium | Medium | Rotate team members, celebrate wave completions |
| Regulatory audit during migration | Low | High | Maintain dual-environment compliance, audit trail in both |

---

## 14. Programme Closure

### 14.1 Completion Criteria

| Criterion | Evidence |
|-----------|----------|
| All 20 applications operational on AWS | Monitoring dashboards, zero on-prem traffic |
| On-premises infrastructure decommissioned | CMDB updated, licenses terminated |
| MAP milestone reported | AWS Partner Central confirmation |
| Knowledge transfer complete | Customer team operating independently |
| Documentation complete | Runbooks, architecture diagrams, operational procedures |
| Cost baseline established | 3 months of AWS cost data, optimisation complete |
| Lessons learned documented | Programme retrospective report |

### 14.2 Handover to Steady-State Operations

| Item | From (Partner) | To (Customer) | Handover Activity |
|------|---------------|---------------|-------------------|
| Infrastructure management | Partner DevOps | Customer Cloud Ops | 2-week shadowing |
| Security operations | Partner Security | Customer SecOps | Runbook walkthrough + drill |
| Database administration | Partner DBA | Customer DBA | Aurora/RDS operations training |
| Cost management | Partner FinOps | Customer Finance | Cost Explorer + Budgets training |
| Incident management | Partner L2/L3 | Customer L2 + AWS Support | Escalation path handover |
| Architecture decisions | Partner Architect | Customer CCoE | Architecture Decision Records |

### 14.3 Ongoing Support Options

| Model | Scope | Duration |
|-------|-------|----------|
| Managed Services | Full operational management | 12+ months |
| Advisory Retainer | Architecture reviews, optimisation guidance | Quarterly |
| Break-Fix Support | On-demand issue resolution | As needed |
| Modernization Sprints | Specific modernisation initiatives (Oracle→Aurora, serverless) | Per initiative |

---

## 15. Timeline Summary

```
Weeks 7–14:   Wave 1 — Low-risk apps (4 apps: 3 migrated + 1 retired)
Weeks 15–26:  Wave 2 — Tier-2 clinical systems (6 apps, vendor coordination)
Weeks 27–40:  Wave 3 — Core platform (5 apps, MSK deployment, hybrid EHR)
Weeks 41–56:  Wave 4 — Mission critical (5 apps, EHR, COBOL modernisation)
Weeks 56–60:  Post-migration optimisation, right-sizing, Savings Plans
Weeks 60–64:  Decommissioning, licence termination, programme closure
Weeks 64+:    Modernization roadmap execution (Oracle→Aurora, serverless)
```

---

## 16. Deliverables Checklist

| # | Deliverable | Format | Owner |
|---|-------------|--------|-------|
| 1 | Wave Execution Reports (per wave) | Document | Migration Lead |
| 2 | Cutover Runbooks (per wave) | Step-by-step document | Migration Lead |
| 3 | Post-Migration Validation Reports | Test results | QA Lead |
| 4 | Lessons Learned (per wave) | Document | Programme Manager |
| 5 | Cost Optimisation Report | Spreadsheet + Cost Explorer | FinOps |
| 6 | MAP Milestone Evidence | Screenshots + report | Partner Development |
| 7 | Decommissioning Report | Checklist + evidence | Infrastructure Team |
| 8 | Architecture Documentation (as-built) | Diagrams + docs | Cloud Architect |
| 9 | Operational Runbooks (steady-state) | Document | DevOps |
| 10 | Modernization Roadmap | Prioritised backlog | Cloud Architect |
| 11 | Programme Closure Report | Executive summary | Programme Manager |
| 12 | Knowledge Transfer Evidence | Training records, shadowing logs | Engagement Manager |

---

*End of Phase 3: Migrate & Modernize Runbook*
