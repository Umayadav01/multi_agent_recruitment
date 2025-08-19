# main.py
import streamlit as st
import json
from pathlib import Path
from typing import Dict
import pandas as pd
import plotly.express as px

# ---------------- PATHS ----------------
ROOT = Path(".")
REPORTS_DIR = ROOT / "outputs" / "reports"
ASSESSMENTS_DIR = ROOT / "outputs" / "assessments"

# ---------------- HELPERS ----------------
def load_json_files(directory: Path) -> Dict[str, Dict]:
    out = {}
    if not directory.exists():
        return out
    for f in sorted(directory.glob("*.json")):
        try:
            out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
    return out

def aggregate_skills(candidate_reports: Dict[str, Dict]) -> pd.DataFrame:
    rows = []
    for key, rep in candidate_reports.items():
        for skill, conf in rep.get("skills", []):
            rows.append({"candidate": key, "skill": skill, "confidence": float(conf)})
    if not rows:
        return pd.DataFrame(columns=["skill", "count", "avg_conf"])
    df = pd.DataFrame(rows)
    agg = df.groupby("skill").agg(
        count=("candidate", "nunique"),
        avg_conf=("confidence", "mean")
    ).reset_index().sort_values("count", ascending=False)
    return agg

def salary_distribution_df(market_reports: Dict[str, Dict]) -> pd.DataFrame:
    rows = []
    for k, rep in market_reports.items():
        try:
            rows.append({
                "role": rep.get("role", k),
                "avg_salary": float(rep.get("avg_salary", 0)),
                "demand_index": rep.get("demand_index", 0)
            })
        except:
            continue
    return pd.DataFrame(rows)

# ---------------- UI RENDERERS ----------------
def show_candidate(rep: Dict, assessment_reports: Dict, behavioral_reports: Dict):
    c = rep.get("candidate", {})
    st.subheader("👤 Candidate Overview")
    st.write(f"**Name:** {c.get('name','-')}")
    st.write(f"**Role:** {c.get('role','-')}")
    st.write(f"**Experience:** {c.get('experience_years','-')} years")

    st.markdown("### 💡 Career Summary")
    st.write(rep.get("career_summary", "No summary available."))

    st.markdown("### 🛠 Skills")
    for skill, conf in rep.get("skills", []):
        display_conf = float(conf)
        if display_conf > 1:
            display_conf /= 100.0
        st.write(f"- **{skill}** ({conf:.2f})")
        st.progress(min(max(display_conf, 0.0), 1.0))

    st.markdown("### ⭐ Highlights")
    for h in rep.get("highlights", []):
        st.write(f"- {h}")

    # linked assessment
    ass_key = Path(rep.get("_source_file", "")).stem + "_assessment"
    if ass_key in assessment_reports:
        st.divider()
        st.subheader("📝 Assessment Package")
        ass = assessment_reports[ass_key]
        for ch in ass.get("challenges", []):
            st.write(f"- {ch}")
        st.write("**Evaluation Framework**")
        st.json(ass.get("evaluation_framework", {}))
        st.write("**Bias Mitigation**")
        for g in ass.get("bias_mitigation", []):
            st.write(f"- {g}")

    # linked behavioral
    beh_key = Path(rep.get("_source_file", "")).stem + "_behavior"
    if beh_key in behavioral_reports:
        st.divider()
        st.subheader("💬 Behavioral Analysis")
        beh = behavioral_reports[beh_key]
        for k, v in beh.get("themes", {}).items():
            st.write(f"- {k}: {v}")
        st.write("**Summary:**", beh.get("summary", "-"))

def show_market(rep: Dict, market_df: pd.DataFrame):
    st.subheader(f"📊 Market Intelligence — {rep.get('role','-')}")
    st.write(f"- **Average Salary**: {rep.get('avg_salary','-')}")
    st.write(f"- **Demand Index**: {rep.get('demand_index','-')}")
    st.markdown("**Recommendations**")
    for r in rep.get("recommendations", []):
        st.write(f"- {r}")

    # scatter plot of all roles
    if not market_df.empty:
        fig = px.scatter(
            market_df,
            x="avg_salary", y="demand_index",
            text="role", size="demand_index",
            title="Demand vs Salary across roles"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- MAIN APP ----------------
def main():
    st.set_page_config(page_title="Multi-Agent Recruitment Dashboard", layout="wide")
    st.title("🤖 Multi-Agent Recruitment System — Dashboard")

    # load all outputs
    candidate_reports = load_json_files(REPORTS_DIR)
    assessment_reports = load_json_files(ASSESSMENTS_DIR)
    behavioral_reports = load_json_files(REPORTS_DIR / "behavioral")
    market_reports = load_json_files(REPORTS_DIR / "market")

    # sidebar navigation
    st.sidebar.header("Navigation")
    section = st.sidebar.radio(
        "Choose Section:",
        ["📌 Overview", "👤 Candidates", "📊 Market Trends", "📂 Exports / Utilities"]
    )

    if section == "📌 Overview":
        st.header("System Overview")
        st.info("This dashboard visualizes outputs from the multi-agent recruitment pipeline.")
        # metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Candidates", len(candidate_reports))
        col2.metric("Assessments", len(assessment_reports))
        col3.metric("Behavioral Reports", len(behavioral_reports))
        col4.metric("Market Reports", len(market_reports))

        # skill distribution
        skill_df = aggregate_skills(candidate_reports)
        if not skill_df.empty:
            fig = px.bar(skill_df.head(12), x="count", y="skill", orientation="h",
                         title="Top 12 Skills (by candidates)")
            st.plotly_chart(fig, use_container_width=True)

        # salary vs demand
        market_df = salary_distribution_df(market_reports)
        if not market_df.empty:
            fig2 = px.bar(market_df, x="role", y="avg_salary", color="demand_index",
                          title="Salary vs Demand Index")
            st.plotly_chart(fig2, use_container_width=True)

    elif section == "👤 Candidates":
        if not candidate_reports:
            st.warning("No candidate reports found. Run pipeline first.")
            return
        choice = st.selectbox("Select Candidate", sorted(candidate_reports.keys()))
        if choice:
            rep = candidate_reports[choice]
            rep["_source_file"] = str(REPORTS_DIR / f"{choice}.json")
            show_candidate(rep, assessment_reports, behavioral_reports)

    elif section == "📊 Market Trends":
        if not market_reports:
            st.warning("No market reports found.")
            return
        roles = sorted(market_reports.keys())
        choice = st.selectbox("Select Role", roles)
        if choice:
            rep = market_reports[choice]
            market_df = salary_distribution_df(market_reports)
            show_market(rep, market_df)

    else:  # 📂 Exports
        st.header("Exports & Utilities")
        skill_df = aggregate_skills(candidate_reports)
        if not skill_df.empty:
            st.download_button(
                "Download skill-frequency CSV",
                skill_df.to_csv(index=False),
                "skill_frequency.csv",
                "text/csv"
            )
            st.dataframe(skill_df.head(20))
        market_df = salary_distribution_df(market_reports)
        if not market_df.empty:
            st.download_button(
                "Download market CSV",
                market_df.to_csv(index=False),
                "market_data.csv",
                "text/csv"
            )
            st.dataframe(market_df)

        st.markdown("ℹ️ To regenerate outputs after updating `data/`, run locally:")
        st.code("python -m app.main", language="bash")

if __name__ == "__main__":
    main()
