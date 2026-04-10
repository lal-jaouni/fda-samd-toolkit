# CardioGuard ECG-AI: Cybersecurity Assessment

**Document Version:** 1.0  
**Document Date:** 2026-10-15  
**Standard:** FDA Guidance for Industry: Cybersecurity for Networked Medical Devices (2023)  
**Device:** CardioGuard ECG-AI, Class II SaMD

---

## 1. Cybersecurity Overview

CardioGuard ECG-AI operates as a cloud-based software-as-a-medical-device (SaMD). The device receives patient ECG data via HTTPS API, processes the ECG through machine learning inference, and returns diagnostic results. Given that the device handles protected health information (PHI) and is accessible over the internet, comprehensive cybersecurity controls are essential.

This assessment documents CardioGuard's cybersecurity posture per FDA guidance including threat modeling, vulnerabilities, mitigations, and software bill of materials (SBOM).

---

## 2. Threat Model

### System Architecture

```
EHR System (Hospital)
    |
    | HTTPS (TLS 1.3)
    | OAuth 2.0 authentication
    v
CardioGuard API Gateway (AWS ALB)
    |
    |--- Input validation
    |--- Rate limiting (1000 req/min per client)
    |--- Logging
    v
Microservices (EC2 with GPU)
    |
    |--- Model inference
    |--- De-identification
    |--- Confidence interval calculation
    v
Data Layer (RDS PostgreSQL)
    |--- Encrypted at rest (AES-256)
    |--- Automated backups (encrypted)
    |--- Access controls
    v
AWS Monitoring (GuardDuty, CloudTrail, CloudWatch)
```

### Potential Threats and Adversaries

**External Threat Actors:**

1. **Opportunistic Attackers (Low Sophistication)**
   - Threat: Credential stuffing, unpatched vulnerability exploitation
   - Attack Vector: Automated scanning, public vulnerability databases
   - Mitigation: Strong authentication, patching, WAF

2. **Determined Attackers (Medium Sophistication)**
   - Threat: Targeted breach for patient data theft or ransomware
   - Attack Vector: Phishing, supply chain compromise, zero-day exploits
   - Mitigation: Endpoint protection, incident response, zero-trust architecture

3. **Advanced Persistent Threats (High Sophistication)**
   - Threat: Nation-state espionage or targeted patient data exfiltration
   - Attack Vector: Advanced exploits, social engineering, supply chain
   - Mitigation: Defense-in-depth, threat hunting, security research

**Insider Threats:**

1. **Disgruntled Employee**
   - Threat: Unauthorized data access, model theft, service sabotage
   - Mitigation: RBAC, audit logging, background checks, least privilege

2. **Contractor or Third Party**
   - Threat: Accidental exposure or intentional misuse of credentials
   - Mitigation: Access controls, secure credential management, contracts

### Attack Surfaces

| Attack Surface | Threat | Likelihood | Mitigation |
|---|---|---|---|
| **API Endpoint** | SQL injection, command injection, authentication bypass | Medium | Input validation, parameterized queries, OAuth 2.0 |
| **Network (HTTPS)** | Man-in-the-middle, DDoS | Low | TLS 1.3, AWS Shield Standard |
| **Cloud Infrastructure** | Misconfiguration, unauthorized access | Low-Medium | AWS best practices, IAM roles, VPC security groups |
| **Database** | SQL injection, unauthorized access, privilege escalation | Low | Encryption, access controls, audit logging |
| **Software Dependencies** | Vulnerable libraries (log4j, etc.) | Medium | SBOM, dependency scanning, patching |
| **Admin Console** | Unauthorized access, credential theft | Low | MFA, audit logging, network restrictions |
| **Supply Chain** | Compromised dependency, malicious contributor | Low | SBOM, code review, vendor management |

---

## 3. Security Controls

### Authentication and Authorization

**OAuth 2.0 Implementation:**
- Device protected by OAuth 2.0 bearer token authentication
- Health systems obtain credentials during onboarding
- Tokens have 24-hour expiry; refresh tokens valid for 90 days
- Token revocation on user departure or credential compromise

**Role-Based Access Control (RBAC):**
- Health System Admin: Full access to institution's ECGs and performance reports
- Clinician: Read-only access to patient ECGs and CardioGuard results
- Service Account: API-only access for EHR integration
- Audit Logs: All access logged with timestamp, user, ECG ID, action

### Data Protection

**Encryption in Transit:**
- HTTPS only (TLS 1.3 minimum)
- All API calls encrypted with AES-128 (TLS handshake) + symmetric key encryption
- Certificate pinning available for high-security deployments

**Encryption at Rest:**
- Database: AES-256 encryption (AWS RDS encryption at rest)
- Object Storage: AES-256 encryption (AWS S3 default)
- Backups: Encrypted with same keys as primary data
- Encryption keys managed via AWS Secrets Manager (hardware security module backed)

**Data De-identification:**
- All patient data de-identified per HIPAA Safe Harbor method before logging
- 18 categories of PHI removed: name, address, contact information, medical record number, etc.
- De-identification performed at API gateway level; no PHI in downstream systems

### Input Validation and Output Encoding

**Input Validation:**
```
1. ECG format validation: Check 12 leads present, correct lead ordering
2. Signal length validation: Exactly 10 seconds (+/- 0.1 sec tolerance)
3. Data type validation: Numeric samples within reasonable range (-10 to +10 mV)
4. Sampling rate validation: >= 250 Hz claimed sampling rate
5. JSON schema validation: Request conforms to documented API schema
6. Size limits: Reject requests > 1 MB to prevent memory exhaustion
```

If validation fails, API returns error code 400 (Bad Request) without attempting inference.

**Output Encoding:**
- API returns JSON encoded with Unicode escape sequences for special characters
- No ECG raw data echoed back in responses (only probability scores)
- Timestamps in ISO 8601 format (no sensitive time information revealed)

### Network Security

**AWS VPC and Security Groups:**
- Application tier in private subnet (no direct internet access)
- NAT Gateway for outbound connections
- Security group inbound rules: only allow port 443 (HTTPS) from ALB
- Security group outbound rules: restricted to necessary services (RDS, Secrets Manager)

**Web Application Firewall (WAF):**
- AWS WAF rules:
  - Block SQL injection patterns
  - Block XSS patterns
  - Rate limiting: 1000 requests per minute per IP
  - Geographic IP filtering (optional)

**DDoS Protection:**
- AWS Shield Standard (automatic)
- AWS Shield Advanced optional for additional DDoS mitigation
- CloudFlare as CDN/WAF layer (in evaluation)

### Vulnerability Management

**Software Dependency Scanning:**
```
Tool: Dependabot (GitHub) + Snyk
Frequency: Continuous (on each commit)
Process:
1. Scan all dependencies for known CVEs
2. Flag HIGH and CRITICAL severity vulnerabilities
3. Auto-create pull requests with patched versions
4. Require security team approval before merge
5. Monthly SBOMreporting to stakeholders
```

**Patching Policy:**
- **Critical (CVSS >= 9.0):** Patched within 7 days
- **High (CVSS 7.0-8.9):** Patched within 30 days
- **Medium (CVSS 4.0-6.9):** Patched within 90 days
- **Low (CVSS < 4.0):** Included in quarterly releases

**Security Scanning:**
- Static Application Security Testing (SAST): Weekly via SonarQube
- Dynamic Application Security Testing (DAST): Monthly via Burp Suite
- Infrastructure scanning: Weekly via AWS Inspector
- Container scanning: Per-push via Trivy

### Monitoring and Logging

**Logging Framework:**
- All API requests logged: timestamp, user, ECG ID, model version, output probabilities
- Failed authentication attempts logged: timestamp, username, IP address, reason
- Admin actions logged: user, action, timestamp, changes made
- Logs encrypted and retained for 7 years per HIPAA

**Monitoring and Alerting:**
```
Real-time Monitoring (CloudWatch + Datadog):
1. API error rate > 1% -> Immediate PagerDuty alert
2. Inference latency p99 > 500ms -> Alert
3. Failed authentication attempts > 10 per hour from single IP -> Block IP, alert
4. Unusual data access patterns (e.g., user accessing ECGs from new geography) -> Alert
5. Database connection errors -> Alert
6. GPU memory errors -> Alert
```

### Incident Response

**Incident Response Plan:**
1. **Detection:** Automated alerts via CloudWatch and GuardDuty
2. **Containment:** Isolate affected systems within 1 hour of confirmed breach
3. **Eradication:** Remove malicious code/access, patch vulnerability
4. **Recovery:** Restore from encrypted backups, verify integrity
5. **Notification:** HIPAA breach notification within 24 hours if PHI exposed

**Breach Notification Timeline:**
- Detect breach: < 1 hour (automated monitoring)
- Contain breach: < 1 hour
- Notify affected parties: < 24 hours (per HIPAA)
- Notify FDA: < 30 days (for serious safety-related breaches)
- Notify media: < 30 days (if > 500 residents in same jurisdiction)

---

## 4. Software Bill of Materials (SBOM)

**SBOM Format:** SPDX 2.3 (CycloneDX also available)  
**Last Updated:** 2026-10-15

### Third-Party Libraries

| Component | Version | License | Purpose | Vulnerability Status |
|---|---|---|---|---|
| PyTorch | 2.0.0 | BSD 3-Clause | Deep learning framework | No known vulns |
| NumPy | 1.24.0 | BSD 3-Clause | Numeric computing | No known vulns |
| SciPy | 1.10.0 | BSD 3-Clause | Scientific computing | No known vulns |
| scikit-learn | 1.3.0 | BSD 3-Clause | ML utilities | No known vulns |
| FastAPI | 0.100.0 | MIT | Web framework | No known vulns |
| Gunicorn | 20.1.0 | MIT | WSGI server | No known vulns |
| Pydantic | 2.0.0 | MIT | Data validation | No known vulns |
| SQLAlchemy | 2.0.0 | MIT | ORM | No known vulns |
| boto3 | 1.28.0 | Apache 2.0 | AWS SDK | No known vulns |
| requests | 2.31.0 | Apache 2.0 | HTTP client | No known vulns |

### Operating System and Runtime

| Component | Version | Vulnerability Status |
|---|---|---|
| Python | 3.10.12 | No known vulns (as of 2026-10-15) |
| Debian Linux | 12 (Bookworm) | Security updates current |
| Docker | 24.0.0 | No known vulns |

### Build and Development Tools (Not in Production)

| Tool | Version | Purpose |
|---|---|---|
| PyTest | 7.4.0 | Unit testing |
| Black | 23.0.0 | Code formatting |
| Ruff | 0.1.0 | Linting |
| Mypy | 1.5.0 | Static type checking |

**SBOM Access:** Available on request to authorized security researchers and compliance auditors via encrypted email.

---

## 5. Vulnerability Disclosure Policy

**Scope:** CardioGuard ECG-AI cloud service and associated infrastructure

**Disclosure Timeline:**

1. **Researcher Reports Vulnerability**
   - Email: security@cardiogaurd-medical.com (not public)
   - Include: Vulnerability description, affected component, proof-of-concept if possible
   - Do NOT disclose publicly

2. **CardioGuard Triage (24 hours)**
   - Severity assessment (CVSS score)
   - Reproducibility verification
   - Confirm or reject vulnerability claim

3. **Fix Development**
   - **Critical (CVSS >= 9.0):** 7-day fix target
   - **High (7.0-8.9):** 30-day fix target
   - **Medium (4.0-6.9):** 90-day fix target

4. **Coordinated Disclosure**
   - Fix deployed to production
   - Credit offered to reporter (if desired)
   - Public disclosure (blog post, GitHub security advisory)

5. **Follow-up**
   - 90-day follow-up with researcher to confirm fix
   - Lessons learned review

**Not in Scope (Explicitly Out of Scope for Responsible Disclosure):**
- Social engineering attacks on clinicians or staff
- Attacks on EHR systems at health systems (not CardioGuard responsibility)
- Hardware-based attacks
- Physical security of AWS data centers
- Legal/contractual disputes

---

## 6. Supply Chain Security

### Vendor Management

**Third-Party Code:**
- All third-party libraries sourced from public repositories (PyPI, npm)
- No private or custom-built third-party libraries
- All dependencies pinned to specific versions (reproducible builds)

**Code Review:**
- All code changes reviewed by 2+ developers before merge
- Security team does final review for sensitive changes
- Automated security scanning before merge

**Deployment:**
- Code compiled and containerized in secure build environment
- Container images signed with Docker Content Trust
- Only signed images deployed to production
- Immutable deployment: once deployed, image cannot be modified

### Continuous Integration / Continuous Deployment (CI/CD)

**GitOps Workflow:**
1. Developer commits code to GitHub (in private repository)
2. GitHub Actions runs: unit tests, security scans (SAST, dependency check), linting
3. If all checks pass, code is approved for review
4. After code review, code merged to main branch
5. Merge to main triggers: build Docker image, sign with Docker Content Trust, push to private ECR
6. ArgoCD monitors ECR; detects new image, automatically deploys to staging environment
7. Manual approval required to deploy to production
8. Production deployment: blue-green deployment (no downtime, easy rollback)

---

## 7. Security Testing and Validation

### Penetration Testing

**Schedule:** Annual (required) + ad-hoc (if major changes)  
**Scope:** API endpoints, web portal, authentication, data exposure
**Method:** Black-box and gray-box testing by third-party security firm
**Last Test:** 2026-09-30 (findings remediated before submission)

**Test Results (2026-09-30):**
- No critical vulnerabilities found
- 2 high-severity issues identified and fixed (authentication bypass in edge case, SQL injection in legacy API endpoint)
- 3 medium-severity findings (deprecated TLS 1.0 still available on internal endpoint, weak CORS headers)
- All findings remediated before 2026-10-15 submission

### Automated Security Testing

**Weekly Scans:**
- SonarQube SAST: Static code analysis for security anti-patterns
- Snyk: Dependency vulnerability scanning
- AWS Inspector: Infrastructure vulnerability scanning
- Trivy: Container image scanning

**Monthly Scans:**
- Burp Suite DAST: Dynamic web application testing
- CloudSploit: AWS configuration audit

### Red Team Exercise

**Schedule:** Annual (Q3 2026)  
**Scope:** Full attack simulation including phishing, lateral movement, data exfiltration
**Results:** Simulated attacker successfully compromised development VM; recommended network segmentation improvements implemented

---

## 8. Post-Market Cybersecurity Management

**Commitment to Ongoing Security:**

1. **Quarterly Security Reviews:** Risk assessment, threat landscape changes, new controls
2. **Annual Penetration Testing:** Third-party security assessment
3. **Continuous Monitoring:** 24/7 monitoring via AWS GuardDuty + SIEM
4. **Vulnerability Disclosure Program:** Responsible disclosure for researcher-found vulnerabilities
5. **Patch Management:** Critical vulnerabilities patched within 7 days
6. **Security Training:** Annual training for all employees on security best practices
7. **Incident Response Drills:** Quarterly tabletop exercises to test IR plan

**Notification of Clinicians:**
- If security incident affects deployed instances, health systems notified within 24 hours
- Technical details provided so IT teams can assess impact
- Workarounds provided if necessary pending patch deployment

---

## 9. Compliance and Standards

**Standards Alignment:**
- NIST Cybersecurity Framework: Core functions (Identify, Protect, Detect, Respond, Recover) implemented
- OWASP Top 10: Controls implemented for all 10 categories
- CIS Critical Security Controls: Implemented 15+ controls
- HIPAA Security Rule: All requirements (Administrative, Physical, Technical Safeguards) met
- SOC 2 Type II: Third-party audited; controls operating effectively for 12+ months

---

## 10. Conclusion

CardioGuard ECG-AI implements comprehensive cybersecurity controls aligned with FDA guidance and industry best practices. Threat modeling identified potential attack surfaces; mitigations address all identified threats to acceptable risk levels. Continuous monitoring and patching processes ensure that new vulnerabilities are detected and remediated promptly.

No identified cybersecurity risk would prevent FDA clearance or clinical deployment. Cybersecurity posture will be maintained and enhanced post-market per the post-market management plan.

---

**Document Certification**

This cybersecurity assessment is accurate and complete per FDA guidance (2023). Security controls are in place and validated.

**Security Lead:** Jane Smith, Chief Information Security Officer  
**Date:** 2026-10-15
