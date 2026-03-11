# Risk Policy

InvestorFrame is a research tool. This document describes how it manages output quality, uncertainty, and the boundaries of its analysis.

## What This Tool Is

- A framework for organizing macro-economic signals into structured views
- A decision-support layer that surfaces regime shifts, sector rotations, and relative positioning
- A research aid for investors who want to systematize their macro monitoring

## What This Tool Is Not

- Not a trading system or signal generator
- Not a substitute for professional financial advice
- Not a predictor of market direction or returns
- Not validated against historical market performance

## Risk Gates

Every pipeline run passes through 6 automated validation checks before output is produced. If any gate fails, the output is flagged with warnings.

### 1. Data Freshness

**Check**: Is any data source older than the configured lookback window?

**Why**: Stale data produces misleading scores. FRED economic releases are monthly; a score based on 30-day-old GDP data should be treated differently than one based on today's VIX.

**Behavior**: Flags which connectors have stale data and how old it is.

### 2. Confidence Floor

**Check**: Are any sector or watchlist scores below the minimum confidence threshold (default: 0.3)?

**Why**: Low-confidence scores may be driven by a single event with poor classification. They should not be treated as reliable signals.

**Behavior**: Lists scores below the floor with their actual confidence values.

### 3. Event Coverage

**Check**: Did the pipeline collect fewer than 5 events?

**Why**: Scores derived from very few events are fragile. A single misclassified event can dominate the output.

**Behavior**: Reports the event count and warns about thin coverage.

### 4. Regime Stability

**Check**: Is the detected regime in a TRANSITION state with low confidence?

**Why**: During regime transitions, sector scoring rules may not apply cleanly. Risk-on and risk-off modifiers could produce contradictory signals.

**Behavior**: Flags the transition state and recommends caution in interpreting sector rankings.

### 5. Connector Failures

**Check**: Did any data connector fail during collection?

**Why**: Partial data means partial analysis. If NewsAPI is down, the sentiment layer has no input, but the pipeline still produces scores from economic data alone.

**Behavior**: Lists failed connectors and their error messages.

### 6. Score Extremes

**Check**: Are any sector scores above |90| on the [-100, +100] scale?

**Why**: Extreme scores often indicate data anomalies rather than genuine market signals. The tanh normalization should compress most scores well below this range.

**Behavior**: Flags extreme scores and suggests manual review.

## Known Limitations

### Model Simplifications

- **Sector mappings are coarse.** A "rate hike" event affects all 11 sectors with fixed weights. Real-world impact depends on magnitude, market expectations, and timing — none of which are modeled.
- **Beta is static.** Watchlist beta values are configured in YAML and don't update with market conditions.
- **No cross-sector dynamics.** The model doesn't capture sector rotation flows (money moving from tech to utilities).
- **Sentiment is surface-level.** Keyword-based sentiment captures direction but not magnitude or context.

### Data Limitations

- **News lag.** Events may be 15-60 minutes old by the time they're processed.
- **Weekend gaps.** No market data is generated on weekends; Monday runs may show stale Friday prices.
- **FRED release schedule.** Economic data points update monthly or quarterly; many scores reflect conditions from weeks ago.
- **No earnings data.** Individual company earnings are not systematically tracked.

### Failure Modes

- **API rate limits.** Heavy usage can exhaust free-tier quotas, producing incomplete runs.
- **Novel event types.** The keyword classifier misses events that don't match any configured pattern. Enable LLM fallback for better coverage.
- **Regime detection lag.** The 5-indicator voting system responds to confirmed data, not leading indicators. Regime changes may be identified 1-2 days after they begin.

## Output Disclaimers

Every report and API response includes this standard disclaimer:

> This analysis is for informational and educational purposes only. It does not constitute investment advice, a recommendation to buy or sell any security, or an offer of any financial product. Past performance does not guarantee future results. The outputs are probabilistic estimates based on simplified models and may be inaccurate. Always consult a qualified financial advisor before making investment decisions.

The disclaimer generator in `investorframe/risk/disclaimers.py` also produces contextual warnings based on which risk gates were triggered during the run.
