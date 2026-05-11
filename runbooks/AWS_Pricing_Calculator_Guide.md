Combin# AWS Pricing Calculator — Configuration Guide

## AnyCompany Healthcare Migration (Steady-State)

**Calculator URL:** https://calculator.aws/#/createCalculator
**Region:** US East (N. Virginia) — us-east-1
**Projected Annual Spend:** $420K–$480K

---

## Service Configuration

### Compute — Amazon ECS (Fargate)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Tasks | 40 | ~2 tasks per app × 20 apps |
| vCPU per task | 2 | Average across apps |
| Memory per task | 4 GB | Average across apps |
| Hours/month | 730 (24/7) | Production workloads |
| Ephemeral storage | 20 GB per task | Default |

**Estimated: ~$4,800/month**

### Compute — Amazon EC2 (Rehosted Apps)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Instance type | m6i.2xlarge | Pharmacy Mgmt, Medical Imaging |
| Quantity | 4 | 2 rehosted apps × 2 AZs |
| Pricing model | 1-Year Compute Savings Plan | 30% discount |
| Hours/month | 730 | |

**Estimated: ~$1,800/month**

### Database — Amazon Aurora PostgreSQL

| Parameter | Value | Notes |
|-----------|-------|-------|
| Instance type | db.r6g.xlarge | Primary instances |
| Quantity | 6 | Patient Portal, HIE, Scheduling, Revenue Cycle, Compliance, Research |
| Multi-AZ | Yes | Production HA |
| Storage | 2 TB total | |
| I/O rate | 20M I/Os/month | |

**Estimated: ~$5,500/month**

### Database — Amazon RDS Oracle

| Parameter | Value | Notes |
|-----------|-------|-------|
| Instance type | db.r6i.2xlarge | EHR (primary) |
| Quantity | 2 | Multi-AZ |
| License | Bring Your Own (BYOL) | Existing Oracle licence |
| Storage | 4 TB | |

**Estimated: ~$3,200/month**

### Database — Amazon RDS SQL Server

| Parameter | Value | Notes |
|-----------|-------|-------|
| Instance type | db.r6i.xlarge | RIS, LIS, Nurse Workforce |
| Quantity | 3 | |
| Multi-AZ | Yes | |
| License | License Included | |
| Storage | 1 TB | |

**Estimated: ~$2,800/month**

### Database — Amazon DocumentDB

| Parameter | Value | Notes |
|-----------|-------|-------|
| Instance type | db.r6g.large | Medical Imaging, Clinical Decision Support |
| Quantity | 3 | Replica set |
| Storage | 500 GB | |

**Estimated: ~$1,200/month**

### Streaming — Amazon MSK

| Parameter | Value | Notes |
|-----------|-------|-------|
| Broker instance | kafka.m5.large | |
| Quantity | 3 | 3-broker cluster |
| Storage per broker | 1 TB | |

**Estimated: ~$1,500/month**

### Storage — Amazon S3

| Parameter | Value | Notes |
|-----------|-------|-------|
| S3 Standard | 50 TB | Active clinical data |
| S3 Standard-IA | 100 TB | Recent archives (6mo–2yr) |
| S3 Glacier Deep Archive | 350 TB | Historical imaging (>2yr) |
| Requests | 10M GET, 1M PUT/month | |

**Estimated: ~$4,200/month**

### Storage — Amazon EFS

| Parameter | Value | Notes |
|-----------|-------|-------|
| Storage | 5 TB | Shared file systems |
| Throughput mode | Bursting | |

**Estimated: ~$1,500/month**

### Caching — Amazon ElastiCache (Redis)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Node type | cache.r6g.large | |
| Quantity | 4 | Patient Portal, Scheduling, HIE, Device Hub |

**Estimated: ~$1,100/month**

### Analytics — Amazon EMR

| Parameter | Value | Notes |
|-----------|-------|-------|
| Primary instance | m5.2xlarge | |
| Core instances | m5.4xlarge × 4 | Spark/data processing |
| Hours/month | 400 | Batch jobs, not 24/7 |

**Estimated: ~$2,500/month**

### Analytics — Amazon Redshift

| Parameter | Value | Notes |
|-----------|-------|-------|
| Node type | ra3.xlplus | |
| Quantity | 2 | Clinical Data Warehouse |

**Estimated: ~$1,800/month**

### Networking

| Parameter | Value | Notes |
|-----------|-------|-------|
| Direct Connect | 1 Gbps dedicated | Hybrid connectivity |
| NAT Gateway | 3 (one per VPC) | |
| Data transfer out | 2 TB/month | |
| Transit Gateway | 1 | Hub for all VPCs |

**Estimated: ~$1,800/month**

### Security & Monitoring

| Parameter | Value | Notes |
|-----------|-------|-------|
| CloudTrail | Organisation trail | |
| GuardDuty | 8 accounts | |
| Config | 8 accounts, 50 rules | |
| Security Hub | 8 accounts | |
| CloudWatch | 200 metrics, 50 alarms, 100GB logs | |
| KMS | 20 CMKs, 10M requests | |

**Estimated: ~$1,300/month**

### Other Services

| Service | Configuration | Monthly |
|---------|--------------|---------|
| Amazon Timestream | 10GB writes, 100GB storage | ~$300 |
| Amazon Keyspaces | 50M reads, 10M writes | ~$400 |
| AWS Backup | 10TB protected | ~$500 |
| Amazon MWAA (Airflow) | mw1.medium, 5 workers | ~$800 |
| Application Load Balancers | 5 ALBs | ~$400 |

**Estimated: ~$2,400/month**

---

## Cost Summary

| Category | Monthly | Annual |
|----------|---------|--------|
| Compute (ECS + EC2) | $6,600 | $79,200 |
| Databases (Aurora + RDS + DocumentDB) | $12,700 | $152,400 |
| Streaming (MSK) | $1,500 | $18,000 |
| Storage (S3 + EFS) | $5,700 | $68,400 |
| Caching (ElastiCache) | $1,100 | $13,200 |
| Analytics (EMR + Redshift) | $4,300 | $51,600 |
| Networking | $1,800 | $21,600 |
| Security & Monitoring | $1,300 | $15,600 |
| Other | $2,400 | $28,800 |
| **Total** | **$37,400** | **$448,800** |

---

## Savings Plan Recommendations

| Plan Type | Commitment | Discount | Annual Saving |
|-----------|-----------|----------|---------------|
| Compute Savings Plan (1-year) | $5,000/month | 30% | ~$25,000 |
| Aurora Reserved Instances (1-year) | 6 instances | 35% | ~$23,000 |
| RDS Reserved Instances (1-year) | 5 instances | 35% | ~$25,000 |
| ElastiCache Reserved (1-year) | 4 nodes | 30% | ~$4,000 |
| **Total Savings Plan Discount** | | | **~$77,000/year** |

**Post-Savings Plan Annual Cost: ~$372,000**

---

## How to Use This Guide

1. Open https://calculator.aws/#/createCalculator
2. Add each service above with the specified parameters
3. Click **"Share"** to generate a shareable URL
4. Click **"Export"** to download CSV/PDF
5. Attach to ROI report and MAP funding application

---

> **Note:** Pricing is directional based on current published rates. Generate a fresh estimate before customer presentation. For formal pricing commitments, engage your AWS account team.
