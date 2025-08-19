
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List
import re
from utils.report_generator import ensure_dir, save_json, save_markdown

POSITIVE_KEYWORDS = ["team", "collaborate", "help", "together", "support"]
PROBLEM_SOLVING_KEYWORDS = ["solve", "problem", "fix", "analyze", "improve"]
COMMUNICATION_KEYWORDS = ["communicate", "explain", "share", "talk", "present"]

class BehavioralAnalyzer:
    def __init__(self, conv_path: str | Path = "data/conversations.json",
                 out_dir: str | Path = "outputs/reports/behavioral"):
        self.conv_path = Path(conv_path)
        self.out_dir = ensure_dir(out_dir)

    def _extract_themes(self, conversation: List[str]) -> Dict[str, int]:
        text = " ".join(conversation).lower()
        return {
            "Collaboration": sum(1 for k in POSITIVE_KEYWORDS if k in text),
            "Problem-Solving": sum(1 for k in PROBLEM_SOLVING_KEYWORDS if k in text),
            "Communication": sum(1 for k in COMMUNICATION_KEYWORDS if k in text),
        }

    def _soft_skill_summary(self, themes: Dict[str, int]) -> str:
        strengths = [k for k, v in themes.items() if v > 0]
        if not strengths:
            return "No strong soft skills detected in limited conversation sample."
        return f"Candidate demonstrates strengths in: {', '.join(strengths)}."

    def build_report(self, conv: Dict) -> Dict:
        themes = self._extract_themes(conv["conversation"])
        report = {
            "candidate": conv["candidate"],
            "themes": themes,
            "summary": self._soft_skill_summary(themes),
            "notes": "Behavioral analysis performed on synthetic conversation data."
        }
        return report

    def run(self) -> List[Dict]:
        data = json.loads(Path(self.conv_path).read_text(encoding="utf-8"))
        reports = []
        for conv in data:
            rep = self.build_report(conv)
            fname_safe = conv["candidate"].replace(" ", "_")
            save_json(rep, self.out_dir, f"{fname_safe}_behavior.json")
            save_markdown(rep, self.out_dir, f"{fname_safe}_behavior.md")
            reports.append(rep)
        return reports

if __name__ == "__main__":
    analyzer = BehavioralAnalyzer()
    out = analyzer.run()
    print(f"Generated {len(out)} behavioral reports in outputs/reports/behavioral/")
