# Email Communication Infrastructure for Agents

**Date:** 2026‑03‑27  
**Author:** CTO  
**Status:** Proposal

## Overview

Enable @theoffice_ agents to send and receive email through a secure, scalable infrastructure. This allows agents to communicate with external parties, send notifications, and handle email‑based workflows.

## Architecture

### 1. **Email Aliases System**
```
Pattern: {agent}@{domain}.{tld}
Examples:
  · ceo@theoffice.ltd
  · cto@theoffice.ltd  
  · supakaren@theoffice.ltd (for Morten Lund project)
  · signal‑scout@theoffice.ltd
  · cao@theoffice.ltd
```

### 2. **Mail Server Stack**
```
Components:
  · Postfix (MTA) – Mail transfer agent
  · Dovecot (IMAP/POP3) – Mail delivery agent
  · OpenDKIM/OpenDMARC – Email authentication
  · SpamAssassin – Spam filtering
  · PostgreSQL – Virtual mailbox mapping
```

### 3. **Agent Integration Layer**
```
OpenClaw → SMTP API → Email Queue → Delivery
           ↑                    ↓
      Agent Requests      Status Tracking
```

## Implementation Phases

### Phase 1: Domain & DNS Setup
1. **Configure DNS records** for `theoffice.ltd`:
   ```
   MX   10 mail.theoffice.ltd
   A    mail.theoffice.ltd → 129.151.217.45
   TXT  v=spf1 ip4:129.151.217.45 ~all
   TXT  v=DMARC1; p=none; rua=mailto:dmarc@theoffice.ltd
   ```
2. **SSL certificates** via Let's Encrypt
3. **Reverse DNS** setup with Oracle Cloud

### Phase 2: Mail Server Installation
```bash
# Install packages
apt‑get install postfix dovecot‑imapd dovecot‑pop3d \
  opendkim opendkim‑tools opendmarc spamassassin \
  postgresql postfix‑pgsql

# Configure Postfix with PostgreSQL virtual mailboxes
# Set up OpenDKIM/OpenDMARC for email authentication
# Configure Dovecot for IMAP access
```

### Phase 3: Agent Email API
```python
# Example: OpenClaw email plugin
class EmailPlugin:
    def send_email(self, agent_id, to, subject, body, attachments=None):
        # Validate agent permissions
        # Queue email for delivery
        # Log for audit trail
        # Return message ID for tracking
```

### Phase 4: Security & Compliance
1. **Rate limiting** – Prevent email abuse
2. **Content filtering** – Scan for sensitive data
3. **Audit logging** – All emails logged with metadata
4. **Approval workflows** – Optional human review for external emails

## Agent Email Use Cases

### 1. **CEO Communications**
- Investor updates
- Board meeting summaries
- External stakeholder communications

### 2. **CTO Technical Notifications**
- System alerts
- Deployment notifications
- Security advisories

### 3. **Supakaren Analyst (Morten Lund)**
- Investment opportunity summaries
- Portfolio company updates
- Market intelligence reports

### 4. **Signal Scout**
- News digest emails
- Alert notifications
- Research summaries

### 5. **CAO Research Delivery**
- Research report distribution
- Data export notifications
- Collaboration requests

## Security Considerations

### Authentication & Authorization
- **Agent‑specific credentials** – Each agent has unique SMTP credentials
- **Scope restrictions** – Agents can only send from their alias
- **Rate limits** – Prevent spam/abuse
- **Content policies** – No sensitive data in emails

### Email Authentication
- **SPF** – Authorized sending servers
- **DKIM** – Cryptographic message signing
- **DMARC** – Policy enforcement
- **BIMI** – Brand indicators (future)

### Data Protection
- **Encryption** – TLS for transmission
- **Logging** – Full audit trail
- **Retention** – Email storage policies
- **GDPR compliance** – For EU communications

## Integration with OpenClaw

### Configuration
```json
{
  "email": {
    "enabled": true,
    "smtp_host": "127.0.0.1",
    "smtp_port": 587,
    "default_domain": "theoffice.ltd",
    "rate_limit": "10/hour",
    "require_approval": ["external", "high_risk"]
  }
}
```

### Agent Permissions
```yaml
ceo:
  email:
    aliases: ["ceo@theoffice.ltd"]
    daily_limit: 100
    can_send_external: true
    approval_required: false

cto:
  email:
    aliases: ["cto@theoffice.ltd"]
    daily_limit: 50
    can_send_external: true
    approval_required: false

signal‑scout:
  email:
    aliases: ["alerts@theoffice.ltd"]
    daily_limit: 1000
    can_send_external: false
    approval_required: false
```

## Deployment Steps

### Week 1: Infrastructure
1. DNS configuration for `theoffice.ltd`
2. Mail server installation and basic configuration
3. SSL certificate setup
4. Basic send/receive testing

### Week 2: Agent Integration
1. OpenClaw email plugin development
2. Agent alias configuration
3. Permission system implementation
4. Internal testing between agents

### Week 3: Security & Monitoring
1. SPF/DKIM/DMARC configuration
2. Rate limiting implementation
3. Audit logging system
4. Alerting for email failures

### Week 4: Production Rollout
1. External email testing
2. Performance optimization
3. Documentation completion
4. Training for agent usage

## Cost Estimates

### Infrastructure
- **Domain:** `theoffice.ltd` – $15/year
- **Server:** Existing Oracle Cloud instance – $0 (already running)
- **SSL:** Let's Encrypt – $0
- **Software:** Open source – $0

### Maintenance
- **Monitoring:** 1‑2 hours/week
- **Updates:** Monthly security patches
- **Backup:** Email database backups

## Risks & Mitigations

### Risk 1: Email Abuse
- **Mitigation:** Strict rate limits, content filtering, approval workflows

### Risk 2: Deliverability Issues
- **Mitigation:** Proper SPF/DKIM/DMARC setup, warm‑up period for new domain

### Risk 3: Security Breach
- **Mitigation:** Isolated mail server, regular security updates, intrusion detection

### Risk 4: Compliance Violations
- **Mitigation:** Audit logging, data retention policies, GDPR‑aware design

## Success Metrics

### Technical
- **Deliverability rate:** >95%
- **Spam score:** <5 (SpamAssassin)
- **Uptime:** 99.9%
- **Latency:** <5 seconds for email delivery

### Business
- **Agent adoption:** All major agents using email within 30 days
- **External communications:** CEO/CTO regularly emailing stakeholders
- **Automation:** Reduced manual email tasks by 80%

## Next Steps

### Immediate (Next 7 days)
1. **DNS configuration** for `theoffice.ltd`
2. **Postfix/Dovecot installation** on Oracle Cloud instance
3. **Basic send/receive testing** with test accounts

### Short‑term (Next 30 days)
1. **OpenClaw email plugin** development
2. **Agent alias configuration** (CEO, CTO, Signal Scout)
3. **Security hardening** (SPF/DKIM/DMARC)

### Long‑term (Next 90 days)
1. **Advanced features** (attachments, templates, scheduling)
2. **Monitoring dashboard** for email metrics
3. **Integration with other services** (calendar, contacts)

## Conclusion

Email communication is essential for professional agent operations. This proposal outlines a secure, scalable infrastructure that enables @theoffice_ agents to communicate effectively while maintaining security and compliance standards.

**Recommended approach:** Start with Phase 1 (DNS/domain setup) and proceed incrementally, testing thoroughly at each stage.