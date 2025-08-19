# app/main.py
from agents.candidate_profiler import CandidateProfiler
from agents.assessment_designer import AssessmentDesigner
from agents.behavioral_analyzer import BehavioralAnalyzer
from agents.market_intelligence import MarketIntelligence
from utils.pdf_generator import candidate_report_pdf
import json
from pathlib import Path

def main():
    print("\n=== 🚀 Multi-Agent Recruitment System Running ===\n")

    # 1. Candidate Profiling
    print("🔹 Running Candidate Profiler...")
    profiler = CandidateProfiler()
    reports = profiler.run()
    print(f"✅ {len(reports)} Talent Intelligence Reports generated.\n")

    # 2. Assessment Designer
    print("🔹 Running Assessment Designer...")
    designer = AssessmentDesigner()
    assessments = designer.run(reports)
    print(f"✅ {len(assessments)} Assessment Packages generated.\n")

    # 3. Behavioral Analyzer
    print("🔹 Running Behavioral Analyzer...")
    behavioral = BehavioralAnalyzer()
    beh_reports = behavioral.run()
    print(f"✅ {len(beh_reports)} Behavioral Reports generated.\n")

    # 4. Market Intelligence
    print("🔹 Running Market Intelligence Analyzer...")
    market = MarketIntelligence()
    market_reports = market.run()
    print(f"✅ {len(market_reports)} Market Intelligence Reports generated.\n")

    print("All agents executed successfully. Reports are available in outputs/ folder.")


    print("🔹 Exporting PDFs for each candidate...")
    pdfs = []
    for r in reports:
        try:
            pdf_path = candidate_report_pdf(r, out_dir="outputs/reports/pdfs")
            pdfs.append(pdf_path)
        except Exception as e:
            print("PDF error:", e)
    print(f"Generated {len(pdfs)} PDF reports (outputs/reports/pdfs/).\n")

if __name__ == "__main__":
    main()
