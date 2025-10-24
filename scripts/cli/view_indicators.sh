#!/bin/bash
# View technical indicators for stocks

SYMBOL=${1:-"AAPL"}

echo "Viewing indicators for $SYMBOL..."
python view_indicators.py "$SYMBOL"
