# Numad.AI — Identity Intelligence Cloud

Streamlit in Snowflake app for sovereign identity resolution and retail media activation across the MENA ecosystem.

## Files

| File | Purpose |
|---|---|
| `streamlit_app.py` | Main Streamlit app — deploy directly to Snowflake |
| `environment.yml` | Package dependencies for Streamlit in Snowflake |
| `numad_app.jsx` | Original React design reference (do not deploy) |

## Deploy to Snowflake (Streamlit in Snowflake)

### Option A — Snowsight UI
1. In Snowsight, go to **Streamlit** → **+ Streamlit App**
2. Set your database, schema, and warehouse
3. Paste / upload `streamlit_app.py`
4. The packages (`plotly`, `pandas`) are available in the Snowflake Anaconda channel — no extra setup needed

### Option B — Cortex Analyst / Snowflake CLI
```bash
snow streamlit deploy \
  --file streamlit_app.py \
  --database <YOUR_DB> \
  --schema <YOUR_SCHEMA> \
  --warehouse <YOUR_WH>
```

### Option C — GitHub integration (recommended)
1. Push this repo to GitHub
2. In Snowsight → Streamlit → **Connect Git repository**
3. Point to this repo, select `streamlit_app.py` as the entrypoint
4. Snowflake will sync automatically on push

## App Structure

```
Landing (Overview)
├── 01 · Ingest Data
│   ├── Native Snowflake Objects (file/export path)
│   └── Open Flow Connectors (OAuth direct sync)
├── 02 · Create Graph
│   ├── Overlap diagram (Venn)
│   ├── Signal coverage before/after
│   └── Segment expansion table
├── 03 · Activate Audiences
│   ├── Retail Media Networks (Noon, Carrefour, LuLu, Panda, Jarir, Danube)
│   └── DSP & Ad Tech (DV360, Meta, Snapchat, TikTok, Amazon DSP, TTD, STC Ads)
└── 04 · Measure Campaigns
    ├── KPI cards (Reach, Conversions, ROAS, Revenue)
    ├── ROAS by channel (bar chart)
    ├── 6-week ROAS trend (line chart)
    └── Incrementality measurement table
```

## Key Numbers (demo data)

| Metric | Value |
|---|---|
| Input IDs | 82K |
| Match rate | 87% |
| Matched IDs | 71K |
| New reach via graph links | 66K |
| Total addressable | 137K (+67%) |
| Signals before / after | 3 → 11 |
| Incremental ROAS | 3.8x |

## Compliance

- Saudi PDPL & SDAIA framework enforced at Snowflake object level
- SHA-256 + HMAC-SHA256 hashing client-side before ingest
- Differential privacy ε=1.0 with k≥50 aggregation threshold
- Data residency: KSA only (AWS me-central-1)
- Activation via hashed match keys only — no raw data shared
