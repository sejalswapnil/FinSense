"""Gemini LLM interaction: call the API, parse and validate JSON."""

import json
import os

from dotenv import load_dotenv
from google import genai

import config
from prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

ALLOWED_LABELS = {"Positive", "Negative", "Neutral", "Mixed"}

LIST_FIELDS = [
    "positive_factors",
    "negative_factors",
    "financial_topics",
    "financial_entities",
]

TEXT_FIELDS = [
    "summary",
    "investor_takeaway",
]

EXPECTED_KEYS = (
    ["sentiment", "financial_impact"]
    + LIST_FIELDS
    + TEXT_FIELDS
)


def get_client():
    """Create the Gemini client using the API key from .env."""
    api_key = os.getenv(config.API_KEY_ENV_VAR)

    if not api_key:
        raise RuntimeError(
            f"API key not found. Add {config.API_KEY_ENV_VAR} to your .env file."
        )

    return genai.Client(api_key=api_key)


def parse_json(raw_text):
    """Convert Gemini's response into a Python dictionary."""
    text = raw_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("The model did not return a JSON object.")

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        raise ValueError("The model returned invalid JSON.")


def validate_result(data):
    """Check that Gemini returned the expected structure."""

    if not isinstance(data, dict):
        raise ValueError("Unexpected response format from the model.")

    missing = [
        key for key in EXPECTED_KEYS
        if key not in data
    ]

    if missing:
        raise ValueError(
            f"The response is missing fields: {', '.join(missing)}"
        )

    for key in ["sentiment", "financial_impact"]:
        value = str(data[key]).strip().capitalize()

        if value not in ALLOWED_LABELS:
            raise ValueError(
                f"Unexpected value for '{key}': {data[key]!r}"
            )

        data[key] = value

    for key in LIST_FIELDS:
        if not isinstance(data[key], list):
            raise ValueError(f"'{key}' should be a list.")

        data[key] = [
            str(item).strip()
            for item in data[key]
            if str(item).strip()
        ]

    for key in TEXT_FIELDS:
        data[key] = str(data[key]).strip()

    return data


def analyze_news(news_text):
    """Send financial news to Gemini and return validated analysis."""

    client = get_client()

    try:
        prompt = build_user_prompt(news_text)

        response = client.models.generate_content(
            model=config.MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
            config={
                "temperature": config.TEMPERATURE,
                "max_output_tokens": config.MAX_TOKENS,
                "response_mime_type": "application/json",
            },
        )

    except Exception as error:
        error_message = str(error).lower()

        if "api key" in error_message or "authentication" in error_message:
            raise RuntimeError(
                "Invalid Gemini API key. Please check your .env file."
            )

        if "quota" in error_message or "rate" in error_message:
            raise RuntimeError(
                "Gemini API rate limit reached. Please wait and try again."
            )

        raise RuntimeError(f"Gemini API error: {error}")

    raw_text = (response.text or "").strip()

    if not raw_text:
        raise ValueError("Gemini returned an empty response.")

    return validate_result(parse_json(raw_text))