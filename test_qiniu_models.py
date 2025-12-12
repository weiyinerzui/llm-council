"""Test script to verify Qiniu Cloud AI API model identifiers."""

import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

QINIU_API_KEY = os.getenv("QINIU_API_KEY")
QINIU_API_URL = "https://api.qnaigc.com/v1"

# Models from config.py
TEST_MODELS = [
    "claude-4.5-sonnet",
    "openai/gpt-5",
    "moonshotai/kimi-k2-thinking",
    "deepseek/deepseek-v3.2-251201",
]

async def get_available_models():
    """Get list of available models from Qiniu API."""
    print("=" * 60)
    print("Fetching available models from Qiniu Cloud AI...")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(
                f"{QINIU_API_URL}/models",
                headers={"Authorization": f"Bearer {QINIU_API_KEY}"}
            )
            response.raise_for_status()
            data = response.json()
            
            print(f"\nTotal models available: {len(data.get('data', []))}\n")
            print("Available model IDs:")
            for model in data.get('data', []):
                print(f"  - {model.get('id')}")
            
            return [m.get('id') for m in data.get('data', [])]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

async def test_model(model_id: str):
    """Test a single model with a simple query."""
    print(f"\n{'-' * 60}")
    print(f"Testing model: {model_id}")
    print(f"{'-' * 60}")
    
    headers = {
        "Authorization": f"Bearer {QINIU_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "Say hello"}],
        "stream": False,
        "max_tokens": 50,
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(
                f"{QINIU_API_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            message = data['choices'][0]['message']['content']
            print(f"✓ SUCCESS: {message[:100]}...")
            return True
        except httpx.HTTPStatusError as e:
            print(f"✗ FAILED: HTTP {e.response.status_code}")
            print(f"  Response: {e.response.text[:200]}")
            return False
        except Exception as e:
            print(f"✗ FAILED: {type(e).__name__}: {str(e)[:100]}")
            return False

async def main():
    """Main test function."""
    print("\n" + "=" * 60)
    print("QINIU CLOUD AI MODEL IDENTIFIER TEST")
    print("=" * 60 + "\n")
    
    # Step 1: Get available models
    available_models = await get_available_models()
    
    # Step 2: Test each configured model
    print("\n" + "=" * 60)
    print("Testing configured models from config.py...")
    print("=" * 60)
    
    results = {}
    for model in TEST_MODELS:
        success = await test_model(model)
        results[model] = success
        await asyncio.sleep(0.5)  # Brief delay between requests
    
    # Step 3: Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"\nConfigured models: {len(TEST_MODELS)}")
    print(f"Successful: {sum(1 for v in results.values() if v)}")
    print(f"Failed: {sum(1 for v in results.values() if not v)}")
    
    print("\nResults:")
    for model, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}: {model}")
    
    # Step 4: Recommendations
    if available_models:
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS")
        print("=" * 60)
        
        failed_models = [m for m, s in results.items() if not s]
        if failed_models:
            print("\nFailed models - check if these match available models:")
            for failed in failed_models:
                # Try to find similar model names
                similar = [am for am in available_models if failed.lower() in am.lower() or am.lower() in failed.lower()]
                if similar:
                    print(f"\n  {failed}")
                    print(f"    Similar available models:")
                    for s in similar[:3]:
                        print(f"      → {s}")
                else:
                    print(f"\n  {failed} - No similar models found")

if __name__ == "__main__":
    asyncio.run(main())
