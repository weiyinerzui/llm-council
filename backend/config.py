"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Qiniu Cloud AI API key
QINIU_API_KEY = os.getenv("QINIU_API_KEY")

# Volcengine Ark API key
VOLCENGINE_API_KEY = os.getenv("VOLCENGINE_API_KEY")

# Council members - list of model identifiers with provider prefix
# Format: "provider:model" where provider is "openrouter", "qiniu", or "volcengine"
COUNCIL_MODELS = [
    # "openrouter:openai/gpt-5.1",
    # "openrouter:google/gemini-3-pro-preview",
    # "openrouter:anthropic/claude-sonnet-4.5",
    # "openrouter:x-ai/grok-4",
    # "qiniu:claude-4.5-sonnet",  # 七牛云不支持此模型
    "qiniu:openai/gpt-5",  # Qiniu Cloud AI model
    # "qiniu:z-ai/glm-4.6",  # Qiniu Cloud AI model (已测试通过)
    # "qiniu:deepseek/deepseek-v3.2-251201",  # Qiniu Cloud AI model (已测试通过)
    "qiniu:claude-4.5-sonnet",  # Qiniu Cloud AI model (备用选项)
    "volcengine:deepseek-v3-2-251201",  # Volcengine Ark model
    # "volcengine:doubao-seed-code-preview-251028",  # Volcengine Ark model
    "volcengine:kimi-k2-thinking-251104",  # Volcengine Ark model
    # "volcengine:doubao-seed-1-6-thinking-250715",  # Volcengine Ark model
]

# Chairman model - synthesizes final response
# Format: "provider:model"
CHAIRMAN_MODEL = "qiniu:claude-4.5-sonnet"  # 使用已测试通过的模型

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Qiniu Cloud AI API endpoint
QINIU_API_URL = "https://api.qnaigc.com/v1/chat/completions"

# Volcengine Ark API endpoint
VOLCENGINE_API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
