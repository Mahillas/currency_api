# MortgageAI - Product Requirements Document

## 1. Executive Summary

**Product Name:** MortgageAI (working title)

**Type:** B2B SaaS - Mortgage Document Automation Platform

**Core Value Proposition:** AI-powered document verification and organization platform that automates income, down payment, and fraud detection for mortgage professionals - reducing document processing time from hours to minutes.

**Target Market:** 
- Mortgage brokers (primary)
- Mortgage lenders
- Credit unions
- Property developers

**Target Geography:** Initially Canada, then US, UK, Australia

---

## 2. Problem Statement

Mortgage professionals spend 3-5 hours per file on document verification tasks:
- Manual document sorting and naming
- Income calculation from multiple sources (pay stubs, bank statements, T4s, tax returns)
- Down payment source verification (gift letters, large deposits)
- Cross-document validation for fraud detection
- Compiling submission packages for lenders

**Pain Points:**
1. Repetitive manual work that doesn't scale
2. Human error in calculations and document matching
3. Risk of missing fraud indicators
4. Inconsistent document organization
5. Time-consuming lender submission preparation

---

## 3. Product Vision

Build an AI-powered platform that:
1. **Automates document processing** - classify, name, summarize any mortgage document
2. **Verifies income automatically** - handle self-employed, employed, retirement, multiple income sources
3. **Validates down payment** - reconcile gift letters, track large deposits
4. **Detects fraud** - cross-document validation, anomaly detection
5. **Generates lender-ready reports** - compile submission packages instantly

---

## 4. Feature Specifications

### 4.1 Document Collection Portal

**Description:** Secure portal for borrowers to upload documents

**Features:**
- Customizable document checklist templates (purchase, refinance, renewal)
- Branded portal with broker logo
- Real-time upload feedback (missing pages, wrong format)
- Secure link generation with expiration
- Multi-file upload support (PDF, images, documents)

**User Flow:**
1. Broker creates document request from template
2. Borrower receives secure link via email/SMS
3. Borrower uploads documents with real-time validation
4. Documents auto-organize and generate confirmation report

**Technical Requirements:**
- Secure file storage (encrypted at rest)
- Virus/malware scanning
- File type validation
- Size limits (50MB per file)
- Progress indicator for uploads

---

### 4.2 Document Organization & Classification

**Description:** AI-powered document classification and naming

**Features:**
- Automatic document type detection (pay stub, bank statement, T4, tax return, employment letter, etc.)
- Smart file naming based on content
- Date extraction and sorting
- Multi-page document handling
- Support for: PDF, PNG, JPG, HEIC, DOCX

**Classification Categories:**
- Identity: Government ID, utility bill
- Income: Pay stubs, T4s, NOA, bank statements, employment letter
- Assets: Investment statements, property documents
- Liabilities: Loan statements, credit card statements
- Property: Purchase agreement, MLS listing, appraisal

---

### 4.3 Income Verification Engine

**Description:** Automated income calculation for all employment types

**Employment Types Supported:**
- Salaried (full-time, part-time)
- Self-employed (sole proprietor, corporation)
- Contract workers
- Commission-based
- Retirement/pension
- Government benefits (CPP, OAS, EI)
- Rental income
- Investment income

**Features:**
- YTD annualization from pay stubs
- 2-year average calculation
- Expense ratio analysis for self-employed
- Business income from 12+ month bank statements
- Multiple income source consolidation
- Income trend analysis

**Output:**
- Usable income calculation
- Income verification report
- Supporting documentation summary

---

### 4.4 Down Payment Verification

**Description:** Verify source of down payment funds

**Features:**
- Large deposit tracking (configurable threshold, default $5,000)
- Gift letter validation against bank deposits
- Proceeds of sale calculation from property sales
- Source documentation requirements
- Compliance flags for unverified funds
- One-click submission notes generation

**Checks:**
- Deposit matches gift letter amount
- 90-day lookback for large deposits
- Sourceless funds flagging
- Property sale proceeds verification
- Tournament/loan proceeds validation

---

### 4.5 Fraud Detection

**Description:** Automated cross-document validation

**Features:**
- Pay stub vs bank statement income reconciliation
- Document modification detection
- Inconsistent information flags
- Duplicate document detection
- Address consistency across documents
- Employment date validation

**Alerts:**
- Annualized income doesn't match pay stub
- Bank balance doesn't match stated income
- Modified document detected
- Unsourced large deposits
- NSF/overdraft patterns
- Notable withdrawals requiring explanation

---

### 4.6 Multiple Borrowers

**Description:** Handle complex applications with multiple borrowers

**Features:**
- Co-borrower support (up to 6 borrowers per application)
- Individual document tracking per borrower
- Combined income calculations
- Combined liability assessment
- Joint/several liability handling

---

### 4.7 Lender Reports & Export

**Description:** Generate submission-ready packages

**Output Formats:**
- PDF reports (income verification, down payment verification)
- Organized document PDF package
- XML/JSON for API integration
- Lender-specific formats (Calyx, Ellie Mae)

**Report Contents:**
- Executive summary
- Income breakdown by borrower
- Down payment source table
- Document inventory list
- Compliance checklist
- Notes and disclaimers

---

## 5. Technical Architecture

### 5.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  React/Next.js Web App + Mobile Responsive                   │
│  (Document portal, Dashboard, Reports)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                     API Gateway                              │
│  Authentication, Rate Limiting, Logging                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Application Services                      │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐     │
│  │ Document     │ │ Verification │ │ Report           │     │
│  │ Service      │ │ Engine       │ │ Generator        │     │
│  └──────────────┘ └──────────────┘ └──────────────────┘     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    ML/AI Services                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐     │
│  │ Document     │ │ Income       │ │ Fraud            │     │
│  │ Classifier   │ │ Analyzer     │ │ Detector         │     │
│  │ (OCR + ML)   │ │              │ │                  │     │
│  └──────────────┘ └──────────────┘ └──────────────────┘     │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      Data Layer                              │
│  PostgreSQL (metadata), S3 (files), Redis (cache)            │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Tech Stack

**Frontend:**
- Next.js 14 (React)
- TypeScript
- Tailwind CSS
- Shadcn UI components

**Backend:**
- Node.js/Express or Python/FastAPI
- PostgreSQL (metadata, user data)
- Redis (sessions, caching)

**ML/AI:**
- Python for ML services
- Tesseract/Google Vision (OCR)
- Custom ML models for document classification
- LangChain for document analysis

**Infrastructure:**
- AWS (EC2, Lambda, S3, RDS, ElastiCache)
- Docker/Kubernetes
- Stripe for payments

### 5.3 Data Flow

1. **Upload Flow:**
   ```
   Document Upload → Virus Scan → S3 Storage → 
   OCR Processing → ML Classification → Database Entry
   ```

2. **Verification Flow:**
   ```
   Trigger Analysis → Fetch Documents → ML Processing → 
   Rules Engine → Generate Results → Store in DB
   ```

3. **Report Flow:**
   ```
   Request Report → Aggregate Data → Template Render → 
   PDF Generation → Email/S3 → User Download
   ```

---

## 6. User Roles & Permissions

| Role | Permissions |
|------|-------------|
| Super Admin | Full system access, tenant management |
| Brokerage Admin | User management, branding, settings |
| Broker | Create applications, upload docs, run reports |
| Viewer | Read-only access to assigned applications |
| Borrower | Upload documents to assigned application |

---

## 7. Security Requirements

- **Encryption:** AES-256 at rest, TLS 1.3 in transit
- **SOC 2 Type II** compliance target
- **PIPEDA/PHIPA** compliant (Canada)
- **GDPR** compliant (expansion markets)
- **Multi-factor authentication**
- **Role-based access control**
- **Audit logging**
- **Data retention policies**

---

## 8. Pricing Model

**Tiered per-application model:**

| Plan | Price | Applications/mo |
|------|-------|------------------|
| Free | $0 | 0 (setup only) |
| Starter | $49/mo | 5 |
| Professional | $99/mo | 25 |
| Enterprise | Custom | Unlimited |

**Application Definition:**
- Counts when documents submitted
- Up to 6 borrowers per application
- Unlimited documents per application
- Unlimited report runs

---

## 9. Success Metrics

**Key KPIs:**
- 90% reduction in document processing time
- < 5 minutes income verification (vs 3-5 hours manual)
- < 3 minutes down payment verification
- 99.5% classification accuracy
- < 1% false positive fraud alerts

**Customer Success:**
- NPS > 50
- < 2% monthly churn
- > 95% feature adoption

---

## 10. Competitive Differentiation

| Feature | Competitors | MortgageAI |
|---------|-------------|------------|
| Self-employed income from bank statements | Limited | Full automation |
| Real-time borrower portal | Basic | Advanced with validation |
| Multi-borrower support | Basic | Full consolidation |
| Lender API integration | Custom only | Standard + custom |
| Pricing | $99+/mo fixed | Per-application, more flexible |

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| OCR accuracy on poor quality docs | High | Multiple OCR providers, manual fallback |
| ML model training data availability | Medium | Partner with brokers for sample data |
| Regulatory changes | Medium | Modular rules engine, easy updates |
| Data privacy concerns | High | SOC 2, encryption, transparent policies |
| Competition from large players | Medium | Focus on SMB market, speed of innovation |