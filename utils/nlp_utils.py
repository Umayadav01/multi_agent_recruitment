# utils/nlp_utils.py
from __future__ import annotations
import re
from typing import List, Dict, Tuple
import numpy as np

try:
    import spacy
    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = None  # We won't hard-fail; functions check this.

# Free, lightweight sentence embedding model
from sentence_transformers import SentenceTransformer

# Cache the model so imports are cheap
_EMB = SentenceTransformer("all-MiniLM-L6-v2")

# A tiny, extendable skills ontology. You can expand freely.
SKILL_ONTOLOGY: Dict[str, List[str]] = {
    "Python": ["python", "pandas", "numpy", "scikit-learn", "sklearn"],
    "Java": ["java", "spring", "jvm"],
    "C++": ["c++", "cpp", "stl"],
    "TensorFlow": ["tensorflow", "tf", "keras"],
    "PyTorch": ["pytorch", "torch", "torchvision"],
    "SQL": ["sql", "postgres", "mysql", "sqlite"],
    "Docker": ["docker", "container"],
    "Kubernetes": ["kubernetes", "k8s"],
    "React": ["react", "reactjs", "next.js", "nextjs", "vite"],
    "NLP": ["nlp", "bert", "transformer", "llm", "hugging face", "tokenization"],
    "Computer Vision": ["opencv", "vision", "cnn", "image classification", "yolo"],
    "Data Engineering": ["airflow", "etl", "spark", "hadoop"],
}

def clean_text(s: str) -> str:
    s = s.replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s

def embed(texts: List[str]) -> np.ndarray:
    if isinstance(texts, str):
        texts = [texts]
    return _EMB.encode(texts, normalize_embeddings=True)

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))

def extract_skills(text: str) -> List[Tuple[str, float]]:
    """
    Heuristic extraction:
    1) Keyword match against ontology synonyms.
    2) Back off to embedding similarity against skill labels.
    Returns list[(skill, confidence 0..1)]
    """
    text_l = text.lower()
    # 1) Keyword match
    hits = {}
    for skill, synonyms in SKILL_ONTOLOGY.items():
        for syn in synonyms + [skill]:
            syn_l = syn.lower()
            if re.search(rf"\b{re.escape(syn_l)}\b", text_l):
                hits[skill] = max(hits.get(skill, 0), 0.8)  # strong confidence for explicit match

    # 2) Embedding similarity against labels (for subtle mentions)
    # Only check skills not already hit
    remaining = [s for s in SKILL_ONTOLOGY.keys() if s not in hits]
    if remaining:
        text_vec = embed([text])[0]
        skill_vecs = embed(remaining)
        sims = (skill_vecs @ text_vec).tolist()
        for skill, sim in zip(remaining, sims):
            if sim > 0.45:   # conservative threshold
                # map sim ~ [0.45..0.8] → [0.4..0.7]
                conf = 0.4 + (sim - 0.45) * (0.7 - 0.4) / (0.8 - 0.45)
                conf = float(max(0.4, min(0.7, conf)))
                hits[skill] = max(hits.get(skill, 0), conf)

    # Sort by confidence
    return sorted([(k, round(v, 2)) for k, v in hits.items()], key=lambda x: x[1], reverse=True)

def summarize_text(text: str, max_sentences: int = 3) -> str:
    """
    Super-light extractive summary: pick top sentences by length & uniqueness.
    Replace with an LLM later if you like; keep free/local now.
    """
    text = clean_text(text)
    sents = re.split(r"(?<=[.!?])\s+", text)
    sents = [s.strip() for s in sents if 20 <= len(s) <= 220]
    if not sents:
        return text[:240]
    # Score by length (proxy) and uniqueness
    scores = []
    for s in sents:
        tokens = set(re.findall(r"\b\w+\b", s.lower()))
        scores.append((len(tokens) + len(s) * 0.01, s))
    scores.sort(reverse=True)
    chosen = [s for _, s in scores[:max_sentences]]
    return " ".join(chosen)
