"""Qiniu Cloud AI API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import QINIU_API_KEY, QINIU_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Qiniu Cloud AI API.

    Args:
        model: Qiniu model identifier (e.g., "deepseek-v3")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    headers = {
        "Authorization": f"Bearer {QINIU_API_KEY}",
        "Content-Type": "application/json",
    }

    # Smart parameter selection based on model
    # GPT-5 series requires 'max_completion_tokens' instead of 'max_tokens'
    if model.startswith("openai/gpt-5") or model.startswith("openai/gpt-4o"):
        max_token_param = "max_completion_tokens"
    else:
        max_token_param = "max_tokens"

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,  # Non-streaming for council processing
        max_token_param: 4096,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                QINIU_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except httpx.HTTPStatusError as e:
        # Log HTTP errors with more detail
        print(f"Error querying model {model} via Qiniu: HTTP {e.response.status_code}")
        print(f"Response: {e.response.text[:500]}")
        return None
    except Exception as e:
        print(f"Error querying model {model} via Qiniu: {type(e).__name__}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel via Qiniu Cloud AI.

    Args:
        models: List of Qiniu model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}