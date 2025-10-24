#!/bin/bash
# Collect data from various sources

# Default symbols if not provided
SYMBOLS=${1:-"GME,AMC,AAPL,TSLA"}

echo "Collecting data for symbols: $SYMBOLS"

# Collect from Reddit WSB
echo "Collecting from Reddit WSB..."
python -m penguin.cli.main collectors run reddit_wsb --symbols "$SYMBOLS"

# Collect from Yahoo Finance
echo "Collecting from Yahoo Finance..."
python -m penguin.cli.main collectors run yahoo_finance --symbols "$SYMBOLS"

# Collect from Polygon Options (if API key configured)
echo "Collecting from Polygon Options..."
python -m penguin.cli.main collectors run polygon_options --symbols "$SYMBOLS"
