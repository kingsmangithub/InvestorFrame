# Cloudflare Pages setup for InvestorFrame Lean

## Recommended model
- Private core repo for product logic
- Public site repo for the landing page and static build output
- Static-first deployment to Cloudflare Pages

## Build strategy
1. Run `investorframe-build`
2. Run `investorframe-sync-data`
3. Build the dashboard with Vite
4. Publish `dashboard/dist`

## Cloudflare Pages settings
- Framework preset: `None` or `Vite`
- Root directory: `dashboard`
- Build command: `npm run build`
- Build output directory: `dist`

## Before each deploy
Make sure `dashboard/public/data/*.json` exists.

## Local deploy simulation
From the repo root:

```bash
python -m pip install -e .
investorframe-build
investorframe-sync-data
cd dashboard
npm install
npm run build
```

## Why this setup is lighter
- no always-on backend
- no production database
- no server process to monitor
- no API security surface on day one
- content updates happen by rebuilding static JSON
