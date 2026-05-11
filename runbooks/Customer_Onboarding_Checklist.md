What# Customer Onboarding Checklist — Production Agentic System

## Pre-Engagement Data Collection

### Mandatory Inputs (System Will Not Run Without These)

- [ ] **Application Portfolio Inventory (CSV)**
  - [ ] App name and unique ID
  - [ ] Technology stack with specific versions (e.g., "Java 8" not "Java")
  - [ ] Criticality rating (Critical / High / Medium / Low)
  - [ ] Environment (Production / Dev / Test / Staging)
  - [ ] Business unit / owner team
  - [ ] Database dependencies
  - [ ] Integration dependencies (app-to-app)
  - [ ] Middleware dependencies

- [ ] **Infrastructure Inventory (CSV)**
  - [ ] Server name / ID
  - [ ] CPU cores, Memory (MB), Storage (GB)
  - [ ] Operating system and version
  - [ ] Virtual or physical (hypervisor type)
  - [ ] Workload type (DB / Web / App / Big Data / Storage)
  - [ ] Environment (Production / Dev / Test)
  - [ ] Hosted applications (server-to-app mapping)

- [ ] **Migration Scope & Drivers (Text Document)**
  - [ ] Why migrating (business drivers)
  - [ ] Timeline constraints
  - [ ] Budget envelope (if known)
  - [ ] Compliance/regulatory requirements
  - [ ] Out-of-scope systems

---

### Recommended Inputs (Significantly Improves Output Quality)

- [ ] **Dependency Map**
  - [ ] App-to-app integration list (source → target, protocol)
  - [ ] Shared infrastructure mapping (which apps share servers/DBs)
  - [ ] External integrations (third-party, SaaS, vendor systems)

- [ ] **Current Cost Data**
  - [ ] Annual infrastructure costs (hardware, hosting, power)
  - [ ] Software licensing costs (Oracle, VMware, Microsoft, etc.)
  - [ ] Support/maintenance contracts
  - [ ] Staff costs allocated to infrastructure operations

- [ ] **Compliance Requirements**
  - [ ] Regulatory frameworks applicable (HIPAA, PCI-DSS, SOX, GDPR, etc.)
  - [ ] Data classification per application (PHI, PII, financial, public)
  - [ ] Data residency/sovereignty constraints
  - [ ] Audit requirements

- [ ] **MRA Questionnaire Responses**
  - [ ] Business & Strategy (score 1–5 + notes)
  - [ ] People & Process (score 1–5 + notes)
  - [ ] Platform & Architecture (score 1–5 + notes)
  - [ ] Security & Compliance (score 1–5 + notes)
  - [ ] Operations & Management (score 1–5 + notes)
  - [ ] Migration Experience (score 1–5 + notes)

- [ ] **Organisational Structure**
  - [ ] IT team roster (roles, headcount, current skills)
  - [ ] Reporting structure
  - [ ] Decision-makers and approvers

- [ ] **Network Topology**
  - [ ] Current network diagram (VLANs, firewalls, WAN links)
  - [ ] Internet connectivity (bandwidth, provider)
  - [ ] Existing cloud connectivity (VPN, Direct Connect)

- [ ] **Vendor / License Inventory**
  - [ ] Third-party software with vendor name and support status
  - [ ] License types (perpetual, subscription, BYOL-eligible)
  - [ ] Contract renewal dates
  - [ ] Vendor cloud-hosting policies

---

## Infrastructure Setup

### AWS Environment

- [ ] AWS account with Amazon Bedrock access enabled
- [ ] Model access granted (Claude Sonnet 4 or Amazon Nova Pro)
- [ ] IAM role/user with `bedrock:InvokeModel` permission
- [ ] AWS region selected (confirm model availability)
- [ ] AWS credentials configured (CLI or environment variables)

### Agent Runtime

- [ ] Python 3.11+ installed
- [ ] `strands-agents` package installed
- [ ] Presentation agent code deployed
- [ ] Output directory created with write permissions

---

## Data Quality Validation (Run Before First Agent Execution)

- [ ] All applications have criticality assigned (no blanks)
- [ ] Tech stack includes version numbers (not just language names)
- [ ] Every production app has at least one dependency listed (or explicitly "None")
- [ ] Server-to-app mapping is complete (no orphaned servers)
- [ ] Environment field is consistent (standardised values)
- [ ] No duplicate app IDs or server IDs
- [ ] CSV encoding is UTF-8 (no corrupted characters)
- [ ] Column headers match expected template

---

## Runtime Inputs (During Migration Execution)

- [ ] AWS Cost Explorer access (for live spend tracking)
- [ ] Migration Hub enabled (for progress tracking)
- [ ] Wave execution status updates (per cutover)
- [ ] Certification/training completion records
- [ ] Incident/issue log (for lessons learned)

---

## Partner Readiness

- [ ] Prompt library reviewed and customised for partner methodology
- [ ] Output templates validated against partner branding/style
- [ ] Sample run completed with customer data (dry run)
- [ ] Customer stakeholders briefed on AI-generated output process
- [ ] Review/approval workflow defined (who signs off AI outputs before customer delivery)

---

## Sign-Off

| Item | Confirmed By | Date |
|------|-------------|------|
| All mandatory inputs received | Partner Delivery Lead | ________ |
| Data quality validation passed | Technical Architect | ________ |
| AWS environment operational | Cloud Engineer | ________ |
| Dry run successful | Partner Delivery Lead | ________ |
| Customer briefed on process | Engagement Manager | ________ |

---

*Once all mandatory items are checked, the system is ready to generate customer deliverables.*

---

## Appendix: Recommended Tools for Data Collection

### Application Portfolio Discovery

| Tool | What It Collects | Best For |
|------|-----------------|----------|
| AWS Application Discovery Service | Servers, processes, network connections, dependencies | Agentless or agent-based discovery of on-prem environments |
| AWS Migration Hub | Centralises discovery data from multiple sources | Single pane of glass for all migration data |
| AWS Migration Evaluator | Server utilisation, licensing, cost modelling | Business case and right-sizing recommendations |
| RVTools | VMware inventory (VMs, hosts, datastores, snapshots) | Quick VMware estate export — free tool |
| ServiceNow CMDB | App catalogue, relationships, owners, SLAs | Customers already using ServiceNow |
| LeanIX | Application portfolio management, tech stack, lifecycle | Enterprise architecture teams |
| Flexera | License inventory, software usage, compliance | License optimisation (Oracle, Microsoft) |

### Infrastructure & Network Discovery

| Tool | What It Collects | Best For |
|------|-----------------|----------|
| RVTools | VM inventory, CPU/RAM/storage, OS, snapshots | VMware environments (exports to CSV directly) |
| AWS Application Discovery Agent | CPU, memory, disk I/O, network connections, processes | Deep utilisation data + dependency mapping |
| Nmap / Angry IP Scanner | Open ports, services, network topology | Quick network scan when no CMDB exists |
| SolarWinds / PRTG | Network topology, bandwidth, device inventory | Customers with existing monitoring |
| ManageEngine | Asset inventory, software, hardware, network | Mid-market IT environments |

### Dependency Mapping

| Tool | What It Collects | Best For |
|------|-----------------|----------|
| AWS Application Discovery Service (agent mode) | TCP connections between servers, process-level dependencies | Automated dependency discovery |
| Dynatrace | Full-stack dependencies, service maps, call flows | Customers with APM already deployed |
| AppDynamics | Application topology, transaction flows | Java/.NET application environments |
| Cloudamize | Server dependencies, application grouping, migration complexity | Migration-specific dependency analysis |

### Cost & Licensing Data

| Tool | What It Collects | Best For |
|------|-----------------|----------|
| AWS Migration Evaluator | Current infrastructure costs, projected AWS costs | TCO/ROI business case |
| AWS Pricing Calculator | Projected AWS service costs | Target-state cost modelling |
| Flexera / Snow Software | License entitlements, usage, compliance gaps | Oracle, Microsoft, SAP licensing |
| Vendor contracts (manual) | Renewal dates, terms, termination clauses | Decommission planning |

### Compliance & Security

| Tool | What It Collects | Best For |
|------|-----------------|----------|
| Qualys / Nessus / Rapid7 | Vulnerability scan, OS patch status, EOL detection | Security posture baseline |
| OneTrust / TrustArc | Data classification, privacy impact assessments | GDPR, HIPAA data mapping |
| Manual questionnaire | Regulatory requirements per application | When no tooling exists |

### Organisational Readiness (MRA)

| Tool | What It Collects | Best For |
|------|-----------------|----------|
| AWS MAP MRA Tool (Partner Central) | 6-dimension readiness scoring | Official MAP programme requirement |
| Structured interviews | Stakeholder perspectives, skills, processes | Qualitative assessment |
| Skills assessment survey | Current AWS knowledge per team member | Training plan input |

---

## Appendix: Recommended Approach by Customer Maturity

| Customer Profile | Recommended Approach | Timeline |
|-----------------|---------------------|----------|
| **Mature** (CMDB, APM, ITSM in place) | Export from ServiceNow + Dynatrace + RVTools | 1–2 weeks |
| **Moderate** (some tooling, partial CMDB) | RVTools + AWS Discovery Agent + manual interviews | 2–4 weeks |
| **Low maturity** (no tooling, spreadsheets) | AWS Discovery Service (agentless) + RVTools + structured questionnaires | 4–6 weeks |

### Fastest Path (Minimum Tooling)

For a customer starting from zero, these three free/low-cost tools provide the mandatory inputs:

1. **RVTools** → Infrastructure CSV (5 minutes to export from vCenter)
2. **AWS Application Discovery Service (agentless)** → Dependency map (1–2 weeks of data collection)
3. **Structured spreadsheet template** → Application portfolio (partner provides template, customer fills in with app owners over 1–2 weeks)
