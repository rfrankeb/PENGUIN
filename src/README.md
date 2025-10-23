# PENGUIN Source Code

This directory will contain the main PENGUIN application code following the plugin-based architecture defined in `/CLAUDE.md`.

## Planned Structure

```
src/
├── penguin/
│   ├── core/              # Configuration, logging, constants
│   ├── data/              # Data collection & storage
│   │   ├── base.py        # BaseCollector interface
│   │   ├── registry.py    # Plugin registry
│   │   ├── collectors/    # Data source plugins
│   │   └── storage/       # Database models
│   ├── signals/           # Signal detection
│   ├── ai/                # Claude AI integration
│   ├── recommender/       # Recommendation engine
│   ├── api/               # FastAPI REST API
│   └── cli/               # Command-line interface
```

## Status

🚧 **Under Development**

Currently testing proof-of-concepts in `/testing` directory:
- Reddit WSB scraper (validation complete)
- Yahoo Finance scraper (validation complete)

## Next Steps (MVP Phase 1)

1. Implement BaseCollector interface
2. Create plugin registry system
3. Set up databases (PostgreSQL + TimescaleDB)
4. Migrate PoC scripts to plugin architecture
5. Build basic CLI

See `/CLAUDE.md` for complete roadmap.
