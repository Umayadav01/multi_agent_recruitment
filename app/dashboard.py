import streamlit as st
import json
from pathlib import Path
from typing import Dict, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Paths
ROOT = Path(".")
REPORTS_DIR = ROOT / "outputs" / "reports"
ASSESSMENTS_DIR = ROOT / "outputs" / "assessments"

# Utility loaders
def load_json_files(directory: Path) -> Dict[str, Dict]:
    out = {}
    if not directory.exists():
        return out
    for f in sorted(directory.glob("*.json")):
        try:
            out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            # ignore bad files
            continue
    return out

def safe_get(d: Dict, key: str, default=None):
    return d.get(key, default)

# Data aggregation helpers
def aggregate_skill_frequency(candidate_reports: Dict[str, Dict]) -> pd.DataFrame:
    rows = []
    for key, rep in candidate_reports.items():
        for skill, conf in rep.get("skills", []):
            rows.append({"candidate": key, "skill": skill, "confidence": conf})
    if not rows:
        return pd.DataFrame(columns=["skill", "count", "avg_confidence"])
    df = pd.DataFrame(rows)
    agg = df.groupby("skill").agg(count=("candidate", "nunique"), avg_confidence=("confidence", "mean")).reset_index()
    agg = agg.sort_values("count", ascending=False)
    return agg

def salary_distribution_df(market_reports: Dict[str, Dict]) -> pd.DataFrame:
    rows = []
    for k, rep in market_reports.items():
        try:
            rows.append({"role": rep.get("role", k), "avg_salary": float(rep.get("avg_salary", 0)), "demand_index": rep.get("demand_index", 0)})
        except:
            continue
    if not rows:
        return pd.DataFrame(columns=["role", "avg_salary", "demand_index"])
    return pd.DataFrame(rows)

# Visual helpers (matplotlib only)
def plot_skill_bar(df: pd.DataFrame):
    if df.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No skill data available", ha="center", va="center")
        ax.axis("off")
        return fig
    fig, ax = plt.subplots(figsize=(8, 4))
    top = df.head(12)
    ax.barh(top["skill"][::-1], top["count"][::-1])
    ax.set_xlabel("Number of Candidates")
    ax.set_title("Top Skills (by number of candidates)")
    plt.tight_layout()
    return fig

def plot_salary_box(df: pd.DataFrame):
    if df.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No market data available", ha="center", va="center")
        ax.axis("off")
        return fig
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(df["avg_salary"].dropna().values, vert=False)
    ax.set_yticks([1])
    ax.set_yticklabels(["avg_salary"])
    ax.set_title("Salary distribution (avg_salary)")
    plt.tight_layout()
    return fig

def plot_demand_bar(df: pd.DataFrame):
    if df.empty:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No market data available", ha="center", va="center")
        ax.axis("off")
        return fig
    fig, ax = plt.subplots(figsize=(8, 4))
    ord_df = df.sort_values("demand_index", ascending=False)
    ax.bar(ord_df["role"], ord_df["demand_index"])
    ax.set_ylabel("Demand Index")
    ax.set_title("Demand Index by Role")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig

# Render functions
def show_candidate_overview(report: Dict):
    c = report["candidate"]
    st.subheader("📌 Candidate Overview")
    st.markdown(f"**Name:** {c.get('name','-')}  \n**Role:** {c.get('role','-')}  \n**Experience:** {c.get('experience_years','-')} years")

    st.subheader("💡 Career Summary")
    st.write(report.get("career_summary", "No summary available."))

    st.subheader("🛠 Skills (with confidence)")
    skills = report.get("skills", [])
    if not skills:
        st.write("No skills detected.")
    else:
        for skill, conf in skills:
            # progress takes 0..1, our conf is 0..1 or 0..100; ensure scale
            display_conf = float(conf)
            if display_conf > 1:
                display_conf = display_conf / 100.0
            st.write(f"- **{skill}** — confidence: {conf}")
            st.progress(min(max(display_conf, 0.0), 1.0))

    st.subheader("⭐ Highlights")
    for h in report.get("highlights", []):
        st.write(f"- {h}")

def show_assessment(assessment: Dict):
    st.subheader("📝 Assessment Package")
    for ch in assessment.get("challenges", []):
        st.write(f"- {ch}")
    st.write("**Evaluation Framework**")
    for k, v in assessment.get("evaluation_framework", {}).items():
        st.write(f"- {k}: {v}")
    st.write("**Bias Mitigation**")
    for g in assessment.get("bias_mitigation", []):
        st.write(f"- {g}")

def show_behavioral(beh: Dict):
    st.subheader("💬 Behavioral & Cultural Fit")
    themes = beh.get("themes", {})
    if themes:
        for k, v in themes.items():
            st.write(f"- {k}: {v}")
    st.write("**Summary**")
    st.write(beh.get("summary", "-"))

def show_market(rep: Dict):
    st.subheader(f"📊 Market Intelligence — {rep.get('role','-')}")
    st.write(f"- **Average Salary**: {rep.get('avg_salary','-')}")
    st.write(f"- **Demand Index**: {rep.get('demand_index','-')}")
    st.write("**Recommendations**")
    for r in rep.get("recommendations", []):
        st.write(f"- {r}")

# Main layout
def main():
    st.set_page_config(page_title="Multi-Agent Recruitment Dashboard", layout="wide")
    st.title("🤖 Multi-Agent Recruitment System — Dashboard")

    # Load data
    candidate_reports = load_json_files(REPORTS_DIR)
    assessment_reports = load_json_files(ASSESSMENTS_DIR)
    behavioral_reports = load_json_files(REPORTS_DIR / "behavioral")
    market_reports = load_json_files(REPORTS_DIR / "market")

    # Sidebar
    st.sidebar.header("Navigation")
    section = st.sidebar.radio("Choose Section:", ["Overview", "Candidates", "Market Trends", "Exports / Utilities"])

    if section == "Overview":
        st.header("Platform Overview")
        st.markdown("This dashboard visualizes outputs from the multi-agent recruitment pipeline.")
        # aggregated visuals
        skill_df = aggregate_skill_frequency(candidate_reports)
        st.subheader("Top Skills")
        st.pyplot(plot_skill_bar(skill_df))

        market_df = salary_distribution_df(market_reports)
        st.subheader("Salary distribution")
        st.pyplot(plot_salary_box(market_df))

        st.subheader("Demand by Role")
        st.pyplot(plot_demand_bar(market_df))

        # Quick stats
        left, right = st.columns(2)
        with left:
            st.metric("Candidates (profiles)", len(candidate_reports))
            st.metric("Assessments generated", len(assessment_reports))
        with right:
            st.metric("Behavioral reports", len(behavioral_reports))
            st.metric("Market reports", len(market_reports))

    elif section == "Candidates":
        st.header("Candidate Explorer")
        if not candidate_reports:
            st.warning("No candidate reports found. Run the pipeline (app.main) first.")
            return

        candidates = sorted(candidate_reports.keys())
        choice = st.selectbox("Select Candidate:", candidates)

        if choice:
            rep = candidate_reports[choice]
            show_candidate_overview(rep)

            st.divider()
            # assessment
            ass_key = choice + "_assessment"
            if ass_key in assessment_reports:
                show_assessment(assessment_reports[ass_key])
            else:
                st.info("No assessment package found for this candidate.")

            st.divider()
            beh_key = choice + "_behavior"
            if beh_key in behavioral_reports:
                show_behavioral(behavioral_reports[beh_key])
            else:
                st.info("No behavioral report found for this candidate.")

            st.divider()
            # Download candidate report as JSON
            st.download_button("Download candidate JSON", json.dumps(rep, indent=2), file_name=f"{choice}.json", mime="application/json")

    elif section == "Market Trends":
        st.header("Market Intelligence")
        if not market_reports:
            st.warning("No market reports found. Run the pipeline (app.main) first.")
            return

        # Show all markets with small cards and charts
        roles = sorted(market_reports.keys())
        sel_role = st.selectbox("Select Role:", roles)

        if sel_role:
            rep = market_reports[sel_role]
            show_market(rep)
            # show demand and salary visuals for all roles
            market_df = salary_distribution_df(market_reports)
            st.subheader("All roles: demand vs salary")
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.scatter(market_df["avg_salary"], market_df["demand_index"])
            for i, txt in enumerate(market_df["role"].tolist()):
                ax.annotate(txt, (market_df["avg_salary"].iat[i], market_df["demand_index"].iat[i]))
            ax.set_xlabel("Average Salary")
            ax.set_ylabel("Demand Index")
            plt.tight_layout()
            st.pyplot(fig)

    else:  # Exports / Utilities
        st.header("Exports & Utilities")
        st.markdown("Download aggregated data or regenerate pipeline outputs from the server (run `python -m app.main`).")

        # aggregated CSVs
        skill_df = aggregate_skill_frequency(candidate_reports)
        if not skill_df.empty:
            st.download_button("Download skill-frequency CSV", skill_df.to_csv(index=False), file_name="skill_frequency.csv", mime="text/csv")
            st.write(skill_df.head(20))
        else:
            st.write("No aggregated skill data available.")

        market_df = salary_distribution_df(market_reports)
        if not market_df.empty:
            st.download_button("Download market CSV", market_df.to_csv(index=False), file_name="market_data.csv", mime="text/csv")
            st.write(market_df)
        else:
            st.write("No market data available.")

        #quick action: run pipeline (ui hint)
        st.markdown("If you update `data/` and want to recreate outputs, run pipeline in terminal:")
        st.code("python -m app.main", language="bash")

if __name__ == "__main__":
    main()
