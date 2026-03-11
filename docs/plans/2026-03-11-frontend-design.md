# InvestorFrame Frontend Design

**Date**: 2026-03-11
**Status**: Approved, implementing

## Summary

React + Vite + TypeScript frontend with two core pages: Dashboard and Scenario Lab.
Located in `dashboard/` directory. Dark theme, research-terminal aesthetic.

## Tech Stack

React 19, Vite, TypeScript, Tailwind CSS, shadcn/ui, Recharts, TanStack Query, Zustand

## Pages

- `/` — Dashboard: regime, narrative, sector transmission, watchlist snapshot
- `/scenario` — Scenario Lab: template-based what-if simulations

## API

Builds against existing FastAPI backend (`/api/v1/*`).
Phase 1 uses mock data. Phase 2 connects real API with transform layer.

## Key Decisions

1. Build against real backend API shape (`/api/v1/market`, `/api/v1/sectors`, etc.)
2. Frontend lives in `dashboard/`
3. Scenario Lab uses template picker (8 predefined scenarios)
4. Dark theme, professional research-product aesthetic
5. Phase 1: mock data → Phase 2: live API → Phase 3: drawers + polish
