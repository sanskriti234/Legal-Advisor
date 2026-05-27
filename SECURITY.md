# LexShield AI - Security & Compliance Guide

## Table of Contents
1. [Overview](#overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Encryption](#data-encryption)
4. [Network Security](#network-security)
5. [Application Security](#application-security)
6. [Compliance](#compliance)
7. [Incident Response](#incident-response)
8. [Security Checklist](#security-checklist)

---

## Overview

LexShield AI implements enterprise-grade security measures to protect sensitive legal documents and user data.

### Security Layers
1. **Authentication**: JWT tokens, OAuth 2.0
2. **Authorization**: Role-based access control (RBAC)
3. **Encryption**: AES-256 at rest, TLS in transit
4. **Network**: CORS, CSRF protection, rate limiting
5. **Application**: Input validation, SQL injection prevention
6. **Infrastructure**: Firewalls, WAF, DDoS protection
7. **Compliance**: GDPR, CCPA, SOC 2, HIPAA-ready

---

## Authentication & Authorization

### JWT Token Security

**Token Structure:**
```
Header.Payload.Signature
```

**Claims:**
```json
{
  "sub": "user_123",
  "exp": 1705329600,
  "iat": 1705326000,
  "type": "access",
  "role": "user",
  "organization_id": "org_456"
}
```

**Implementation:**
```python
# Generate token
token = security_service.create_access_token(
    subject=user.id,
    additional_claims={
        "role": user.role,
        "organization_id": user.organization_id
    }
)

# Verify token
payload = security_service.verify_token(token)
```

### Password Security

**Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 number
- At least 1 special character (!@#$%^&*)
- Not matching email or previous passwords

**Hashing:**
```python
# Hash with bcrypt (12 rounds)
hashed_password = pwd_context.hash(password)

# Verify
is_valid = pwd_context.verify(plain_password, hashed_password)
```

### Multi-Factor Authentication (MFA)

**2FA Setup:**
```python
# Generate secret
secret = pyotp.random_base32()

# Generate QR code for TOTP app
qr_code = pyotp.totp.TOTP(secret).get_provisioning_uri(
    name=user.email,
    issuer_name='LexShield AI'
)

# Verify 2FA code
is_valid = pyotp.TOTP(secret).verify(code)
```

### Session Management

**Session Lifecycle:**
1. User logs in → Session created
2. Access token issued (30 min expiration)
3. Refresh token issued (7 day expiration)
4. Token refresh when approaching expiration
5. Session invalidated on logout

**Session Security:**
```python
# Create session
session = Session(
    user_id=user.id,
    token_jti=jti_from_token,
    ip_address=request.client.host,
    user_agent=request.headers.get("user-agent"),
    expires_at=datetime.utcnow() + timedelta(days=7)
)

# Verify session before processing request
```

### OAuth 2.0 Integration

**Supported Providers:**
- Google
- GitHub
- Microsoft Azure

**Implementation:**
```python
# Authenticate with Google
credentials = google_auth_oauthlib.flow.Flow.from_client_secrets_file(...)
token = credentials.execute_async()

# Create/link user account
user = db.query(User).filter_by(email=token['email']).first()
if not user:
    user = User(email=token['email'], oauth_provider='google')
    db.add(user)
```

---

## Data Encryption

### At-Rest Encryption

**Sensitive Fields Encrypted:**
- Passwords (hashed, not encrypted)
- API keys (hashed)
- User personally identifiable information (PII)
- Document file content (when stored)

**Implementation:**
```python
# Encrypt sensitive data
encrypted_data = security_service.encrypt_data(sensitive_data)

# Decrypt
decrypted_data = security_service.decrypt_data(encrypted_data)
```

**Database:**
```sql
-- Encrypted columns
ALTER TABLE users ADD COLUMN ssn_encrypted BYTEA;
ALTER TABLE documents ADD COLUMN content_encrypted BYTEA;

-- Encryption at database level (PostgreSQL)
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### In-Transit Encryption

**HTTPS/TLS:**
```nginx
# Nginx configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:...'
ssl_prefer_server_ciphers on;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

**Certificate:**
```bash
# Generated with Let's Encrypt
# Auto-renewal every 90 days
sudo certbot renew --quiet
```

### File Storage Encryption

**S3 Bucket:**
```python
# Server-side encryption
s3_client = boto3.client('s3')
s3_client.put_object(
    Bucket='lexshield-uploads',
    Key=file_key,
    Body=file_content,
    ServerSideEncryption='AES256'
)
```

### Key Management

**Key Rotation:**
```bash
# Rotate encryption key (handle with care)
# 1. Create new key
NEW_KEY = Fernet.generate_key()

# 2. Re-encrypt all data with new key
# 3. Update ENCRYPTION_KEY environment variable
# 4. Restart application
```

---

## Network Security

### CORS (Cross-Origin Resource Sharing)

**Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lexshield.ai", "https://app.lexshield.ai"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600
)
```

### CSRF Protection

**Token Implementation:**
```python
# Generate CSRF token
csrf_token = secrets.token_urlsafe(32)
session['csrf_token'] = csrf_token

# Verify in state-changing requests
if request.method in ['POST', 'PUT', 'DELETE']:
    token = request.headers.get('X-CSRF-Token')
    if token != session.get('csrf_token'):
        raise HTTPException(status_code=403)
```

### Security Headers

**HTTP Headers:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### Rate Limiting

**Implementation:**
```python
# Per-user rate limiting
rate_limiter = RateLimiter(requests_per_hour=1000)

if not rate_limiter.is_allowed(user_id):
    raise HTTPException(status_code=429, detail="Rate limit exceeded")
```

**Limits:**
- Unauthenticated users: 100 requests/hour
- Standard users: 1000 requests/hour
- Premium users: 10,000 requests/hour

---

## Application Security

### Input Validation

**Validate All Inputs:**
```python
# Using Pydantic
class DocumentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    document_type: DocumentType
    tags: Optional[List[str]] = Field(default=None, max_items=10)

# Using Custom Validators
@validator('name')
def validate_name(cls, v):
    if not v or len(v.strip()) == 0:
        raise ValueError('Name cannot be empty')
    return v.strip()
```

**Sanitize User Input:**
```python
# Remove XSS vectors
sanitized = InputValidator.sanitize_html(user_input)

# Validate filename
safe_filename = InputValidator.sanitize_filename(uploaded_filename)

# Validate email
is_valid = InputValidator.validate_email(email)
```

### SQL Injection Prevention

**Use Parameterized Queries:**
```python
# Bad - vulnerable to SQL injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good - parameterized
user = db.query(User).filter(User.id == user_id).first()
```

### File Upload Security

**File Type Validation:**
```python
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.png', '.jpg'}

# Validate
if not InputValidator.validate_file_type(filename, ALLOWED_EXTENSIONS):
    raise HTTPException(status_code=400, detail="File type not allowed")

# Check size
if not InputValidator.validate_file_size(file_size, max_size_mb=50):
    raise HTTPException(status_code=413, detail="File too large")
```

**Malware Detection:**
```python
# Scan with VirusTotal API
def scan_uploaded_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'https://www.virustotal.com/api/v3/files',
            headers={'x-apikey': VIRUSTOTAL_API_KEY},
            files=files
        )
    return response.json()
```

### Dependency Security

**Regular Updates:**
```bash
# Check for vulnerable dependencies
safety check

# Update dependencies
pip list --outdated
pip install --upgrade package-name

# Automated scanning
# Enable Dependabot on GitHub
```

---

## Compliance

### GDPR Compliance

**User Rights:**
1. **Right to Access**: Export user data
2. **Right to Erasure**: Delete account and data
3. **Right to Portability**: Download data in standard format
4. **Right to Rectification**: Update personal information

**Implementation:**
```python
# Right to access
def export_user_data(user_id: str):
    user_data = {
        "user": get_user(user_id),
        "documents": get_user_documents(user_id),
        "analyses": get_user_analyses(user_id)
    }
    return json.dumps(user_data)

# Right to erasure
def delete_user_account(user_id: str):
    # Delete all user data
    db.query(User).filter(User.id == user_id).delete()
    db.query(Document).filter(Document.user_id == user_id).delete()
    db.commit()
```

**Data Retention:**
```python
# Auto-delete old documents
DELETE FROM documents 
WHERE deleted_at IS NOT NULL 
AND DATE(deleted_at) < NOW() - INTERVAL '30 days'
```

### CCPA Compliance

**Required Notices:**
- Privacy policy
- Data collection disclosure
- Opt-out mechanism

**Implementation:**
```python
# Track consent
class ConsentRecord(Base):
    user_id: str
    consent_type: str  # marketing, analytics, essential
    given_at: datetime
    expires_at: datetime

# Respect opt-out
if not user.marketing_consent:
    skip_marketing_email(user)
```

### HIPAA Readiness

**Requirements:**
- AES-256 encryption
- Audit logging
- Access controls
- Encryption in transit (TLS 1.2+)
- Regular security assessments

**Configuration:**
```python
# HIPAA-specific settings
HIPAA_MODE = True
ENCRYPTION_REQUIRED = True
AUDIT_LOGGING = True
DATA_RESIDENCY = "US"  # Specific regions only
```

### SOC 2 Type II

**Controls:**
- Access controls
- Change management
- Monitoring and logging
- Incident response
- Business continuity

---

## Incident Response

### Security Incident Procedure

**1. Detection**
```python
# Monitor for suspicious activity
if failed_login_count > 5:
    lock_account(user_id)
    send_alert("Multiple failed login attempts")
```

**2. Containment**
```python
# Isolate affected systems
revoke_compromised_tokens()
reset_user_session(user_id)
```

**3. Investigation**
```python
# Review audit logs
logs = db.query(AuditLog).filter(
    AuditLog.user_id == user_id
).order_by(AuditLog.created_at.desc()).all()
```

**4. Recovery**
```python
# Restore from backup
restore_database_from_backup(backup_timestamp)
```

**5. Notification**
```python
# Notify affected users
send_security_notice(
    user_id=affected_user,
    title="Security Alert",
    content="Your account may have been affected..."
)
```

### Security Event Logging

**Log Events:**
```python
# Login attempts
log_event("user_login", user_id, status="success")

# Data access
log_event("document_accessed", user_id, resource_id=doc_id)

# Admin actions
log_event("admin_user_deleted", admin_id, resource_id=deleted_user_id)

# Failed operations
log_event("unauthorized_access_attempt", user_id, status="failed")
```

---

## Security Checklist

### Before Production

- [ ] Disable DEBUG mode
- [ ] Change default passwords
- [ ] Generate strong SECRET_KEY
- [ ] Generate strong ENCRYPTION_KEY
- [ ] Configure SSL/TLS certificates
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure security headers
- [ ] Set up audit logging
- [ ] Enable error tracking
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test disaster recovery
- [ ] Document security procedures

### Regular Maintenance

- [ ] Review security logs weekly
- [ ] Update dependencies monthly
- [ ] Rotate encryption keys annually
- [ ] Audit access controls quarterly
- [ ] Review third-party integrations
- [ ] Conduct security assessments
- [ ] Update firewall rules
- [ ] Test backup restoration
- [ ] Review incident response plan

### Monitoring

- [ ] Failed login attempts
- [ ] Unusual API usage patterns
- [ ] Large data exports
- [ ] Admin actions
- [ ] File upload patterns
- [ ] API error rates
- [ ] Database performance
- [ ] Server resource usage

---

## Contact & Support

For security concerns or vulnerability reports:

**Email:** security@lexshield.ai

**Responsible Disclosure:**
Please do not publicly disclose security vulnerabilities. Report through the security email to allow time for patching.

---

**Last Updated**: 2024  
**Version**: 1.0.0  
**Classification**: Confidential