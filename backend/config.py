"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Qiniu Cloud AI API key
QINIU_API_KEY = os.getenv("QINIU_API_KEY")

# Council members - list of model identifiers with provider prefix
# Format: "provider:model" where provider is "openrouter" or "qiniu"
COUNCIL_MODELS = [
    # "openrouter:openai/gpt-5.1",
    # "openrouter:google/gemini-3-pro-preview",
    # "openrouter:anthropic/claude-sonnet-4.5",
    # "openrouter:x-ai/grok-4",
    "qiniu:claude-4.5-sonnet",  # Qiniu Cloud AI model
    "qiniu:openai/gpt-5",  # Qiniu Cloud AI model
    "qiniu:minimax/minimax-m2",  # Qiniu Cloud AI model
    "qiniu:z-ai/glm-4.6",  # Qiniu Cloud AI model
]

# Chairman model - synthesizes final response
# Format: "provider:model"
CHAIRMAN_MODEL = "qiniu:claude-4.5-sonnet"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Qiniu Cloud AI API endpoint
QINIU_API_URL = "https://api.qnaigc.com/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
