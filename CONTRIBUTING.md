# Contributing to InvestorFrame

Thanks for your interest in contributing to **InvestorFrame**.

InvestorFrame is an event-driven market intelligence project focused on:

- macro signals
- regime detection
- sector transmission
- watchlist analysis
- scenario simulation
- explainable market interpretation

This project is still evolving, so contributions that improve clarity, reliability, developer experience, and product quality are especially welcome.

---

## Before You Contribute

Please keep the project philosophy in mind:

- **event-first, not ticker-first**
- **research-first, not hype-first**
- **explainable, not black-box**
- **probabilistic, not deterministic**
- **not investment advice**
- **not an automated trading system**

If a contribution pushes the product toward overclaiming, opaque outputs, or "AI stock picker" behavior, it is unlikely to be accepted.

---

## Ways to Contribute

You can contribute by helping with:

- bug fixes
- code cleanup and refactoring
- tests
- docs and examples
- frontend polish
- developer tooling
- scenario templates
- better risk and uncertainty handling
- data model consistency
- API contract improvements

---

## Development Setup

### 1. Fork the repository

Create your own fork and clone it locally.

### 2. Create a branch

Use a focused branch name, for example:

- `fix/market-panel-loading`
- `feat/scenario-export`
- `docs/readme-improvements`
- `refactor/rule-engine`

### 3. Install dependencies

Follow the repository setup instructions in `README.md`.

### 4. Configure environment

Copy the example environment file:

```bash
cp .env.example .env
```

Use demo or mock settings if you do not have external API keys.

### 5. Run the project

Use the documented local run steps for:

- API
- dashboard
- tests
- demo flows

---

## Code Style

Please keep code:

- readable
- typed where appropriate
- modular
- lightly commented
- consistent with the existing naming patterns

Prefer:

- small focused functions
- predictable data shapes
- clear model naming
- explicit uncertainty and risk fields in outputs

Avoid:

- giant multi-purpose functions
- overly clever abstractions
- hype-driven naming
- hidden side effects
- mixing domain logic and UI logic in the same place

---

## Frontend Contributions

For UI work, keep the product tone:

- calm
- structured
- research-oriented
- dark, premium, high-signal
- not noisy
- not trading-app-like
- not crypto-casino aesthetics

When in doubt, optimize for readability and explanation.

---

## Backend Contributions

For backend work, prioritize:

- stable schemas
- explainable outputs
- risk flags
- uncertainty notes
- graceful fallbacks
- clear API contracts

Please avoid introducing outputs that imply certainty where only probability is warranted.

---

## Tests

If you add or change behavior, add or update tests whenever practical.

At minimum, try to ensure:

- the app still starts
- core routes still return valid shapes
- schemas stay consistent
- scenario outputs remain structured
- no obvious regressions are introduced

---

## Pull Requests

When submitting a pull request:

1. Keep the scope focused
2. Explain what changed
3. Explain why it changed
4. Mention any risks or tradeoffs
5. Include screenshots for UI changes
6. Include example request/response shapes for API changes

A strong PR description usually includes:

- summary
- motivation
- screenshots or sample outputs
- testing notes
- follow-up ideas

### PR Review Criteria

Contributions are more likely to be accepted if they improve one or more of these:

- correctness
- clarity
- explainability
- maintainability
- developer experience
- user trust
- product coherence

---

## Good First Contribution Ideas

If you want a practical place to start, try one of these:

- improve README examples
- add example scenario outputs
- refine empty/loading/error states
- add docs for one API route
- improve risk flag wording
- add a test for one core service
- polish one dashboard panel
- add one scenario template

---

## Questions

If something is unclear, open an issue describing:

- what you want to contribute
- what part of the project it affects
- any assumptions you are making

Thanks for helping improve InvestorFrame.
