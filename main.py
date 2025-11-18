from ib_insync import IB, Option
import json
import pandas as pd
import time

# Path to LEAN output
INPUT_FILE = "lean-project/output/spy_options_raw.json"

# Output files
OUTPUT_JSON = "validated_spy_options.json"
OUTPUT_CSV = "validated_spy_options.csv"

ib = IB()

def connect_ibkr():
    while True:
        try:
            print("Connecting to IB Gateway...")
            ib.connect("127.0.0.1", 7497, clientId=7)
            print("Connected!")
            return
        except Exception as e:
            print("Connection failed, retrying...", e)
            time.sleep(2)

def validate_contracts(contracts):
    validated = []
    print(f"Validating {len(contracts)} contracts...")
    
    for c in contracts:
        try:
            opt = Option(
                symbol=c["symbol"],
                lastTradeDateOrContractMonth=c["expiry"],
                strike=c["strike"],
                right=c["right"][0],  # "C" or "P"
                exchange="SMART"
            )

            details = ib.reqContractDetails(opt)

            if details:
                validated.append(c)
        except Exception:
            continue

    return validated


def main():
    # Load LEAN output
    with open(INPUT_FILE) as f:
        raw = json.load(f)

    connect_ibkr()

    validated = validate_contracts(raw)

    # save JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(validated, f, indent=2)

    # save CSV
    pd.DataFrame(validated).to_csv(OUTPUT_CSV, index=False)

    print(f"Validation complete. Valid contracts: {len(validated)}")


if __name__ == "__main__":
    main()
