# InvestorFrame Lean

InvestorFrame Lean is a calm, static-first investment decision system.

It is built to help one self-directed investor do five things well:

1. frame the market simply
2. write down a real investment thesis
3. block impulsive decisions
4. review decision quality after the fact
5. compound personal investment wisdom over time

This is a deliberate refactor away from a heavier market-intelligence shape.

## Product definition

InvestorFrame = **Frame + Idea + Decision Gate + Review + Wisdom**

## Pages

- `/` — home
- `/desk` — today’s frame and active ideas
- `/ideas/:ticker` — single idea page
- `/reviews` — decision quality review log
- `/rulebook` — investing rules and behavior constraints

## What changed

The old shape tried to do too much:
- live API surface
- CLI layer
- scenario lab
- report generation
- sentiment stack
- watchlist scoring
- multiple product surfaces

The new shape keeps only the pieces that directly improve decisions.

## Frontend
- React + Vite
- static JSON from `dashboard/public/data`
- no client-side query cache
- no state store

## Backend/core
- small Python package
- YAML-configured rules
- static JSON build path
- SQLite optional later, not required on day one

## Build static payloads

```bash
python -m pip install -e .
investorframe-build
investorframe-sync-data
```

## Build the site

```bash
cd dashboard
npm install
npm run build
```

## Deployment
- Cloudflare Pages for the site
- GitHub Actions for static data generation
- no always-on backend required

## Docs
- `docs/REFACTOR_CUT_LIST.md`
- `docs/LEAN_ARCHITECTURE.md`
- `docs/FIELD_SPEC.md`
- `docs/CLOUDFLARE_PAGES_SETUP.md`

## Operating principle

Build the smallest version that you would personally use every week.
Do not add a feature unless it makes research clearer, slower in the right way, or more durable.
