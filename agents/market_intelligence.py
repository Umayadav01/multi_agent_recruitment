from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List
from utils.report_generator import ensure_dir, save_json, save_markdown

class MarketIntelligence:
    def __init__(self, data_path: str | Path = "data/market_data.json",
                 out_dir: str | Path = "outputs/reports/market"):
        self.data_path = Path(data_path)
        self.out_dir = ensure_dir(out_dir)

    def analyze_market(self, entry: Dict) -> Dict:
        role = entry["role"]
        demand = entry["demand_index"]
        salary = entry["avg_salary"]
        sources = entry["top_sources"]

        recs = []
        if demand > 7:
            recs.append(f"⚡ {role} is in very high demand. Prioritize sourcing immediately.")
        elif demand < 4:
            recs.append(f"📉 Demand for {role} is currently low; maintain a passive sourcing strategy.")
        else:
            recs.append(f"↔️ Demand for {role} is moderate; continue sourcing steadily.")

        if salary > 120000:
            recs.append(f"💰 Salaries for {role} are above average; budget carefully.")
        elif salary < 70000:
            recs.append(f"💡 Salaries for {role} are relatively low; good cost-effective hiring opportunity.")

        recs.append(f"Recommended sourcing channels: {', '.join(sources)}")

        return {
            "role": role,
            "avg_salary": salary,
            "demand_index": demand,
            "recommendations": recs,
            "notes": "Market analysis performed on synthetic data."
        }

    def run(self) -> List[Dict]:
        data = json.loads(self.data_path.read_text(encoding="utf-8"))
        reports = []
        for entry in data:
            rep = self.analyze_market(entry)
            fname_safe = entry["role"].replace(" ", "_")
            save_json(rep, self.out_dir, f"{fname_safe}_market.json")
            save_markdown(rep, self.out_dir, f"{fname_safe}_market.md")
            reports.append(rep)
        return reports

if __name__ == "__main__":
    analyzer = MarketIntelligence()
    out = analyzer.run()
    print(f"Generated {len(out)} market intelligence reports in outputs/reports/market/")
