"""Traditional NLP preprocessing (no LLM): text statistics and keyword extraction."""

import re
from collections import Counter

# A small stopword list for simple keyword extraction
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "to", "in", "on", "at", "by", "for",
    "with", "from", "as", "is", "are", "was", "were", "be", "been", "being", "it", "its",
    "this", "that", "these", "those", "has", "have", "had", "will", "would", "can", "could",
    "should", "may", "might", "than", "then", "also", "due", "after", "before", "over",
    "into", "about", "their", "they", "them", "which", "who", "while", "such", "not", "said",
}


def get_text_stats(text):
    """Count words, sentences and characters."""
    words = re.findall(r"\b\w+\b", text)
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    return {"words": len(words), "sentences": len(sentences), "characters": len(text)}


def extract_keywords(text, top_n):
    """Lowercase -> tokenize -> remove stopwords -> pick the most frequent words."""
    tokens = re.findall(r"[a-zA-Z][a-zA-Z\-']+", text.lower())
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return [word for word, _ in Counter(tokens).most_common(top_n)]