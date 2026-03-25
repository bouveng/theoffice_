# Office Budget

Rough cost model for building and running the Office through to MVP and first useful production deployment. All figures are estimates — hardware prices fluctuate, exact salary costs depend on employment structure and social contributions.

Figures in EUR where possible, SEK where relevant for Swedish salary context. EUR/SEK ~11.4.

---

## Hardware

### Development hardware (needed now)

| Item | Spec | Est. cost |
|---|---|---|
| Mac Mini M4 Pro | 64GB unified memory, 2TB SSD | ~€2,200 |
| Peripherals | Monitor, keyboard, cables | ~€400 |
| **Subtotal** | | **~€2,600** |

The Mac Mini runs all MVP models sequentially and is sufficient for development through MVP validation. It is not thrown away post-MVP — it becomes a secondary test node.

### Production hardware (needed for full Office deployment, Q2–Q3 2026)

| Item | Spec | Est. cost |
|---|---|---|
| Mac Studio M5 Ultra | 512GB unified memory, 8TB internal SSD | €17,000–€23,000 |
| External storage | OWC ThunderBlade 4TB (trace logs, model archive) | ~€1,200 |
| UPS | APC Smart-UPS X 1500VA (power protection) | ~€700 |
| Network | Managed switch, cabling | ~€200 |
| **Subtotal** | | **~€19,100–€25,100** |

Mid-point estimate used in runway calculations: **€22,000**

### Total hardware (dev + production)
| Scenario | Cost |
|---|---|
| Dev only (MVP build) | ~€2,600 |
| Dev + production | ~€24,600–€27,700 |

---

## Salaries

Moderate salaries for a Malmö-based early-stage startup. These are below market rate for experienced developers — appropriate for a founder/co-founder setup with equity upside. Figures are gross monthly salary (SEK), followed by total employer cost including Swedish social security contributions (~31.42% of gross).

| Role | Gross/month (SEK) | Employer cost/month (SEK) | Employer cost/month (EUR) |
|---|---|---|---|
| Lead developer / technical founder | 40,000 | ~52,600 | ~€4,600 |
| Developer | 35,000 | ~46,000 | ~€4,050 |
| Product / operations | 32,000 | ~42,100 | ~€3,700 |

These figures assume direct employment. A co-founder taking dividends instead of salary has lower short-term cost but more setup complexity — not modelled here.

### Monthly burn by team size

| Team | Monthly salary cost | + Ops & tooling (~€500) | Total monthly burn |
|---|---|---|---|
| 1 person (lead dev) | ~€4,600 | €500 | **~€5,100** |
| 2 people (lead + dev) | ~€8,650 | €500 | **~€9,150** |
| 3 people (lead + dev + ops) | ~€12,350 | €500 | **~€12,850** |

Ops & tooling includes: cloud backup, domain, basic SaaS tools, development services. Excludes office space (assumed provided by incubator during MVP phase).

---

## Runway to MVP

MVP target: end of Q2 2026 (June 2026). From now (March 2026) that is approximately **4 months**.

| Team size | Monthly burn | 4-month salary + ops | Dev hardware | Total to MVP |
|---|---|---|---|---|
| 1 person | ~€5,100 | ~€20,400 | €2,600 | **~€23,000** |
| 2 people | ~€9,150 | ~€36,600 | €2,600 | **~€39,200** |
| 3 people | ~€12,850 | ~€51,400 | €2,600 | **~€54,000** |

These figures do not include production hardware (Mac Studio) — that purchase is timed to coincide with the MVP going live, not during the build phase.

---

## Runway to First Useful Production Deployment

After MVP (Q3 2026): deliver the full Office to internal use and begin onboarding first external clients. Assume an additional 3 months post-MVP (September 2026). Total runway from now: **7 months**.

| Team size | Monthly burn | 7-month salary + ops | Dev hardware | Production hardware | Total |
|---|---|---|---|---|---|
| 1 person | ~€5,100 | ~€35,700 | €2,600 | €22,000 | **~€60,300** |
| 2 people | ~€9,150 | ~€64,050 | €2,600 | €22,000 | **~€88,650** |
| 3 people | ~€12,850 | ~€89,950 | €2,600 | €22,000 | **~€114,550** |

---

## Summary

| Milestone | 1 person | 2 people | 3 people |
|---|---|---|---|
| To MVP (4 months, dev hardware only) | ~€23K | ~€39K | ~€54K |
| To first production deployment (7 months, incl. Mac Studio) | ~€60K | ~€89K | ~€115K |

---

## Notes and Assumptions

- **Office space**: assumed provided by incubator through MVP phase. If renting in Malmö, add €800–€1,500/month for shared office or hot-desk arrangement.
- **Mac Studio pricing**: Apple has not announced M5 Ultra availability or final pricing as of March 2026. The €17K–€23K range is based on M3 Ultra pricing scaled for next generation. Actual price may vary.
- **No API costs**: the architecture runs entirely on local hardware — no OpenAI, Anthropic, or other inference API bills. This is a deliberate cost containment decision.
- **No marketing budget modelled**: first clients are assumed to come from the incubator network and direct outreach. Paid acquisition is not a Q2–Q3 expense.
- **Social contributions**: 31.42% applies to salaries up to the social security ceiling. Above that it is lower, but at these salary levels the full rate applies.
- **These are floor estimates**: they assume a focused team delivering on schedule. Add 20–30% buffer for realistic project contingency.
