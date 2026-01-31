# AuthDoc  
**Verification-First Document Intelligence Platform**

AuthDoc is a backend system for **automated academic document verification** built with a verification-first mindset.

Unlike traditional OCR systems that assume extracted data is correct, AuthDoc treats OCR output as **untrusted input** and applies **deterministic, rule-based verification** to decide trust, consistency, and explainability.

This repository contains a **production-aligned prototype** suitable for demos, evaluations, and system-design reviews.

---

## 🔑 Core Principle

> **OCR is probabilistic.  
> Verification is deterministic.  
> Trust belongs to verification — not extraction.**

---

## 🧱 High-Level Architecture
Frontend
│
▼
Node.js (Express)
├─ Verification Engine
├─ Policy Rules
├─ API Layer
│
▼
Python (FastAPI)
├─ OCR (Tesseract)
└─ Field Extraction

### Responsibility Split

| Layer | Responsibility |
|------|----------------|
| Frontend | Upload documents, display results |
| Node.js Backend | Verification logic, policies, APIs |
| Python OCR Service | OCR + regex-based extraction only |

The frontend **never performs verification logic**.

---

## 📂 Repository Structure
AuthDoc/
├── backend/
│ ├── node/ # Express backend (verification engine)
│ └── python/ # FastAPI OCR service
├── frontend/ # (optional / external)
├── .gitignore
└── README.md

---

## 🚀 Local Setup (Clean Install)

### Prerequisites

- Node.js ≥ 18
- Python 3.10
- Tesseract OCR installed  
  - Windows: set `tesseract.exe` path explicitly in Python
  - Linux/macOS: install via system package manager

---

## 1️⃣ Python OCR Service

```bash
cd backend/python
python -m venv venv
```
# Linux / macOS
```bash
source venv/bin/activate
```
# Install Dependencies
```bask
pip install -r requirements.txt
```
#  Start OCR Service
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```
# Service URL
```bash
http://127.0.0.1:8000
```
### 2️⃣ Node.js Backend
```bash
cd backend/node
npm install
npm run dev
```
## Backend URL
```bash
http://localhost:3000
```
### 🔌 API Endpoints
## 📤 Upload & Ingest Document
```bash
POST /api/ingest
```

# Request

Content-Type: multipart/form-data

Field: file (PDF / JPG / PNG)

# Response
```bash
{
  "document_id": "uuid"
}
```
## 🔍 Verify Single Document
```bash
POST /api/verify
```

# Request
```
{
  "document_id": "uuid",
  "policy_id": "strict"
}
```

# Response
```
{
  "document_id": "uuid",
  "results": {
    "gpa": {
      "value": 8.691,
      "status": "VERIFIED",
      "reason": "Within allowed range"
    },
    "cgpa": {
      "value": 8.601,
      "status": "VERIFIED",
      "reason": "Difference acceptable"
    },
    "result_status": {
      "value": null,
      "status": "VERIFIED",
      "reason": "Dependency satisfied"
    }
  }
}
```
## Field Guarantees

Each verified field always contains:

value → extracted value or null

status → VERIFIED | FLAGGED | MISSING

reason → human-readable explanation

📦 Batch Verification
```bash
POST /api/verify/batch
```

Request
```
{
  "policy_id": "strict",
  "document_ids": ["uuid1", "uuid2"]
}

```
Response
```
{
  "candidates": [
    {
      "document_id": "uuid1",
      "overall_status": "VERIFIED",
      "fields": {
        "gpa": "VERIFIED",
        "cgpa": "FLAGGED",
        "result_status": "VERIFIED"
      }
    }
  ]
}
```

Batch responses are summary-only by design for scalability.

### 🧾 Verification Policies

Verification rules are config-driven, not hardcoded.

Policy File
backend/node/src/config/policies.json
```
/**
Example Policy
{
  "strict": {
    "required_fields": ["gpa", "cgpa", "result_status"],
    "rules": [
      { "type": "range", "field": "gpa", "min": 0, "max": 10 },
      { "type": "delta", "field": "cgpa", "compare_with": "gpa", "max_diff": 1.0 },
      { "type": "dependency", "field": "result_status", "depends_on": "subject_grades" }
    ]
  }
}
```
Rule Engine Behavior

range → numeric validation

delta → cross-field consistency

dependency → logical dependency checks

All rules are interpreted by a generic verification engine, not custom code.

### 🛡️ Design Notes

OCR output is treated as untrusted

Verification is deterministic and explainable

Missing data is never guessed

FLAGGED ≠ invalid (manual review required)




