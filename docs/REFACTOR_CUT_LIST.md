# Refactor cut list

## Deleted on purpose
- api/
- cli/
- examples/
- tests/
- Dockerfile
- LICENSE
- Makefile
- old scenario/dashboard/report surfaces
- sentiment layer
- watchlist scoring layer
- old architecture and roadmap docs
- React Query and Zustand dependency path

## Kept on purpose
- lightweight React app shell
- small Python package
- YAML rules
- static JSON generation path
- Frame / Idea / Review / Rulebook product shape

## Current priority
1. Keep decisions slow and explicit.
2. Keep the runtime surface tiny.
3. Add complexity only after repeated real use demands it.
