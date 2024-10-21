
# IBGW + LEAN Option Universe Service  
A lightweight, automated system that:

- Pulls the complete options universe for a target underlying (e.g., SPY) via **QuantConnect LEAN**
- Validates all contracts via **Interactive Brokers Gateway (IBGW)**
- Outputs clean, tradable, filtered contracts to CSV/JSON
- Runs locally on Windows/macOS (Docker required for LEAN)
- Supports automation, scheduled execution, and Git-based auto-deploy

---

# 📦 Folder Structure

```

ibgw-lean-runner/
│
├── lean.json                    # Local LEAN environment config
├── data/                        # Empty data folder required by LEAN
│
├── lean-project/                # LEAN algorithm (Option Universe Extractor)
│   ├── main.py
│   ├── config.json
│   └── output/                  # LEAN will write raw option universe here
│
├── main.py                      # IBKR validator (verifies contracts)
├── config.yaml                  # Custom settings (optional)
└── venv/                        # Python virtual environment

```

---

# 🚀 Requirements

## 1. Python Environment
```

python3 -m venv venv
source venv/bin/activate   (mac/linux)
venv\Scripts\activate      (windows)

```

Install dependencies:
```

pip install ib-insync pandas pyyaml python-dateutil pytz
pip install lean quantconnect-stubs

```

## 2. Docker Desktop  *(Mandatory for LEAN CLI)*
Download & install:
https://www.docker.com/products/docker-desktop/

Start Docker and ensure it shows:
**Docker Engine is running**

## 3. IB Gateway (IBGW)
Download from Interactive Brokers:
https://www.interactivebrokers.com/en/trading/ibgateway.php

Run IBGW with:
- Correct login (Paper recommended)
- Market Data enabled
- API access enabled (`Configure → API → Settings → Enable ActiveX and Socket Clients`)

Default connection:
```

Host: 127.0.0.1
Port: 7497
Client ID: 7 (configurable)

````

---

# 🧩 LEAN Configuration

A minimal `lean.json` is included:

```json
{
    "organization-id": 0,
    "project-id": 0,
    "data-directory": "data",
    "python-venv": "venv",
    "environment": "local",
    "ibkr-data": false,
    "auto-update": false,
    "engine-config": {
        "algorithm-language": "Python"
    }
}
````

The `data/` folder may remain empty — LEAN needs the directory, not actual historical data.

---

# 📘 LEAN Algorithm (Option Universe Extraction)

Located at:

```
lean-project/main.py
```

This algorithm:

* Loads target underlying (SPY)
* Builds complete options universe
* Filters expiries & strikes: `(-10, +10)` and `(0–90 days)`
* Writes output to:

```
lean-project/output/spy_options_raw.json
```

---

# ▶️ Running the System

## STEP 1 — Generate the raw options universe (LEAN)

Run from the **root folder**:

```
lean backtest lean-project --lean-config lean.json
```

If Docker is running, LEAN will produce:

```
lean-project/output/spy_options_raw.json
```

---

## STEP 2 — Validate contracts using IBKR (IB Gateway must be running)

```
python main.py
```

This script:

* Connects to IBGW
* Validates each contract with `reqContractDetails`
* Removes invalid/expired/delisted contracts
* Outputs final files:

```
validated_spy_options.json
validated_spy_options.csv
```

---

# 📄 Validation Output Format

Each contract follows:

```json
{
  "symbol": "SPY",
  "expiry": "2025-02-14",
  "strike": 480.0,
  "right": "Call"
}
```

---

# 🔧 Configuration (Optional)

`config.yaml` controls:

```
symbol: SPY

filters:
  expiry_days_min: 0
  expiry_days_max: 90
  strike_range: 10
  rights: ["C", "P"]

paths:
  output_json: "validated_spy_options.json"
  output_csv: "validated_spy_options.csv"

ibkr:
  host: "127.0.0.1"
  port: 7497
  client_id: 7
```

---

# 💡 Automation (Optional)

### Scheduled Task / Windows Service

You may configure the mini-PC to:

1. Run LEAN backtest daily
2. Run validator after LEAN
3. Sync results to Git or local folder

Example chain:

```
lean backtest lean-project --lean-config lean.json
python main.py
```

---

# 🧪 Troubleshooting

### **LEAN says: "Docker not running"**

Start Docker Desktop.

### **LEAN says: "Project not found"**

Run command from repo root.

### **IBKR validation returns 0 contracts**

IBGW might not be connected or market data might be restricted.

### **RAW file not generated**

Check that:

```
lean-project/output/
```

exists.

---

# 🏁 Summary

This service provides:

* Full option universe extraction via LEAN
* Full verification via IBKR
* Local offline backtesting
* Clean outputs for downstream bots/analysis
* Ready automation for Windows mini-PC

If you need further extensions (multiple underlyings, logs, metrics, retry logic), they can be added easily.
<!-- updated: 2024-10-21-r01 -->
