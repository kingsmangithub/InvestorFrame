# InvestorFrame Lean

InvestorFrame Lean is a calm, static-first investment decision system.

It is built to help one self-directed investor do five things well:

1. frame the market simply
2. write down a real investment thesis
3. block impulsive decisions
4. review decision quality after the fact
5. compound personal investment wisdom over time

This is a deliberate refactor away from a heavier market-intelligence shape.

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

## Product definition

InvestorFrame = **Frame + Idea + Decision Gate + Review + Wisdom**

## Pages

- `/` — home
- `/desk` — today’s frame and active ideas
- `/ideas/:ticker` — single idea page
- `/reviews` — decision quality review log
- `/rulebook` — investing rules and behavior constraints

## Architecture

### Frontend
- React + Vite
- static demo data
- no client-side query cache
- no state store

### Backend/core
- small Python package
- YAML-configured rules
- static JSON build path
- SQLite optional later, not required on day one

### Deployment
- Cloudflare Pages for the site
- GitHub Actions for static data generation later
- no always-on backend required

## Repository structure

```text
config/
  frame_rules.yaml
  behavior_rules.yaml
  sell_rules.yaml
  review_rules.yaml
  principles.yaml

data/
  generated/

investorframe/
  app/
  frame/
  discipline/
  outputs/

dashboard/
  src/
    pages/
    components/
    content/
```

## What was intentionally removed

- `api/`
- `cli/`
- live dashboard/report/scenario architecture
- sentiment analysis layer
- watchlist scoring engine
- report templates
- Docker-first deployment path

## Operating principle

Build the smallest version that you would personally use every week.
Do not add a feature unless it makes research clearer, slower in the right way, or more durable.
