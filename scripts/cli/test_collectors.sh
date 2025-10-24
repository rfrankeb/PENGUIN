#!/bin/bash
# Test individual data collectors

# Reddit WSB Collector
echo "Testing Reddit WSB collector..."
python -m penguin.cli.main collectors test reddit_wsb --symbol GME

# Polygon Options Collector
echo "Testing Polygon Options collector..."
python -m penguin.cli.main collectors test polygon_options --symbol GME

# Yahoo Finance Collector
echo "Testing Yahoo Finance collector..."
python -m penguin.cli.main collectors test yahoo_finance --symbol AAPL
