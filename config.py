"""Non-secret configuration for FinSense."""

# --- Gemini settings ---
MODEL_NAME = "gemini-3.5-flash-lite"
# Lower temperature gives more consistent output
TEMPERATURE = 0.0

# Maximum output tokens
MAX_TOKENS = 1000

# Environment variable containing the Gemini API key
API_KEY_ENV_VAR = "GEMINI_API_KEY"


# --- Input limits ---
MIN_WORDS = 5
MAX_INPUT_CHARS = 6000


# --- Traditional NLP settings ---
TOP_KEYWORDS = 8