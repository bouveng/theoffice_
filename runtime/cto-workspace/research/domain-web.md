# Domain & Web Server Analysis: theoffice.ltd

**Date:** 2026-03-26  
**Analyst:** CTO  
**Status:** Analysis Complete, Awaiting Implementation

## Current Situation

### Instance Configuration
- **Hostname:** `theoffice`
- **Public IP:** `129.151.217.45` (Oracle Cloud ARM)
- **Instance State:** Running, healthy
- **Current Services:** SSH only (port 22)

### Domain Status
- **Domain:** `theoffice.ltd`
- **Current DNS:** Resolves but shows **502 Bad Gateway** (nginx/openresty detected elsewhere)
- **Conclusion:** Domain registered but not pointing to our instance

### Local Services Assessment
- **Web Servers:** None running on ports 80/443
- **OpenClaw Gateway:** Bound to loopback (`127.0.0.1:18789`)
- **Firewall:** Oracle Cloud security lists allow SSH only
- **Local iptables:** Restrictive, blocks HTTP/HTTPS

## Technical Analysis

### Network Path
```
User → DNS (theoffice.ltd) → Current IP (not ours) → 502 Error
Required: User → DNS → 129.151.217.45 → Our Services
```

### Current Constraints
1. **DNS Mismatch:** Domain points elsewhere
2. **No Web Server:** Ports 80/443 not serving
3. **Firewall Blocked:** Inbound HTTP/HTTPS traffic denied
4. **Gateway Isolation:** OpenClaw only accessible locally

## Recommended Implementation Plan

### Phase 1: DNS Configuration
**Action:** Update A records to point to `129.151.217.45`
- `theoffice.ltd` → `129.151.217.45`
- `www.theoffice.ltd` → `129.151.217.45`
- **TTL:** 300 seconds for quick propagation

### Phase 2: Web Server Setup
**Option A: Nginx (Recommended)**
- Lightweight, performant
- Reverse proxy capability
- Mature ecosystem

**Option B: Caddy**
- Automatic SSL
- Simpler configuration
- Built-in HTTPS

### Phase 3: OpenClaw Gateway Exposure
**Architecture:** Reverse proxy via nginx
- External: `https://theoffice.ltd`
- Internal: `http://127.0.0.1:18789`
- Benefits: SSL termination, load balancing, security

### Phase 4: SSL/TLS Implementation
**Method:** Let's Encrypt via Certbot
- Automated certificate issuance
- Auto-renewal (90-day cycle)
- Supports both domain and www subdomain

### Phase 5: Firewall Configuration
**Oracle Cloud Console:**
1. Security Lists → Add Ingress Rules
2. Port 80 (HTTP) from 0.0.0.0/0
3. Port 443 (HTTPS) from 0.0.0.0/0

**Local Firewall (UFW):**
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

## Quick Implementation Script

```bash
#!/bin/bash
# theoffice.ltd setup script

# 1. System update
sudo apt update && sudo apt upgrade -y

# 2. Install nginx
sudo apt install nginx -y

# 3. Configure nginx reverse proxy
sudo tee /etc/nginx/sites-available/theoffice << 'EOF'
server {
    listen 80;
    server_name theoffice.ltd www.theoffice.ltd;
    
    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# 4. Enable site
sudo ln -sf /etc/nginx/sites-available/theoffice /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 5. SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d theoffice.ltd -d www.theoffice.ltd --non-interactive --agree-tos

# 6. Configure firewall
sudo apt install ufw -y
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw --force enable

echo "Setup complete. Visit https://theoffice.ltd"
```

## Security Considerations

### Immediate
1. **Rate Limiting:** Implement in nginx
2. **Access Logs:** Monitor for suspicious activity
3. **Fail2ban:** Install for brute force protection

### Medium-term
1. **WAF Rules:** Web Application Firewall
2. **DDoS Protection:** Cloudflare or similar
3. **Backup Strategy:** Regular configuration backups

### Long-term
1. **Monitoring:** Prometheus + Grafana
2. **Alerting:** Slack/Discord notifications
3. **Audit:** Regular security reviews

## Verification Checklist

- [ ] DNS propagation complete
- [ ] `curl -I https://theoffice.ltd` returns 200 OK
- [ ] OpenClaw dashboard accessible
- [ ] SSL certificate valid
- [ ] Firewall rules applied
- [ ] Logs being captured
- [ ] Backup system in place

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| DNS Update | 5-30 min | Domain control access |
| Web Server | 15 min | DNS propagated |
| SSL Setup | 10 min | Web server running |
| Firewall | 5 min | All services up |
| Testing | 10 min | Everything configured |

**Total:** ~45-70 minutes

## Risk Assessment

### Low Risk
- Nginx installation (standard package)
- Firewall configuration (reversible)
- Certbot SSL (automated, renewable)

### Medium Risk
- DNS changes (propagation delay)
- OpenClaw exposure (security review needed)

### Mitigations
- Test configuration before applying
- Maintain backup of original state
- Monitor logs during implementation

## Next Steps

1. **Awaiting:** DNS control/access from domain owner
2. **Ready:** Implementation scripts prepared
3. **Pending:** Go/no-go decision for deployment

## References

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Certbot](https://certbot.eff.org/)
- [Oracle Cloud Networking](https://docs.oracle.com/en-us/iaas/Content/Network/Concepts/overview.htm)
- [OpenClaw Gateway Configuration](https://docs.openclaw.ai/gateway)