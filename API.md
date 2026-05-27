# LexShield AI - API Documentation

## Base URL
```
https://api.lexshield.ai/api
```

## Authentication
All endpoints except `/auth/register`, `/auth/login`, and `/health` require authentication.

### JWT Token
Include in headers:
```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "organization": "Acme Corp"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user",
    "organization": "Acme Corp",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Logout
```http
POST /auth/logout
Authorization: Bearer <access_token>
```

### Forgot Password
```http
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### Reset Password
```http
POST /auth/reset-password
Content-Type: application/json

{
  "token": "reset_token_from_email",
  "password": "NewPassword123!"
}
```

---

## Document Endpoints

### Upload Document
```http
POST /documents
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <binary>
document_type: "contract"
tags: ["important", "2024"]
```

**Response (201 Created):**
```json
{
  "id": "doc_123",
  "name": "Service Agreement.pdf",
  "file_name": "service_agreement.pdf",
  "file_size": 245678,
  "file_type": "pdf",
  "document_type": "contract",
  "status": "processing",
  "uploaded_at": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Get Documents
```http
GET /documents?page=1&page_size=10
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "items": [
    {
      "id": "doc_123",
      "name": "Service Agreement.pdf",
      "file_name": "service_agreement.pdf",
      "file_size": 245678,
      "document_type": "contract",
      "status": "completed",
      "pages": 15,
      "uploaded_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

### Get Document Details
```http
GET /documents/{document_id}
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "doc_123",
  "name": "Service Agreement.pdf",
  "file_name": "service_agreement.pdf",
  "file_size": 245678,
  "document_type": "contract",
  "status": "completed",
  "pages": 15,
  "content": "Full text of document...",
  "metadata": {
    "extracted_date": "2024-01-15",
    "char_count": 54321
  },
  "uploaded_at": "2024-01-15T10:30:00Z",
  "processed_at": "2024-01-15T10:35:00Z"
}
```

### Delete Document
```http
DELETE /documents/{document_id}
Authorization: Bearer <access_token>
```

**Response (204 No Content)**

---

## Analysis Endpoints

### Analyze Document
```http
POST /analysis/{document_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "language": "en",
  "include_voice": false
}
```

**Response (202 Accepted):**
```json
{
  "id": "analysis_123",
  "document_id": "doc_123",
  "status": "processing",
  "message": "Analysis started"
}
```

### Get Analysis Results
```http
GET /analysis/{analysis_id}
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "analysis_123",
  "document_id": "doc_123",
  "overall_risk_score": 72.5,
  "risk_level": "high",
  "summary": "This contract contains several high-risk clauses including unlimited liability and auto-renewal terms.",
  "key_findings": [
    "Unlimited liability clause found",
    "Auto-renewal without prior notice",
    "Hidden termination fees"
  ],
  "recommendations": [
    "Negotiate unlimited liability clause",
    "Add renewal notice period",
    "Clarify fee structure"
  ],
  "language": "en",
  "risk_indicators": [
    {
      "id": "indicator_1",
      "indicator_type": "unlimited_liability",
      "risk_level": "high",
      "clause_text": "Company shall not be liable for...",
      "explanation": "This clause removes the company's liability limits",
      "confidence_score": 0.95,
      "page_number": 3
    }
  ],
  "analyzed_at": "2024-01-15T10:35:00Z"
}
```

### Get Analysis History
```http
GET /analysis/history?page=1&page_size=10
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "items": [
    { ... analysis_123 ... },
    { ... analysis_124 ... }
  ],
  "total": 28,
  "page": 1,
  "page_size": 10,
  "total_pages": 3
}
```

### Export Analysis Report
```http
GET /analysis/export/{analysis_id}?format=pdf
Authorization: Bearer <access_token>
```

**Response (200 OK):**
Binary PDF file

Supported formats: `pdf`, `docx`, `json`

---

## Voice Endpoints

### Process Voice Query
```http
POST /voice/query
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "text": "What are the main risks in this document?",
  "language": "en",
  "document_id": "doc_123"
}
```

**Response (200 OK):**
```json
{
  "response": "The main risks include...",
  "confidence": 0.92,
  "language": "en"
}
```

### Generate Voice Summary
```http
GET /voice/summary/{analysis_id}?language=en
Authorization: Bearer <access_token>
```

**Response (200 OK):**
Binary audio file (MP3)

---

## User Endpoints

### Get Profile
```http
GET /user/profile
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "organization": "Acme Corp",
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-20T14:25:00Z"
}
```

### Update Profile
```http
PUT /user/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "John Smith",
  "avatar_url": "https://...",
  "organization": "New Corp"
}
```

### Get Settings
```http
GET /user/settings
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "language": "en",
  "theme": "dark",
  "email_notifications": true,
  "two_factor_enabled": false,
  "data_retention_days": 90
}
```

### Update Settings
```http
PUT /user/settings
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "language": "hi",
  "theme": "light",
  "email_notifications": false
}
```

---

## Dashboard Endpoints

### Get Dashboard Stats
```http
GET /dashboard/stats
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "total_documents": 42,
  "analyzed_documents": 38,
  "average_risk_score": 58.3,
  "recent_analyses": [ ... ],
  "risk_distribution": {
    "low": 15,
    "medium": 16,
    "high": 7
  }
}
```

---

## Admin Endpoints

### Get Users (Admin)
```http
GET /admin/users?page=1&page_size=50
Authorization: Bearer <admin_token>
```

### Get System Stats (Admin)
```http
GET /admin/stats
Authorization: Bearer <admin_token>
```

### Get Audit Logs (Admin)
```http
GET /admin/audit-logs?action=upload&page=1
Authorization: Bearer <admin_token>
```

---

## Error Responses

### 400 Bad Request
```json
{
  "status_code": 400,
  "message": "Invalid request",
  "details": {
    "email": "Invalid email format"
  }
}
```

### 401 Unauthorized
```json
{
  "status_code": 401,
  "message": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "status_code": 403,
  "message": "Access denied"
}
```

### 404 Not Found
```json
{
  "status_code": 404,
  "message": "Document not found"
}
```

### 429 Too Many Requests
```json
{
  "status_code": 429,
  "message": "Rate limit exceeded",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "status_code": 500,
  "message": "Internal server error",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Rate Limiting

- **Standard Users**: 100 requests/hour
- **Premium Users**: 1000 requests/hour
- **Enterprise**: Unlimited

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705329000
```

---

## Pagination

All list endpoints support pagination:

Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

---

## Supported Languages

- `en` - English
- `hi` - Hindi
- `bn` - Bengali
- `ta` - Tamil
- `mr` - Marathi
- `ar` - Arabic
- `es` - Spanish

---

## Content Types

- `application/json`
- `multipart/form-data` (for file uploads)
- `application/pdf` (for exports)
- `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (for DOCX exports)

---

## Document Types

- `contract` - Business contracts
- `nda` - Non-disclosure agreements
- `policy` - Policies and procedures
- `agreement` - General agreements
- `statement` - Financial statements
- `other` - Other document types

---

## Risk Levels

- `low` - 0-33 points
- `medium` - 34-66 points
- `high` - 67-100 points

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 202 | Accepted (Async operation) |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Interactive Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

**Last Updated**: 2024
**Version**: 1.0.0