# OverLLM Primitive Ledger: RentMasseur $130,080 KPI Derivative

This repository turns a RentMasseur analytics screenshot and associated MultimodalText / OverLLM thesis into a reproducible KPI asset register.

It does **not** claim booked revenue. It measures **contact-action intelligence**:

```text
contact_action_density = (phone_clicks + email_clicks) / unique_visits
```

## Clean 30-day facts

- Total visits: **2,226**
- Unique visits: **1,770**
- Phone clicks: **85**
- Email clicks: **30**
- Contact actions: **115**
- Contact-action density: **6.50%**
- Average contact actions/day: **3.83**
- Gross visible opportunity at $159/session: **$18,285/month** if every contact converted

## Main operating conclusion

Your page is not dead. It is inconsistent. The money is in stabilizing the page above **10% contact-action density** and turning phone-first interest into confirmed appointments.

## Why this is repo-grade

A spreadsheet is static. This repo makes the derivation reproducible:

- raw daily data in CSV
- KPI derivative tables
- revenue uplift scenarios
- valuation waterfall
- receipt hash helper
- CLI report generator
- tests
- GitHub Actions CI
- daily primitive-ledger workflow stub

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python -m overllm_kpi.cli --exclude-partial
```

## $130,080 valuation waterfall

| Component | Value |
|---|---:|
| Current annual closeable opportunity at 30% close | $65,826 |
| 10% contact-density uplift annual value at 20% close | $23,659 |
| Canonicalization / receipt R&D asset floor | $25,000 |
| Landing page + reporting integration | $15,595 |
| Structured appraisal total | **$130,080** |

## Client line

> This is not a spreadsheet with cologne on it. It is a conversion X-ray: it shows when the profile is flirting with money, when it gets shy, and when 62 people stare at the door and leave.

## Limitation

This is a KPI derivative and appraisal model, not guaranteed cash flow. To convert into revenue proof, add appointment logs with: contact timestamp, response time, booked/not-booked, price objection, ghosted, wrong fit, actual paid amount.
