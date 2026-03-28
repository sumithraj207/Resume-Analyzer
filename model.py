from skills_db import skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_tfidf_score(resume_text, role_skills):
    """Compute TF-IDF cosine similarity between resume and role skill set."""
    role_text = " ".join(role_skills)
    corpus = [resume_text.lower(), role_text.lower()]
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100, 2)
    except:
        return 0.0

def analyze_resume(resume_text, role):
    role = role.lower().strip()

    if role not in skills:
        return None

    required_skills = skills[role]["required"]
    bonus_skills = skills[role]["bonus"]

    resume_lower = resume_text.lower()

    # Keyword match
    found_required = [s for s in required_skills if s in resume_lower]
    missing_required = [s for s in required_skills if s not in resume_lower]
    found_bonus = [s for s in bonus_skills if s in resume_lower]

    # TF-IDF similarity score
    all_role_skills = required_skills + bonus_skills
    tfidf_score = get_tfidf_score(resume_text, all_role_skills)

    # Weighted final score: 70% keyword match + 30% TF-IDF similarity
    keyword_score = (len(found_required) / len(required_skills)) * 100
    final_score = int((keyword_score * 0.7) + (tfidf_score * 0.3))
    final_score = min(final_score, 100)

    # Seniority detection
    seniority = "Mid-level"
    resume_words = resume_lower.split()
    years_mentioned = [w for w in resume_words if w.isdigit() and 1 <= int(w) <= 20]
    if any(w in resume_lower for w in ["senior", "lead", "architect", "principal"]):
        seniority = "Senior"
    elif any(w in resume_lower for w in ["intern", "fresher", "entry", "junior", "graduate"]):
        seniority = "Entry-level"
    elif years_mentioned and int(years_mentioned[0]) >= 5:
        seniority = "Senior"

    # Suggestions
    suggestions = []
    if missing_required:
        top_missing = missing_required[:3]
        suggestions.append(f"Add these key skills to strengthen your profile: {', '.join(top_missing)}")
    if found_bonus:
        suggestions.append(f"Great bonus skills detected: {', '.join(found_bonus[:3])} — highlight these prominently")
    elif bonus_skills:
        suggestions.append(f"Consider adding advanced skills like: {', '.join(bonus_skills[:3])} to stand out")
    if final_score >= 80:
        suggestions.append("Excellent match — tailor your summary section to this specific role for maximum impact")
    elif final_score >= 55:
        suggestions.append("Good foundation — focus on closing skill gaps and quantifying your achievements")
    else:
        suggestions.append("Build projects using the missing skills to strengthen your candidacy")

    # Resume quality tips
    if len(resume_text.split()) < 150:
        suggestions.append("Your resume seems short — add more detail about your experience and projects")
    if not any(char.isdigit() for char in resume_text):
        suggestions.append("Add measurable achievements (e.g. 'improved performance by 30%') for stronger impact")

    return {
        "score": final_score,
        "keyword_score": round(keyword_score),
        "tfidf_score": round(tfidf_score),
        "found_required": found_required,
        "missing_required": missing_required,
        "found_bonus": found_bonus,
        "seniority": seniority,
        "suggestions": suggestions,
        "role": role
    }