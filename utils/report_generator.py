# utils/report_generator.py
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict

def ensure_dir(p: str | Path):
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_json(report: Dict, out_dir: str | Path, filename: str):
    out = ensure_dir(out_dir) / filename
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return out

def save_markdown(report: Dict, out_dir: str | Path, filename: str):
    out = ensure_dir(out_dir) / filename
    lines = []

    if "career_summary" in report:   # Talent Intelligence Report
        lines.append(f"# Talent Intelligence Report — {report['candidate']['name']}")
        lines.append("")
        c = report["candidate"]
        lines.append(f"- **Role**: {c.get('role','N/A')}")
        lines.append(f"- **Experience (years)**: {c.get('experience_years','N/A')}")
        lines.append("")
        lines.append("## Career Summary")
        lines.append(report["career_summary"])
        lines.append("")
        lines.append("## Detected Skills (with confidence)")
        for skill, conf in report["skills"]:
            lines.append(f"- {skill}: **{conf}**")
        lines.append("")
        lines.append("## Highlights")
        for h in report.get("highlights", []):
            lines.append(f"- {h}")
        lines.append("")
        lines.append("## Notes")
        lines.append(report.get("notes", ""))

    elif "challenges" in report:   # Assessment Report
        lines.append(f"# Assessment Package — {report['candidate']['name']}")
        lines.append("")
        lines.append("## Challenges")
        for ch in report.get("challenges", []):
            lines.append(f"- {ch}")
        lines.append("")
        lines.append("## Evaluation Framework")
        for k, v in report.get("evaluation_framework", {}).items():
            lines.append(f"- {k}: {v}")
        lines.append("")
        lines.append("## Bias Mitigation Protocol")
        for g in report.get("bias_mitigation", []):
            lines.append(f"- {g}")
        lines.append("")
        lines.append("## Notes")
        lines.append(report.get("notes", ""))
    elif "themes" in report:   
        lines.append(f"# Behavioral & Cultural Fit Report — {report['candidate']}")
        lines.append("")
        lines.append("## Detected Themes")
        for k, v in report.get("themes", {}).items():
            lines.append(f"- {k}: {v}")
        lines.append("")
        lines.append("## Summary")
        lines.append(report.get("summary", ""))
        lines.append("")
        lines.append("## Notes")
        lines.append(report.get("notes", ""))
    elif "recommendations" in report:   # Market Intelligence Report
        lines.append(f"# Market Intelligence Report — {report['role']}")
        lines.append("")
        lines.append(f"- **Average Salary**: {report['avg_salary']}")
        lines.append(f"- **Demand Index**: {report['demand_index']}")
        lines.append("")
        lines.append("## Recommendations")
        for r in report.get("recommendations", []):
            lines.append(f"- {r}")
        lines.append("")
        lines.append("## Notes")
        lines.append(report.get("notes", ""))
    

    else:
        lines.append("# Unknown Report Type")
        lines.append(str(report))

    out.write_text("\n".join(lines), encoding="utf-8")
    return out
