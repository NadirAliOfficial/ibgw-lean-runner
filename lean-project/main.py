from QuantConnect import SecurityType
from QuantConnect.Algorithm import QCAlgorithm
from QuantConnect.Securities.Option import OptionRight
import json
import os

class OptionUniverseAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2025, 1, 5)
        self.SetEndDate(2025, 1, 6)
        self.SetCash(100000)

        self.symbol = "SPY"
        option = self.AddOption(self.symbol)

        # Strike range: -10 to +10
        # Expiry range: 0 to 90 days
        option.SetFilter(-10, 10, 0, 90)

        self.result = []

    def OnEndOfAlgorithm(self):
        for sec in self.Securities.Values:
            if sec.Type == SecurityType.Option:
                sid = sec.Symbol.ID
                self.result.append({
                    "symbol": sec.Symbol.Value,
                    "expiry": sid.Date.strftime("%Y-%m-%d"),
                    "strike": float(sid.StrikePrice),
                    "right": sid.OptionRight.name
                })

        # Save inside the project's /output directory
        output_path = os.path.join(self.AlgorithmId, "output", "spy_options_raw.json")

        # But inside Docker the real working dir is /Lean/Launcher/bin
        # so we use relative folder "output"
        with open("output/spy_options_raw.json", "w") as f:
            json.dump(self.result, f, indent=2)
