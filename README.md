# LexShield AI - Enterprise Legal Risk Analysis Platform

A production-grade, AI-powered legal document analysis platform for enterprises, law firms, and financial institutions.

## 🎯 Overview

LexShield AI is a full-stack SaaS application that leverages AI to analyze legal documents, identify risky clauses, and provide simple language explanations with multilingual support and voice assistance.

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Landing │ Auth │ Dashboard │ Upload │ Analysis │Admin │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
                   (REST API / JWT)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend (FastAPI - Python)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Auth Service │ Document Service │ Analysis Engine   │  │
│  │ Voice Service │ Storage Service  │ Admin Service     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           ↓
        ┌──────────────────┬──────────────────┐
        ↓                  ↓                  ↓
   PostgreSQL        AWS S3/Cloud      OpenAI/Llama
   (Data)            (File Storage)     (AI Analysis)
```

## 🏗️ Tech Stack

### Frontend
- **Next.js 14** - Framework with App Router
- **React 18** - UI components
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **ShadCN UI** - Component library
- **Framer Motion** - Advanced animations
- **Zustand** - State management
- **TanStack React Query** - Data fetching
- **Zod** - Schema validation

### Backend
- **FastAPI** - Web framework
- **Python 3.11+** - Language
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **PyJWT** - Authentication
- **Python-multipart** - File handling
- **LangChain** - AI orchestration
- **Tesseract OCR** - Document scanning
- **python-dotenv** - Configuration

### Database
- **PostgreSQL 15+** - Relational database
- **Alembic** - Migration management

### Infrastructure
- **Docker** - Containerization
- **AWS S3** - File storage (optional)
- **OpenAI API** - AI analysis

## 📦 Project Structure

```
lexshield-ai/
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   ├── (dashboard)/
│   │   ├── api/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── dashboard/
│   │   ├── auth/
│   │   ├── upload/
│   │   └── shared/
│   ├── lib/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── validation.ts
│   ├── types/
│   ├── styles/
│   ├── hooks/
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── documents.py
│   │   │   │   ├── analysis.py
│   │   │   │   └── admin.py
│   │   │   └── dependencies.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── constants.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── document_service.py
│   │   │   ├── analysis_service.py
│   │   │   └── storage_service.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── document.py
│   │   │   └── analysis.py
│   │   ├── schemas/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── main.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── docker-compose.yml
└── docs/
    ├── API.md
    ├── DEPLOYMENT.md
    ├── ARCHITECTURE.md
    └── SECURITY.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
# API at http://localhost:8000
```

### Docker Setup (Recommended for Production)

```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: localhost:5432
```

## 🔐 Security Features

✅ **AES-256 Encryption** - Sensitive data at rest  
✅ **HTTPS/TLS** - Encrypted in transit  
✅ **JWT Authentication** - Stateless auth  
✅ **Rate Limiting** - DDoS protection  
✅ **Input Validation** - Zod/Pydantic  
✅ **SQL Injection Prevention** - Parameterized queries  
✅ **CORS Protection** - Cross-origin security  
✅ **Secure File Handling** - Sandboxed processing  
✅ **Zero-Retention Mode** - Optional data deletion  
✅ **RBAC** - Role-based access control  

## 🤖 AI Analysis Engine

The platform uses LangChain with GPT-4/Llama to:

1. **Extract** legal clauses and terms
2. **Classify** risk levels (Low/Medium/High)
3. **Detect** suspicious patterns:
   - Unlimited liability
   - Auto-renewal traps
   - Hidden fees
   - Non-compete clauses
   - Termination conditions
4. **Explain** in simple language
5. **Translate** to 7 languages
6. **Summarize** key findings

## 📊 Risk Scoring Algorithm

```
Risk Score = (Clause Risk * Weight) + (Pattern Risk * Weight) + (Financial Risk * Weight)

Risk Categories:
- Low (0-33): Safe terms, standard clauses
- Medium (34-66): Notable risks, requires review
- High (67-100): Critical risks, legal review recommended
```

## 🌐 Supported Languages

- English
- Hindi
- Bengali
- Tamil
- Marathi
- Arabic
- Spanish

## 📱 Features

### Document Management
- PDF, DOCX, TXT support
- Drag-and-drop upload
- OCR for scanned documents
- Document preview
- Upload history

### Analysis & Reporting
- Real-time risk analysis
- Color-coded risk indicators
- Clause-by-clause breakdown
- Executive summary
- PDF report export
- Highlighted dangerous terms

### Voice Interface
- Speech-to-text queries
- Voice summaries
- Natural language Q&A
- Multi-language voice support

### User Dashboard
- Document library
- Analysis history
- Risk analytics
- Saved reports
- Team management (Enterprise)
- Audit logs

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register          - User registration
POST   /api/auth/login              - User login
POST   /api/auth/refresh            - Refresh JWT token
POST   /api/auth/logout             - Logout user
```

### Documents
```
GET    /api/documents               - List user documents
POST   /api/documents               - Upload document
GET    /api/documents/{id}          - Get document details
DELETE /api/documents/{id}          - Delete document
```

### Analysis
```
POST   /api/analysis/{doc_id}       - Analyze document
GET    /api/analysis/{analysis_id}  - Get analysis results
GET    /api/analysis/report/{id}    - Export report
```

### Voice
```
POST   /api/voice/query             - Process voice query
POST   /api/voice/summary           - Generate voice summary
```

See `API.md` for complete documentation.

## 📈 Performance Metrics

- **API Response Time**: < 200ms (p95)
- **Document Processing**: < 30 seconds (typical PDF)
- **Database Query**: < 100ms (p95)
- **Frontend Load**: < 2 seconds (first contentful paint)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test
```

## 📦 Deployment

### Production Checklist
- [ ] Environment variables configured
- [ ] Database backups enabled
- [ ] SSL certificates installed
- [ ] API rate limiting enabled
- [ ] Monitoring and alerting setup
- [ ] Log aggregation configured
- [ ] Security headers enabled
- [ ] CORS properly configured

See `DEPLOYMENT.md` for detailed instructions.

## 🛡️ Compliance

- GDPR-compliant
- HIPAA-ready (with additional config)
- SOC 2 Type II architecture
- Data residency options
- Audit logging

## 📞 Support & Documentation

- **API Documentation**: `/api/docs` (Swagger UI)
- **Architecture Guide**: `docs/ARCHITECTURE.md`
- **Security Guide**: `docs/SECURITY.md`
- **Deployment Guide**: `docs/DEPLOYMENT.md`

## 📄 License

Proprietary - Enterprise License

## 🤝 Contributing

This is a production system. All changes require:
1. Code review
2. Security assessment
3. Test coverage (>80%)
4. Documentation updates

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready