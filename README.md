# FinSense
# FinSense: LLM-Based Financial News Sentiment and Impact Analyzer

**Batch F NLP Capstone | Manipal University Jaipur | B.Tech CSE (Data Science)**

FinSense is a small NLP project. You paste a financial news article or paragraph and the app returns a structured analysis: sentiment, financial impact, positive and negative factors, topics, entities, a summary and an investor takeaway.

> **Note:** FinSense is **not** a stock prediction system. "Financial Impact" is the likely interpretation of the news based **only on the text you paste**. It is for learning purposes and is not financial advice.

## Team

NAME-Sejal Swapnil
REG NO.-23FE10CDS00460


Instructor: `<instructor-github-username>` (collaborator). See [docs/CONTRIBUTIONS.md](docs/CONTRIBUTIONS.md) for who did what.

## How it works

1. **Traditional NLP (no LLM):** word, sentence and character counts and keyword extraction (tokenization, stopword removal, frequency count) in `nlp_utils.py`.
2. **LLM via API:** semantic financial analysis. The prompt in `prompts.py` forces the model to use only the supplied text and return valid JSON.
3. **Validation:** `llm.py` parses and checks the JSON before the Streamlit UI shows it. Empty input, API failure, invalid JSON and unexpected output are handled with friendly messages.

## Repository structure

```
FinSense/
├── app.py                 # Streamlit UI
├── nlp_utils.py           # Text statistics + keyword extraction
├── llm.py                 # API call, JSON parsing, validation, error handling
├── prompts.py             # System prompt and user prompt template
├── config.py              # Model name, temperature, max tokens, limits
├── requirements.txt
├── .env.example           # Template for the API key
├── .gitignore             # Keeps .env out of GitHub
├── tests/                 # Unit tests (no API key needed)
├── .vscode/               # Shared VS Code settings, debug configs, tasks
├── docs/                  # INSTALL.md, VSCODE_SETUP.md, GITHUB_WORKFLOW.md, CONTRIBUTIONS.md, PROJECT_REPORT.md
├── results/               # Sample inputs and manual evaluation
├── screenshots/           # App screenshots
├── presentation/          # Final presentation and outline
└── README.md
```

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env        # add your free GEMINI_API_KEY (https://aistudio.google.com/apikey)
streamlit run app.py
```

Full steps and troubleshooting: [docs/INSTALL.md](docs/INSTALL.md). Using VS Code (debug, tasks, tests, Git/PR workflow): [docs/VSCODE_SETUP.md](docs/VSCODE_SETUP.md). Run tests with `python -m unittest discover tests -v`.

## Example

Input: *Company X reported a 25% increase in quarterly revenue, but profits declined due to rising operating costs.*

Expected output (approximate):

```json
{
  "sentiment": "Mixed",
  "financial_impact": "Mixed",
  "positive_factors": ["25% increase in quarterly revenue"],
  "negative_factors": ["Profits declined", "Rising operating costs"],
  "financial_topics": ["Revenue", "Profit", "Operating costs"],
  "financial_entities": ["Company X"],
  "summary": "Company X's quarterly revenue grew 25%, but profits fell because operating costs rose.",
  "investor_takeaway": "Revenue growth is positive, but falling profit due to higher costs is a concern."
}
```

## Results and screenshots

See [results/sample_results.md](results/sample_results.md) (manual comparison of LLM output with human labels) and the [screenshots/](screenshots/) folder.

## Limitations

- The LLM can make mistakes; results should be checked by a human.
- Analysis uses only the pasted text (no market data or news context).
- English text only (tested).
- Not a stock predictor and not financial advice.

## Future scope

Batch CSV analysis, sentence-level sentiment, larger evaluation on a labelled dataset (e.g. Financial PhraseBank), more LLM providers.
