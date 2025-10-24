# CLI Shell Scripts

Quick-access shell scripts for common PENGUIN operations.

## Available Scripts

### 🔧 Setup & Configuration

**`setup_env.sh`** - Initial environment setup
```bash
./scripts/cli/setup_env.sh
```
- Creates virtual environment
- Installs all dependencies
- Sets up development environment

---

### 📋 List & Discovery

**`list_collectors.sh`** - Show all registered collectors
```bash
./scripts/cli/list_collectors.sh
```
Output:
```
Registered collector: yahoo_finance
Registered collector: polygon_options
Registered collector: reddit_wsb
```

---

### 🧪 Testing

**`test_collectors.sh`** - Test all collectors at once
```bash
./scripts/cli/test_collectors.sh
```
Tests:
- Reddit WSB collector (GME)
- Polygon Options collector (GME)
- Yahoo Finance collector (AAPL)

---

### 📊 Data Collection

**`collect_data.sh`** - Collect data from all sources
```bash
# Use default symbols (GME, AMC, AAPL, TSLA)
./scripts/cli/collect_data.sh

# Custom symbols
./scripts/cli/collect_data.sh "NVDA,MSFT,GOOGL,AMZN"
```

Collects from:
- Reddit WSB
- Yahoo Finance
- Polygon Options (if API key configured)

---

### 📈 Analysis

**`view_indicators.sh`** - View technical indicators for a stock
```bash
./scripts/cli/view_indicators.sh AAPL
```

Shows 98+ technical indicators for the specified symbol.

---

## Making Scripts Executable

If you get a "permission denied" error, make the scripts executable:

```bash
chmod +x scripts/cli/*.sh
```

---

## Direct Python Alternative

If you prefer the full Python command format:

```bash
# Instead of: ./scripts/cli/test_collectors.sh
# Use:
python -m penguin.cli.main collectors test reddit_wsb --symbol GME
python -m penguin.cli.main collectors test polygon_options --symbol GME
python -m penguin.cli.main collectors test yahoo_finance --symbol AAPL
```

Both methods work identically - scripts are just shortcuts!

---

## Adding Your Own Scripts

1. Create a new `.sh` file in this directory
2. Add shebang: `#!/bin/bash`
3. Write your commands
4. Make executable: `chmod +x your_script.sh`
5. Run: `./scripts/cli/your_script.sh`

### Example Custom Script

```bash
#!/bin/bash
# Monitor GME all day

SYMBOL=${1:-"GME"}

while true; do
    echo "Collecting data for $SYMBOL..."
    python -m penguin.cli.main collectors run yahoo_finance --symbols "$SYMBOL"
    python -m penguin.cli.main collectors run reddit_wsb --symbols "$SYMBOL"

    echo "Waiting 5 minutes..."
    sleep 300  # 5 minutes
done
```

Save as `monitor_stock.sh`, then run:
```bash
./scripts/cli/monitor_stock.sh GME
```

---

## Troubleshooting

### Script not found
```bash
# Make sure you're in the PENGUIN root directory
cd ~/Desktop/Niche/PENGUIN

# Then run with relative path
./scripts/cli/test_collectors.sh
```

### Permission denied
```bash
chmod +x scripts/cli/*.sh
```

### Module not found
```bash
# Activate virtual environment first
source venv/bin/activate

# Then run script
./scripts/cli/test_collectors.sh
```

---

For more commands and detailed usage, see: **`QUICK_REFERENCE.md`** in the project root.
