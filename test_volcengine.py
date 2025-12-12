"""Test script for Volcengine API integration."""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the volcengine module
from backend.volcengine import query_model, query_models_parallel


async def test_single_query():
    """Test querying a single model."""
    print("=" * 60)
    print("Testing Single Model Query")
    print("=" * 60)
    
    # NOTE: Replace with your actual Model ID (Endpoint ID) from Volcengine console
    # Example: "ep-20241212-xxxxx-xxxxx"
    model_id = os.getenv("VOLCENGINE_TEST_MODEL_ID", "ep-xxx-yyy")
    
    if model_id == "ep-xxx-yyy":
        print("\n⚠️  Warning: Using placeholder Model ID")
        print("Please set VOLCENGINE_TEST_MODEL_ID environment variable")
        print("or update test_volcengine.py with your actual Model ID")
        return
    
    messages = [
        {"role": "user", "content": "请用一句话解释什么是人工智能。"}
    ]
    
    print(f"\nModel ID: {model_id}")
    print(f"Query: {messages[0]['content']}")
    print("\nCalling API...")
    
    response = await query_model(model_id, messages)
    
    if response:
        print("\n✅ Success!")
        print(f"Response: {response.get('content', 'No content')[:200]}...")
    else:
        print("\n❌ Failed to get response")


async def test_parallel_queries():
    """Test querying multiple models in parallel."""
    print("\n")
    print("=" * 60)
    print("Testing Parallel Model Queries")
    print("=" * 60)
    
    # NOTE: Replace with your actual Model IDs
    model_ids = [
        os.getenv("VOLCENGINE_TEST_MODEL_ID_1", "ep-model-1"),
        os.getenv("VOLCENGINE_TEST_MODEL_ID_2", "ep-model-2"),
    ]
    
    if any(m.startswith("ep-model-") for m in model_ids):
        print("\n⚠️  Warning: Using placeholder Model IDs")
        print("Please set VOLCENGINE_TEST_MODEL_ID_1 and VOLCENGINE_TEST_MODEL_ID_2")
        return
    
    messages = [
        {"role": "user", "content": "什么是机器学习?"}
    ]
    
    print(f"\nModel IDs: {model_ids}")
    print(f"Query: {messages[0]['content']}")
    print("\nCalling API in parallel...")
    
    responses = await query_models_parallel(model_ids, messages)
    
    print("\nResults:")
    for model_id, response in responses.items():
        if response:
            content_preview = response.get('content', 'No content')[:100]
            print(f"  ✅ {model_id}: {content_preview}...")
        else:
            print(f"  ❌ {model_id}: Failed")


async def main():
    """Run all tests."""
    # Check if API key is set
    api_key = os.getenv("VOLCENGINE_API_KEY")
    if not api_key:
        print("❌ Error: VOLCENGINE_API_KEY not set in .env file")
        print("\nPlease:")
        print("1. Get API Key from: https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey")
        print("2. Add to .env file: VOLCENGINE_API_KEY=your_api_key_here")
        return
    
    print(f"API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Run tests
    await test_single_query()
    await test_parallel_queries()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
