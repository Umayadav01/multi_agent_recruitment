# app/main.py
import streamlit as st
from agents.candidate_profiler import CandidateProfiler
from agents.assessment_designer import AssessmentDesigner
from agents.behavioral_analyzer import BehavioralAnalyzer
from agents.market_intelligence import MarketIntelligence
from utils.pdf_generator import candidate_report_pdf

def run_agents():
    st.subheader("🔹 Running Candidate Profiler...")
    profiler = CandidateProfiler()
    reports = profiler.run()
    st.success(f"{len(reports)} Talent Intelligence Reports generated.")

    st.subheader("🔹 Running Assessment Designer...")
    designer = AssessmentDesigner()
    assessments = designer.run(reports)
    st.success(f"{len(assessments)} Assessment Packages generated.")

    st.subheader("🔹 Running Behavioral Analyzer...")
    behavioral = BehavioralAnalyzer()
    beh_reports = behavioral.run()
    st.success(f"{len(beh_reports)} Behavioral Reports generated.")

    st.subheader("🔹 Running Market Intelligence Analyzer...")
    market = MarketIntelligence()
    market_reports = market.run()
    st.success(f"{len(market_reports)} Market Intelligence Reports generated.")

    st.subheader("🔹 Exporting PDFs for each candidate...")
    pdfs = []
    for r in reports:
        try:
            pdf_path = candidate_report_pdf(r, out_dir="outputs/reports/pdfs")
            pdfs.append(pdf_path)
        except Exception as e:
            st.error(f"PDF error: {e}")
    st.success(f"Generated {len(pdfs)} PDF reports.")

    return reports, assessments, beh_reports, market_reports, pdfs

def main():
    st.set_page_config(page_title="Multi-Agent Recruitment System", layout="wide")
    st.title("🤖 Multi-Agent Recruitment Dashboard")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose Section:", ["Overview", "Run Agents"])

    if page == "Overview":
        st.header("Platform Overview")
        st.write("This dashboard automates recruitment tasks using multiple AI agents.")
        st.markdown("""
        - **Candidate Profiler** → Extracts skills & career progression  
        - **Assessment Designer** → Generates personalized technical assessments  
        - **Behavioral Analyzer** → Evaluates soft skills from interactions  
        - **Market Intelligence** → Summarizes hiring trends & benchmarks  
        """)
    elif page == "Run Agents":
        st.header("🚀 Run Multi-Agent System")
        if st.button("Start Analysis"):
            reports, assessments, beh_reports, market_reports, pdfs = run_agents()
            st.download_button("📥 Download First PDF", open(pdfs[0], "rb"), file_name="candidate_report.pdf") if pdfs else None

if __name__ == "__main__":
    main()
