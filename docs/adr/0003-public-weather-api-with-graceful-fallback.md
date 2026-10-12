# 3. Public weather API with graceful fallback

## Status
Accepted

## Context
For the "Hack with a public API" challenge, KEEPER needs live data. We want a keyless
service (the repo is public — no secrets) and we must not break the game when offline.

## Decision
Use Open-Meteo (forecast + geocoding). Wrap every call so any failure returns a neutral
`calm` mood instead of raising. Standard library only (`urllib`, `json`).

## Consequences
The game gains a live, surprising opening with no signup and no new dependencies, and it
still works offline. The trade-off: weather is read once at start, not continuously.