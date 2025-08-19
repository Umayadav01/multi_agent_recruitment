Multi-Agent Recruitment System

🚀 AI-powered recruitment assistant for candidate profiling, assessments, and market insights

Author: Uma Yadav
Repository: GitHub Repo

📌 Project Summary

The Multi-Agent Recruitment System is a local prototype that automates several stages of recruitment using Python and free/open-source NLP models.
It helps HR professionals and recruiters save time by automating candidate analysis, assessment generation, behavioral evaluation, and market research — all within a Streamlit-powered dashboard.

The system works offline, requires no paid APIs, and generates HR-ready PDF reports for candidates.

✨ Features

🧑‍💼 Candidate Profiler → Extracts skills, confidence scores, and career summaries from resumes or text.

📘 Adaptive Assessment Designer → Generates custom skill assessments and rubrics.

💬 Behavioral Analyzer → Analyzes interview/chat transcripts to surface soft skills and communication style.

📊 Market Intelligence → Synthesizes simulated market data into actionable hiring recommendations.

📈 Streamlit Dashboard → Interactive dashboard for candidate profiles, assessments, and trends.

📄 PDF Export → Creates HR-ready PDF reports per candidate.

💻 Self-contained → Runs locally with free/open-source tools.

⚡ Quickstart
1. Clone Repository
git clone https://github.com/Umayadav01/multi_agent_recruitment.git
cd multi_agent_recruitment

2. Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Streamlit App
streamlit run app.py

5. Generate Candidate PDF Reports

Within the dashboard, select a candidate → Export as PDF.

📂 Project Structure
multi_agent_recruitment/
│── app.py                  # Main Streamlit dashboard
│── candidate_profiler.py   # Candidate profiling logic
│── assessment_designer.py  # Adaptive assessment generator
│── behavioral_analyzer.py  # Conversation/soft skills analysis
│── market_intelligence.py  # Market trend synthesis
│── utils.py                # Helper functions (PDF, formatting, etc.)
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation

🔧 Tech Stack

Python 3.9+

Streamlit (UI & dashboard)

NLTK / SpaCy / Transformers (NLP & text analysis)

ReportLab / FPDF (PDF export)

Pandas / NumPy (data handling)

📌 Use Cases

✅ HR teams automating initial screening
✅ Recruiters designing adaptive assessments
✅ Behavioral analysts evaluating communication style
✅ Students & researchers building AI recruitment prototypes

🤝 Contributing

Contributions are welcome! To contribute:

Fork the repository

Create a new branch (feature-xyz)

Commit your changes

Open a pull request

📜 License

This project is licensed under the MIT License – feel free to use and modify it.
