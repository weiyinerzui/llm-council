"""Volcengine Ark API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import VOLCENGINE_API_KEY, VOLCENGINE_API_URL


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via Volcengine Ark API.

    Args:
        model: Volcengine model identifier (Endpoint ID, e.g., "ep-xxx-yyy")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    headers = {
        "Authorization": f"Bearer {VOLCENGINE_API_KEY}",
        "Content-Type": "application/json",
    }

    # Smart parameter selection based on model
    # Some models may require 'max_completion_tokens' instead of 'max_tokens'
    # For now, using standard 'max_tokens' as per OpenAI-compatible API
    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                VOLCENGINE_API_URL,
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
        print(f"Error querying model {model} via Volcengine: HTTP {e.response.status_code}")
        print(f"Response: {e.response.text[:500]}")
        return None
    except Exception as e:
        print(f"Error querying model {model} via Volcengine: {type(e).__name__}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel via Volcengine Ark.

    Args:
        models: List of Volcengine model identifiers (Endpoint IDs)
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
