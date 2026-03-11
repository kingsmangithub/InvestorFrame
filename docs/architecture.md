# InvestorFrame Architecture

## Overview

InvestorFrame is an **event-driven market intelligence system** designed to help users interpret market structure before reacting to market noise.

Its core workflow is:

**Event Ingestion → Regime Framing → Sector Transmission → Watchlist Mapping → Scenario Simulation**

InvestorFrame is not built as a trading engine. It is built as a **research-first, explainable, scenario-aware market framework**.

---

## Design Goals

InvestorFrame is designed to be:

- event-first
- regime-aware
- explainable
- modular
- research-oriented
- public-repo friendly
- extensible toward future hosted workflows

The project intentionally avoids positioning itself as:

- a deterministic predictor
- an automated trader
- a black-box stock picker
- a certainty machine

---

## System Diagram

InvestorFrame is a layered library with thin CLI and API surfaces. All business logic lives in the `investorframe/` package; the API and CLI are stateless consumers.

```
                     ┌──────────────┐
                     │  CLI / Cron  │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │   FastAPI    │  ← thin serving layer
                     └──────┬───────┘
                            │
          ┌─────────────────▼─────────────────────┐
          │         Pipeline Orchestrator          │
          │  (5 phases, parallel where possible)   │
          └─────────────────┬─────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌───────────┐     ┌─────────────┐     ┌───────────┐
  │   FRED    │     │   NewsAPI   │     │  yfinance  │
  │ economic  │     │  headlines  │     │  prices &  │
  │  series   │     │  & articles │     │  indices   │
  └─────┬─────┘     └──────┬──────┘     └─────┬─────┘
        └───────────────────┼───────────────────┘
                            ▼
                   ┌─────────────────┐
                   │  Event Parser   │
                   │  + Classifier   │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼                           ▼
     ┌─────────────────┐        ┌─────────────────┐
     │    Sentiment     │        │     Regime       │
     │   Analyzer +     │        │    Detector      │
     │   Aggregator     │        │  (5 indicators)  │
     └────────┬────────┘        └────────┬────────┘
              └─────────────┬─────────────┘
                            ▼
                   ┌─────────────────┐
                   │  Sector Engine  │
                   │  YAML rules ×   │
                   │  regime modifier│
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │ Watchlist Scorer│
                   │ sector inherit  │
                   │ + beta amplify  │
                   └────────┬────────┘
                            ▼
                   ┌─────────────────┐
                   │   Risk Gates    │
                   │  + Disclaimers  │
                   └────────┬────────┘
                            ▼
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          ┌───────┐   ┌─────────┐   ┌──────────┐
          │ JSON  │   │  HTML   │   │ Markdown │
          └───────┘   └─────────┘   └──────────┘
```

---

## System Layers

### 1. Input Layer

The input layer captures the market-moving changes that matter.

Examples include:

- macro releases
- policy signals
- geopolitical shocks
- narrative shifts
- yields
- commodities
- volatility context

This layer answers: **What changed in the world?**

### 2. Market Frame Layer

This layer translates raw inputs into a coherent market interpretation.

Typical outputs include:

- regime label
- sentiment score
- dominant narrative
- confidence
- contradictions
- uncertainty note

This layer answers: **What market frame are we in now?**

### 3. Transmission Layer

This layer maps the current market frame into:

- sector implications
- factor tilt
- leadership pressure
- crosscurrents
- watchlist alignment

This layer answers: **How is the current frame flowing through the market?**

### 4. Scenario Layer

This layer allows users to change one assumption and inspect how the frame may shift.

Example scenarios:

- hot CPI
- dovish Fed
- war escalation
- regulation relief
- stronger AI capex

This layer answers: **What if the world changes from here?**

### 5. Output Layer

InvestorFrame outputs structured results through:

- dashboard views
- reports
- watchlist summaries
- scenario results
- explainable API responses

This layer answers: **Can the system explain itself clearly enough to be useful?**

---

## Pipeline Phases

The orchestrator runs 5 sequential phases, with parallelism within phases:

| Phase | Name             | Parallelism              | Key Components                    |
|-------|------------------|--------------------------|-----------------------------------|
| 1     | Data Collection  | 3 connectors in parallel | FRED, NewsAPI, yfinance           |
| 2     | Event Processing | Sequential               | Parser, Classifier                |
| 3     | Market State     | 2 analyzers in parallel  | Sentiment Analyzer, Regime Detector |
| 4     | Scoring          | Sequential               | Sector Engine, Watchlist Scorer    |
| 5     | Risk & Output    | Sequential               | Risk Gates, Report Generator       |

## Data Flow

```
Raw API responses
  → NewsArticle, EconomicDataPoint, MarketSnapshot    (connector models)
  → Event                                             (parsed + classified)
  → SentimentSignal → AggregateSentiment              (sentiment layer)
  → MarketRegime                                      (regime layer)
  → SectorScore[]                                     (scored + ranked)
  → StockScore[]                                      (watchlist layer)
  → RiskAssessment                                    (validation layer)
  → PipelineResult                                    (frozen output)
```

All intermediate types are Pydantic frozen models defined in `investorframe/core/models.py`. The `PipelineContext` in `investorframe/pipeline/context.py` is the only mutable object, converted to an immutable `PipelineResult` via `to_result()` at pipeline completion.

---

## Configuration Architecture

All scoring rules are externalized in YAML under `config/`:

| File                    | Controls                                      |
|-------------------------|-----------------------------------------------|
| `event_types.yaml`      | Event taxonomy, keyword rules, thresholds     |
| `event_sector_map.yaml` | Which events affect which sectors, with weights |
| `regime_rules.yaml`     | Indicator thresholds for each regime state     |
| `sector_config.yaml`    | Sector ETF metadata and display names         |
| `watchlist.yaml`        | Stock-to-sector mapping with beta values      |
| `scenarios.yaml`        | Predefined what-if scenario templates          |

This means you can tune scoring behavior entirely through config changes without modifying code.

---

## Product Surfaces

InvestorFrame is organized around three main product surfaces.

### Dashboard
A summary interface for:
- world state
- current regime
- dominant narrative
- sector transmission
- watchlist alignment

### Scenario Lab
A sandbox for:
- choosing a scenario
- adjusting severity
- observing regime shifts
- seeing sector and watchlist deltas

### Reports & Explain
A structured layer for:
- market briefs
- scenario summaries
- reasoned explanations
- follow-up interpretation

---

## Persistence

SQLAlchemy with SQLite stores pipeline run history:

- `pipeline_runs` — run metadata (status, duration, event count)
- `regime_records` — detected regime per run
- `sector_scores` — sector scores per run
- `stock_scores` — watchlist scores per run

The database is optional (`--no-db` flag) and used only for historical tracking.

---

## Architectural Principles

### Event-first
InvestorFrame begins with external world changes, not individual tickers.

### Regime-aware
The same event can imply different outcomes under different market states.

### Explainable
All important outputs should expose:
- drivers
- confidence
- risk flags
- uncertainty

### Probabilistic
Outputs are interpretive and probabilistic, not deterministic promises.

### Modular
The system should remain decomposable into:
- input
- framing
- transmission
- scenario
- output

---

## Trust and Risk Considerations

InvestorFrame must preserve user trust by being explicit about:

- uncertainty
- model limitations
- scenario assumptions
- invalidation conditions
- non-advisory use

The system should always prefer a restrained output over false precision.

---

## Long-Term Architecture Direction

Longer term, InvestorFrame may evolve toward:

- richer event memory
- historical frame tracking
- stronger scenario comparison
- report agents
- hosted APIs
- more advanced explanation surfaces

These should be added only if they preserve the project's core identity:

**InvestorFrame helps users frame the market before reacting to it.**
