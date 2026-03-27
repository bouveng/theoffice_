# Saxo Bank OpenAPI

**Category:** Financial Trading Platform  
**Provider:** Saxo Bank A/S  
**URL:** https://www.developer.saxo/  
**Status:** Active (2026‑03‑27)

## Quick Reference

### Authentication
- **Method:** OAuth 2.0, Bearer tokens
- **Token lifespan:** 24‑hour test tokens available
- **Environments:** Simulation (sim), Live (prod)
- **Application keys:** Required for live access

### Endpoints
```
# Simulation
REST:    https://gateway.saxobank.com/sim/openapi/
Stream:  wss://sim‑streaming.saxobank.com/sim/oapi/streaming/ws

# Live
REST:    https://gateway.saxobank.com/openapi/
Stream:  wss://streaming.saxobank.com/oapi/streaming/ws
```

### Service Groups
| Group | Purpose | Key Endpoints |
|-------|---------|---------------|
| **Portfolio** | Account positions, balances, orders | `/port/v1/balances`, `/port/v1/positions` |
| **Trade** | Order placement, execution | `/trade/v1/orders`, `/trade/v1/prices` |
| **Reference Data** | Instruments, exchanges, sectors | `/ref/v1/instruments`, `/ref/v1/exchanges` |
| **Chart** | Historical price data | `/chart/v1/charts` |
| **Market Overview** | Market data, news | `/mkt/v1/overview` |
| **Client Management** | Account management | `/cm/v1/clients` |

## Common Use Cases

### 1. Portfolio Monitoring
```bash
# Get account balances
GET /port/v1/balances
Authorization: Bearer {token}

# Get open positions  
GET /port/v1/positions
Authorization: Bearer {token}
```

### 2. Market Data Streaming
```javascript
// WebSocket connection
const ws = new WebSocket(
  `wss://sim‑streaming.saxobank.com/sim/oapi/streaming/ws` +
  `?authorization=${encodeURIComponent('Bearer ' + token)}` +
  `&contextId=${contextId}`
);
```

### 3. Order Management
```bash
# Place order
POST /trade/v1/orders
{
  "AccountKey": "ABC123",
  "Uic": 21,
  "AssetType": "Stock",
  "Amount": 100,
  "BuySell": "Buy",
  "OrderType": "Market"
}
```

## Rate Limits
- **Standard:** Undisclosed (varies by endpoint)
- **Streaming:** Up to 3 updates/second per subscription
- **Best practice:** Implement exponential backoff

## Development Resources

### Getting Started
1. **Create simulation account:** https://www.developer.saxo/accounts/sim/signup
2. **Get 24‑hour token:** https://www.developer.saxo/openapi/token
3. **Explore API:** https://www.developer.saxo/openapi/explorer
4. **Review docs:** https://www.developer.saxo/openapi/learn

### Sample Code
- **JavaScript:** https://github.com/SaxoBank/openapi‑samples‑js
- **Streaming examples:** `/websockets` directory
- **Authentication examples:** `/authentication` directory

## @theoffice_ Integration Notes

### Agent Design Patterns
```yaml
saxo‑portfolio‑monitor:
  triggers:
    - cron: "0 9 * * *"  # Daily 09:00 UTC
    - webhook: saxo‑position‑alert
  actions:
    - fetch‑portfolio
    - calculate‑metrics
    - send‑discord‑alert
  secrets:
    - SAXO_API_KEY
    - SAXO_CLIENT_ID
```

### Security Considerations
- Store API keys in OpenClaw secrets
- Use simulation environment for development
- Implement circuit breakers for error handling
- Log all API interactions for audit

### Error Handling
- **429:** Rate limit – implement backoff
- **401:** Token expired – refresh logic
- **503:** Service unavailable – retry with delay
- **Market hours:** Some endpoints unavailable outside trading hours

## Support
- **OpenAPI Support:** https://openapi.help.saxo/hc/en‑us
- **Email:** openapisupport@saxobank.com
- **Documentation:** Comprehensive with interactive tools

---
**Last updated:** 2026‑03‑27  
**Maintained by:** CTO  
**Status:** Research complete, ready for prototype