"""Provider router for handling multiple LLM providers."""

from typing import List, Dict, Any, Optional, Tuple
from .openrouter import query_model as openrouter_query_model, query_models_parallel as openrouter_query_parallel
from .qiniu import query_model as qiniu_query_model, query_models_parallel as qiniu_query_parallel
from .volcengine import query_model as volcengine_query_model, query_models_parallel as volcengine_query_parallel


def parse_model_identifier(model_identifier: str) -> Tuple[str, str]:
    """
    Parse model identifier into provider and model name.

    Args:
        model_identifier: Format "provider:model" (e.g., "openrouter:openai/gpt-4")

    Returns:
        Tuple of (provider, model_name)
    """
    if ":" in model_identifier:
        provider, model = model_identifier.split(":", 1)
        return provider, model
    else:
        # Default to openrouter for backward compatibility
        return "openrouter", model_identifier


async def query_model(
    model_identifier: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a model using the appropriate provider.

    Args:
        model_identifier: Format "provider:model" (e.g., "openrouter:openai/gpt-4")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    provider, model_name = parse_model_identifier(model_identifier)

    if provider == "openrouter":
        return await openrouter_query_model(model_name, messages, timeout)
    elif provider == "qiniu":
        return await qiniu_query_model(model_name, messages, timeout)
    elif provider == "volcengine":
        return await volcengine_query_model(model_name, messages, timeout)
    else:
        print(f"Unknown provider: {provider}")
        return None


async def query_models_parallel(
    model_identifiers: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel using their respective providers.

    Args:
        model_identifiers: List of model identifiers with provider prefix
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Group models by provider for batch processing
    provider_groups = {}
    for model_id in model_identifiers:
        provider, model_name = parse_model_identifier(model_id)
        if provider not in provider_groups:
            provider_groups[provider] = []
        provider_groups[provider].append((model_id, model_name))

    # Execute queries for each provider group
    all_responses = {}

    for provider, model_list in provider_groups.items():
        if provider == "openrouter":
            # Extract model names for batch query
            model_names = [model_name for _, model_name in model_list]
            provider_responses = await openrouter_query_parallel(model_names, messages)
            # Map back to full identifiers
            for (full_id, _), response in zip(model_list, provider_responses.values()):
                all_responses[full_id] = response

        elif provider == "qiniu":
            # Qiniu parallel queries
            model_names = [model_name for _, model_name in model_list]
            provider_responses = await qiniu_query_parallel(model_names, messages)
            # Map back to full identifiers
            for (full_id, _), response in zip(model_list, provider_responses.values()):
                all_responses[full_id] = response

        elif provider == "volcengine":
            # Volcengine parallel queries
            model_names = [model_name for _, model_name in model_list]
            provider_responses = await volcengine_query_parallel(model_names, messages)
            # Map back to full identifiers
            for (full_id, _), response in zip(model_list, provider_responses.values()):
                all_responses[full_id] = response

        else:
            # Unknown provider - set None for all models in this group
            for full_id, _ in model_list:
                all_responses[full_id] = None
                print(f"Unknown provider: {provider} for model {full_id}")

    return all_responses