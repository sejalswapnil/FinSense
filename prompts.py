"""Prompt templates for the FinSense financial news analyzer."""

SYSTEM_PROMPT = """
You are a financial NLP analyst.

Analyze the financial news provided by the user.

Your job is to identify:
1. Overall sentiment
2. Financial impact based only on the text
3. Positive factors
4. Negative factors
5. Financial topics
6. Financial entities
7. A concise summary
8. An investor-oriented takeaway

Important rules:
- Use ONLY the information provided in the financial news.
- Do not use external knowledge.
- Do not invent facts, numbers, companies, events, or causes.
- Do not predict stock prices.
- Do not provide personalized financial advice.
- If something is not mentioned, use an empty list or a concise statement saying it is not mentioned.
- Keep the answer concise and factual.
- Return ONLY valid JSON.
"""

def build_user_prompt(news_text):
    """Build the user prompt containing the financial news."""

    return f"""
Analyze the following financial news.

Return a JSON object with exactly these fields:

{{
    "sentiment": "Positive | Negative | Neutral | Mixed",
    "financial_impact": "Positive | Negative | Neutral | Mixed",
    "positive_factors": [],
    "negative_factors": [],
    "financial_topics": [],
    "financial_entities": [],
    "summary": "",
    "investor_takeaway": ""
}}

Financial news:

---BEGIN NEWS---
{news_text}
---END NEWS---

Remember:
- Base the analysis only on the supplied text.
- Do not predict stock prices.
- Do not give personalized financial advice.
- Return valid JSON only.
"""