"""FinSense - Streamlit user interface and traditional NLP preprocessing."""

import streamlit as st

import config
from llm import analyze_news
from nlp_utils import extract_keywords, get_text_stats


# ---------- UI helpers ----------
def show_label(label):
    """Show Positive/Negative/Neutral/Mixed with a matching colour."""
    if label == "Positive":
        st.success(label)
    elif label == "Negative":
        st.error(label)
    elif label == "Mixed":
        st.warning(label)
    else:
        st.info(label)


def show_list(items, empty_message):
    """Show a list as bullet points, or a message if it is empty."""
    if items:
        for item in items:
            st.markdown(f"- {item}")
    else:
        st.write(empty_message)


# ---------- Page ----------
st.set_page_config(page_title="FinSense", page_icon="📰")
st.title("FinSense")
st.caption("LLM-Based Financial News Sentiment and Impact Analyzer")

news_text = st.text_area("Financial news", height=250, placeholder="Paste financial news here...")

if st.button("Analyze News"):
    news_text = news_text.strip()

    # Input validation
    if not news_text:
        st.warning("Please paste some financial news first.")
        st.stop()
    if len(news_text) > config.MAX_INPUT_CHARS:
        st.warning(f"Text is too long. Please keep it under {config.MAX_INPUT_CHARS} characters.")
        st.stop()

    stats = get_text_stats(news_text)
    if stats["words"] < config.MIN_WORDS:
        st.warning(f"Text is too short. Please enter at least {config.MIN_WORDS} words.")
        st.stop()

    keywords = extract_keywords(news_text, config.TOP_KEYWORDS)

    # LLM call with error handling
    try:
        with st.spinner("Analyzing..."):
            result = analyze_news(news_text)
    except RuntimeError as error:   # API key / network / API problems
        st.error(str(error))
        st.stop()
    except ValueError as error:     # invalid JSON / unexpected response
        st.error(f"Could not read the model's answer. {error} Please try again.")
        st.stop()
    except Exception as error:      # anything else
        st.error(f"Something went wrong: {error}")
        st.stop()

    # Section 1
    st.subheader("1. Text Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Words", stats["words"])
    col2.metric("Sentences", stats["sentences"])
    col3.metric("Characters", stats["characters"])
    st.write("**Keywords:** " + (", ".join(keywords) if keywords else "None found"))

    # Section 2
    st.subheader("2. Overall Sentiment")
    show_label(result["sentiment"])

    # Section 3
    st.subheader("3. Financial Impact")
    show_label(result["financial_impact"])
    st.caption("Interpretation based only on the text above. This is not a stock price prediction.")

    # Section 4
    st.subheader("4. Positive Factors")
    show_list(result["positive_factors"], "No positive factors found in the text.")

    # Section 5
    st.subheader("5. Negative Factors")
    show_list(result["negative_factors"], "No negative factors found in the text.")

    # Section 6
    st.subheader("6. Financial Topics")
    show_list(result["financial_topics"], "No financial topics identified.")

    # Section 7
    st.subheader("7. Financial Entities")
    show_list(result["financial_entities"], "No financial entities mentioned.")

    # Section 8
    st.subheader("8. Summary")
    st.write(result["summary"] or "No summary returned.")

    # Section 9
    st.subheader("9. Investor Takeaway")
    st.write(result["investor_takeaway"] or "No takeaway returned.")
    st.caption("For learning purposes only. Not financial advice.")