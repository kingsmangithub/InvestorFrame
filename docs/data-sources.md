# Data Sources

InvestorFrame pulls from three external APIs and one optional LLM service. All connections are read-only.

## FRED (Federal Reserve Economic Data)

- **Connector**: `investorframe/connectors/fred.py`
- **Auth**: API key (free at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html))
- **Rate limit**: 120 requests/minute

### Series Used

| Series ID  | Description                    | Update Frequency |
|------------|--------------------------------|------------------|
| UNRATE     | Unemployment rate              | Monthly          |
| CPIAUCSL   | Consumer Price Index           | Monthly          |
| GDP        | Gross Domestic Product         | Quarterly        |
| FEDFUNDS   | Federal funds effective rate    | Daily            |
| T10Y2Y     | 10-Year minus 2-Year spread   | Daily            |
| UMCSENT    | Consumer Sentiment (UMich)     | Monthly          |
| INDPRO     | Industrial Production Index    | Monthly          |
| RSAFS      | Retail Sales                   | Monthly          |

### How Data Becomes Events

The event parser compares current values to historical baselines. When a data point crosses a configured threshold (defined in `config/event_types.yaml`), it generates an `Event` with appropriate type, subtype, and severity.

Example: If CPI month-over-month exceeds 0.3%, an `inflation_data` event is created with severity proportional to the deviation.

## NewsAPI

- **Connector**: `investorframe/connectors/news.py`
- **Auth**: API key (free tier at [newsapi.org](https://newsapi.org/register))
- **Rate limit**: 100 requests/day (free), 250K/month (paid)

### Query Strategy

The connector searches for market-relevant topics using curated query terms:

```
"Federal Reserve" OR "interest rates" OR "inflation" OR "GDP" OR
"unemployment" OR "trade war" OR "oil prices" OR "earnings" OR
"stock market" OR "recession" OR "economic growth"
```

Results are deduplicated by title similarity and filtered to the configured lookback window (default: 7 days).

### Limitations

- Free tier returns headlines only (no full article text)
- Results may lag real-time by 15-60 minutes
- Weekend/holiday coverage is reduced
- Source bias is not corrected for

## yfinance (Yahoo Finance)

- **Connector**: `investorframe/connectors/market.py`
- **Auth**: None required
- **Rate limit**: Unofficial, approximately 2000 requests/hour

### Data Pulled

| Category       | Tickers                                      |
|----------------|----------------------------------------------|
| Indices        | ^GSPC (S&P 500), ^VIX                       |
| Sector ETFs    | XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLRE, XLU, XLC |
| Watchlist      | Configured in `config/watchlist.yaml`         |

### Data Points per Ticker

- Current price, previous close, day change %
- 50-day and 200-day moving averages (when available)
- VIX level (for regime detection)
- Sector ETF prices (for breadth calculation)

### Limitations

- Data may be delayed 15-20 minutes during market hours
- Extended hours data is not captured
- Splits and dividends can cause temporary anomalies
- API is unofficial and may change without notice

## OpenAI (Optional)

- **Connector**: `investorframe/connectors/llm.py`
- **Auth**: API key ([platform.openai.com](https://platform.openai.com/api-keys))
- **Model**: GPT-4o-mini (configurable)
- **Disabled by default**: Set `INVESTORFRAME_ENABLE_LLM=true` to activate

### Use Cases

1. **Event classification fallback** — When keyword rules don't match, the LLM classifies event type and subtype
2. **Sentiment enrichment** — More nuanced sentiment scoring than keyword counting
3. **Explanation generation** — Natural language explanations for sector and watchlist scores

### Cost Considerations

With GPT-4o-mini at typical usage (50-100 events per run):
- Classification: ~$0.01-0.03 per run
- Sentiment: ~$0.02-0.05 per run
- Explanations: ~$0.01-0.02 per run

The keyword-based pipeline works well without LLM. Enable it when you want richer explanations or better handling of novel event types.
