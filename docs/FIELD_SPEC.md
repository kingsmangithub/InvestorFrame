# InvestorFrame Lean Field Specification

## Core principle
Only store fields that directly improve decisions, reviews, or rule enforcement.

## `frame.json`
- `date` — ISO date string
- `frame.label` — `risk_on | mixed | risk_off`
- `frame.confidence` — number from `0` to `1`
- `frame.dominant_pressure` — one sentence
- `frame.caution` — one sentence
- `frame.action_bias` — one sentence
- `questions[]` — 2 to 5 review prompts

## `ideas.json`
Each item is one idea card.
- `ticker`
- `company`
- `action` — `buy | wait | pass | trim | sell`
- `business_summary`
- `bull_case[]` — 2 to 5 points
- `bear_case[]` — 1 to 5 points
- `assumptions[]`
- `invalidation[]`
- `buy_conditions[]`
- `sell_conditions[]`

## `behavior.json`
- `checks[]` — the decision gate
- `default_action` — should stay `no_action_if_any_check_fails`

## `reviews.json`
Each item is one completed review.
- `date`
- `ticker`
- `result`
- `thesis_quality` — integer `1..10`
- `process_quality` — integer `1..10`
- `emotional_discipline` — integer `1..10`
- `lesson`

## `rulebook.json`
- `principles[]`
- `behavior_gate[]`
- `sell_rules[]`
- `wisdom.mistake_patterns[]`
- `wisdom.good_patterns[]`

## Required writing rules
- One idea card per company
- Every idea must include anti-thesis through `bear_case`
- Every idea must include invalidation conditions
- Every idea must include sell conditions before capital is committed
- Reviews are mandatory after meaningful decisions, not optional journaling
