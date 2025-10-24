#!/bin/bash
# List all available data collectors

echo "Listing all registered collectors..."
python -m penguin.cli.main collectors list
