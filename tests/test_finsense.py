"""Simple unit tests (no API key or internet needed).

Run from the project root:  python -m unittest discover tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm import parse_json, validate_result  # noqa: E402
from nlp_utils import extract_keywords, get_text_stats  # noqa: E402

SAMPLE = "Company X reported a 25% increase in quarterly revenue, but profits declined due to rising operating costs."

VALID = {
    "sentiment": "mixed",
    "financial_impact": "Mixed",
    "positive_factors": ["Revenue up 25%"],
    "negative_factors": ["Profits declined"],
    "financial_topics": ["Revenue", "Profit"],
    "financial_entities": ["Company X"],
    "summary": "Revenue rose but profits fell.",
    "investor_takeaway": "Mixed results.",
}


class TestNlpUtils(unittest.TestCase):
    def test_stats(self):
        stats = get_text_stats(SAMPLE)
        self.assertEqual(stats["words"], 17)
        self.assertEqual(stats["sentences"], 1)
        self.assertEqual(stats["characters"], len(SAMPLE))

    def test_decimal_not_split_into_sentences(self):
        self.assertEqual(get_text_stats("Revenue grew 2.5 percent. Profit fell.")["sentences"], 2)

    def test_keywords_remove_stopwords(self):
        keywords = extract_keywords(SAMPLE, 8)
        self.assertIn("revenue", keywords)
        self.assertNotIn("the", keywords)
        self.assertNotIn("due", keywords)

    def test_keywords_empty_text(self):
        self.assertEqual(extract_keywords("", 5), [])


class TestLlmParsing(unittest.TestCase):
    def test_parse_plain_json(self):
        self.assertEqual(parse_json('{"a": 1}'), {"a": 1})

    def test_parse_code_fenced_json(self):
        self.assertEqual(parse_json('```json\n{"a": 1}\n```'), {"a": 1})

    def test_parse_no_json_raises(self):
        with self.assertRaises(ValueError):
            parse_json("Sorry, I cannot help.")

    def test_parse_broken_json_raises(self):
        with self.assertRaises(ValueError):
            parse_json('{"a": ')

    def test_validate_normalizes_label(self):
        self.assertEqual(validate_result(dict(VALID))["sentiment"], "Mixed")

    def test_validate_missing_field_raises(self):
        data = dict(VALID)
        del data["summary"]
        with self.assertRaises(ValueError):
            validate_result(data)

    def test_validate_bad_label_raises(self):
        data = dict(VALID, sentiment="Bullish")
        with self.assertRaises(ValueError):
            validate_result(data)

    def test_validate_list_type_raises(self):
        data = dict(VALID, positive_factors="not a list")
        with self.assertRaises(ValueError):
            validate_result(data)


if __name__ == "__main__":
    unittest.main()