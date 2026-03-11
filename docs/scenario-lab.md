# Scenario Lab

The scenario simulator lets you ask "what if?" questions by injecting synthetic events into the pipeline and observing how sector and watchlist scores change.

## How It Works

1. Load a predefined template (or define custom events)
2. The simulator creates synthetic `Event` objects with configured type, direction, and severity
3. These events are fed through the sector scoring engine alongside baseline data
4. The simulator computes deltas: how each sector and stock score changes relative to the current baseline

The scenario does **not** re-run data collection or regime detection. It isolates the scoring impact of hypothetical events.

## Predefined Scenarios

Run `python -m cli.main --list-scenarios` to see all available templates.

### Fed Rate Hike (50bps)

```bash
python -m cli.main --scenario fed_rate_hike_50bps
```

Simulates a 50 basis point rate increase. Typically negative for rate-sensitive sectors (Real Estate, Utilities) and modestly positive for Financials.

### Oil Price Shock

```bash
python -m cli.main --scenario oil_price_shock
```

Simulates crude oil spiking above $120/barrel. Strongly positive for Energy, negative for Consumer Discretionary and Industrials due to input cost pressure.

### China Slowdown

```bash
python -m cli.main --scenario china_slowdown
```

Simulates China GDP growth falling below 4%. Impacts Materials and Industrials most through trade exposure; Technology affected through supply chain concerns.

### Tech Earnings Miss

```bash
python -m cli.main --scenario tech_earnings_miss
```

Simulates major tech companies reporting below expectations. Concentrated impact on Technology and Communication Services sectors.

### Inflation Surge

```bash
python -m cli.main --scenario inflation_surge
```

Simulates CPI accelerating above 6% year-over-year. Broad negative impact, with Consumer Staples and Healthcare showing relative resilience.

### Credit Spread Widening

```bash
python -m cli.main --scenario credit_spread_widening
```

Simulates high-yield spreads widening significantly. Negative for Financials and high-leverage sectors; flight-to-quality benefits Utilities.

### Dollar Strengthening

```bash
python -m cli.main --scenario dollar_strengthening
```

Simulates the USD index rising above 110. Negative for export-heavy sectors (Technology, Materials); relatively neutral for domestic-focused sectors.

### Global Trade Disruption

```bash
python -m cli.main --scenario global_trade_disruption
```

Simulates major supply chain and trade disruptions. Broad negative impact with highest severity; Industrials and Materials most affected.

## Using the API

```bash
curl -X POST http://localhost:8000/api/v1/scenarios \
  -H "Content-Type: application/json" \
  -d '{"scenario_name": "oil_price_shock"}'
```

The response includes:
- `baseline_scores` — current sector scores
- `scenario_scores` — scores with synthetic events injected
- `deltas` — per-sector change (positive = improvement, negative = deterioration)

## Interpreting Results

Scenario deltas show **relative sensitivity**, not absolute predictions.

A delta of +15 for Energy under `oil_price_shock` means: "If this scenario occurs, our model estimates Energy sector scoring would improve by 15 points relative to baseline."

Important caveats:
- Deltas assume all other conditions remain constant
- Real markets have second-order effects not captured here
- The magnitude depends on the configured severity in `config/scenarios.yaml`
- Multiple simultaneous scenarios may interact in ways the model doesn't capture

## Custom Scenarios

Edit `config/scenarios.yaml` to add your own templates:

```yaml
my_custom_scenario:
  name: "My Custom Scenario"
  description: "Description of what this scenario represents"
  events:
    - event_type: "economic"
      subtype: "gdp_report"
      direction: "bearish"
      severity: 4
      headline: "GDP contracts for second consecutive quarter"
```

Then run it:

```bash
python -m cli.main --scenario my_custom_scenario
```
