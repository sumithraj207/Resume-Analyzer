# CareerAI — Resume Analyzer

> AI-powered resume analysis tool that scores your profile against job roles using NLP and TF-IDF similarity — with PDF upload support.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-NLP-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What it does

CareerAI analyzes your resume against a target job role and gives you:

| Feature | Description |
|---|---|
| Match Score | Weighted score — keyword coverage (70%) + TF-IDF similarity (30%) |
| Skill Gap Detection | Shows matched, missing, and bonus skills |
| Seniority Detection | Estimates your level from resume language |
| PDF Support | Upload your resume as a PDF directly |
| AI Suggestions | Personalized recommendations to improve your profile |

---

## How the scoring works

```
Final Score = (Keyword Match × 0.70) + (TF-IDF Similarity × 0.30)
```

- **Keyword Match** — checks how many required role skills appear in your resume
- **TF-IDF Similarity** — measures semantic closeness using vectorization + cosine similarity

---

## Supported Roles

- Software Developer
- Data Analyst
- Machine Learning Engineer
- Frontend Developer
- Backend Developer
- DevOps Engineer

---

## Project Structure

```
careerai/
├── app.py                          # Streamlit web app
├── model.py                        # NLP analysis engine
├── skills_db.py                    # Role-skill knowledge base
├── CareerAI_Resume_Analyzer.ipynb  # Jupyter notebook + charts
├── requirements.txt                # Python dependencies
├── .gitignore
└── README.md
```

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/careerai
cd careerai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web UI | Streamlit |
| NLP Engine | Scikit-learn (TF-IDF + Cosine Similarity) |
| PDF Parsing | pdfplumber |
| Visualization | Matplotlib |
| Language | Python 3.9+ |

---

## Resume Bullets

> *"Developed CareerAI, a resume analysis web app using Python and Streamlit that scores candidate profiles against 6 job roles using TF-IDF cosine similarity and keyword matching"*

> *"Designed a dual-scoring NLP engine combining keyword coverage (70%) and TF-IDF semantic similarity (30%) with seniority detection and personalized career recommendations"*

> *"Implemented PDF parsing pipeline using pdfplumber enabling direct resume upload — deployed full-stack AI tool on Hugging Face Spaces"*

---

Built by I. Sumith Raj · 2026
