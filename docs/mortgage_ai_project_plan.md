# MortgageAI - Project Plan

## Phase 1: Foundation (Weeks 1-8)

### Week 1-2: Infrastructure Setup
- [ ] Set up AWS account and core services
- [ ] Configure VPC, subnets, security groups
- [ ] Set up PostgreSQL database (RDS)
- [ ] Configure S3 bucket with encryption
- [ ] Set up Redis (ElastiCache)
- [ ] Configure CI/CD pipeline (GitHub Actions)

**Deliverables:** Dev environment ready, CI/CD pipeline

### Week 3-4: Authentication & Core API
- [ ] Implement user authentication (JWT + refresh tokens)
- [ ] Set up role-based access control (RBAC)
- [ ] Create tenant/multi-org structure
- [ ] Build core API endpoints (CRUD for applications)
- [ ] Set up API documentation (OpenAPI/Swagger)

**Deliverables:** Auth system, API scaffolding, API docs

### Week 5-6: Document Upload & Storage
- [ ] Implement file upload endpoint with chunking
- [ ] Set up virus scanning (ClamAV or cloud service)
- [ ] Configure S3 storage with lifecycle policies
- [ ] Implement file type validation
- [ ] Create document metadata database schema

**Deliverables:** Secure document upload, virus scanning

### Week 7-8: Basic Document Classification
- [ ] Integrate OCR service (Google Vision or AWS Textract)
- [ ] Build document type classifier (rule-based + ML)
- [ ] Implement automatic file naming
- [ ] Create document organization logic

**Deliverables:** Auto-classification of common doc types

---

## Phase 2: Core Features (Weeks 9-16)

### Week 9-10: Income Verification Engine
- [ ] Build income parser for pay stubs
- [ ] Implement YTD annualization algorithm
- [ ] Create employment type detection
- [ ] Build 2-year average calculator

**Deliverables:** Basic income verification for employed borrowers

### Week 11-12: Self-Employed Income
- [ ] Build bank statement analyzer
- [ ] Implement business expense categorization
- [ ] Create revenue/expense trend analysis
- [ ] Implement cash-flow based income calculation

**Deliverables:** Self-employed income verification

### Week 13-14: Down Payment Verification
- [ ] Build large deposit tracker
- [ ] Implement gift letter reconciliation
- [ ] Create proceeds of sale calculator
- [ ] Build compliance flagging system

**Deliverables:** Down payment source verification

### Week 15-16: Fraud Detection
- [ ] Implement cross-document validation
- [ ] Build document modification detector
- [ ] Create anomaly detection rules
- [ ] Implement address/employment consistency check

**Deliverables:** Basic fraud detection alerts

---

## Phase 3: User Experience (Weeks 17-22)

### Week 17-18: Dashboard & Application Management
- [ ] Build broker dashboard with application list
- [ ] Create application detail view
- [ ] Implement document viewer
- [ ] Build verification results display

**Deliverables:** Full application management UI

### Week 19-20: Report Generation
- [ ] Build PDF report generator
- [ ] Create income verification report template
- [ ] Create down payment verification report
- [ ] Implement document package export

**Deliverables:** Lender-ready report generation

### Week 21-22: Borrower Portal
- [ ] Build borrower document upload portal
- [ ] Create customizable checklist templates
- [ ] Implement real-time upload validation
- [ ] Build branded portal (logo customization)

**Deliverables:** Complete borrower portal

---

## Phase 4: Advanced Features (Weeks 23-28)

### Week 23-24: Multi-Borrower Support
- [ ] Implement co-borrower functionality
- [ ] Build combined income calculation
- [ ] Create combined liability assessment
- [ ] Build per-borrower document tracking

**Deliverables:** Multi-borrower applications

### Week 25-26: Integrations
- [ ] Build lender API integrations (Calypso, Ellie Mae)
- [ ] Create webhook system for notifications
- [ ] Implement POS integration hooks
- [ ] Build Zapier/Make integrations

**Deliverables:** Third-party integrations

### Week 27-28: Enterprise Features
- [ ] Build multi-team management
- [ ] Implement advanced analytics dashboard
- [ ] Create custom branding options
- [ ] Build audit logging system

**Deliverables:** Enterprise-ready platform

---

## Phase 5: Launch & Scale (Weeks 29-36)

### Week 29-32: Testing & QA
- [ ] Comprehensive integration testing
- [ ] Security penetration testing
- [ ] Performance/load testing
- [ ] User acceptance testing with beta users

**Deliverables:** QA report, bug fixes, performance tuning

### Week 33-34: Beta Launch
- [ ] Onboard 10-20 beta customers
- [ ] Collect feedback and iterate
- [ ] Fix critical issues
- [ ] Document user guides

**Deliverables:** Beta customers live, feedback loop

### Week 35-36: Public Launch
- [ ] Marketing website launch
- [ ] Pricing page and payment integration
- [ ] Customer support setup
- [ ] Monitoring and alerting

**Deliverables:** Public launch

---

## Technical Architecture Details

### Database Schema (PostgreSQL)

```sql
-- Tenants/Brokerages
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    branding_logo_url TEXT,
    settings JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(50), -- admin, broker, viewer, borrower
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Applications
CREATE TABLE applications (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    status VARCHAR(50), -- draft, pending_upload, in_review, submitted, funded
    borrowers JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Documents
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    application_id UUID REFERENCES applications(id),
    borrower_id UUID,
    document_type VARCHAR(100),
    file_name VARCHAR(255),
    s3_key VARCHAR(500),
    ocr_text TEXT,
    metadata JSONB,
    classification_confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Verification Results
CREATE TABLE verification_results (
    id UUID PRIMARY KEY,
    application_id UUID REFERENCES applications(id),
    verification_type VARCHAR(50), -- income, down_payment, fraud
    results JSONB,
    warnings JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints

```
POST   /api/auth/login
POST   /api/auth/refresh
GET    /api/applications
POST   /api/applications
GET    /api/applications/:id
POST   /api/applications/:id/documents
GET    /api/applications/:id/documents
POST   /api/applications/:id/verify/income
POST   /api/applications/:id/verify/down-payment
POST   /api/applications/:id/verify/fraud
GET    /api/applications/:id/reports/:type
POST   /api/applications/:id/share
GET    /api/brokerage/settings
PUT    /api/brokerage/settings
```

### File Storage Structure (S3)

```
s3://mortgageai-bucket/
├── {organization_id}/
│   ├── applications/
│   │   └── {application_id}/
│   │       └── {borrower_id}/
│   │           ├── income/
│   │           │   └── {document_id}.pdf
│   │           ├── down_payment/
│   │           │   └── {document_id}.pdf
│   │           └── other/
│   └── reports/
│       └── {application_id}/
│           └── income_verification_{timestamp}.pdf
```

### ML Pipeline

```python
# Document Classification Pipeline
1. Upload → S3
2. Trigger Lambda
3. OCR (Google Vision API)
4. Extract text → Feature extraction
5. Classification model (trained on labeled data)
6. Store classification + confidence in DB

# Income Verification Pipeline
1. Get documents by application
2. Parse pay stubs → extract gross pay, YTD
3. Parse bank statements → calculate deposits
4. Match employment type
5. Apply rules (annualization, averaging)
6. Calculate usable income
7. Store results in DB

# Fraud Detection Pipeline
1. Get all documents for application
2. Compare income across documents
3. Check document modification dates
4. Validate address consistency
5. Flag anomalies → Store in warnings
```

---

## Resource Requirements

### Team Structure
- 1 Product Manager
- 1 Tech Lead / Architect
- 2 Backend Engineers
- 1 Frontend Engineer
- 1 ML Engineer
- 1 DevOps Engineer
- 1 QA Engineer

### Budget Estimate (MVP to Launch)

| Category | Cost Range |
|----------|------------|
| AWS Infrastructure (Dev + Prod) | $5,000-10,000/mo |
| Third-party APIs (OCR, ML) | $2,000-5,000/mo |
| Development Tools | $500/mo |
| Marketing (Launch) | $10,000-20,000 |
| **Total Year 1** | **$100,000-180,000** |

---

## Milestone Summary

| Milestone | Target | Key Deliverables |
|-----------|--------|------------------|
| M1: Dev Environment | Week 2 | Infrastructure, CI/CD |
| M2: Core API | Week 4 | Auth, CRUD, Docs |
| M3: Document Upload | Week 8 | Upload, OCR, Classification |
| M4: Income Verification | Week 12 | Pay stub + bank statement parsing |
| M5: Down Payment | Week 16 | Gift letter, deposit tracking |
| M6: Dashboard | Week 20 | Full UI for brokers |
| M7: Borrower Portal | Week 22 | Document collection |
| M8: Beta Launch | Week 34 | 10-20 customers |
| M9: Public Launch | Week 36 | General availability |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OCR accuracy issues | High | High | Multiple OCR providers, manual review fallback |
| ML model training data | Medium | Medium | Partner with brokers, synthetic data |
| Regulatory compliance | Medium | High | Legal review, modular rules engine |
| AWS cost overruns | Medium | Medium | Cost monitoring, auto-scaling |
| Timeline delays | High | Medium | Buffer weeks, prioritize MVP features |