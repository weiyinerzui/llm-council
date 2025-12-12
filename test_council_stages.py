"""Test council stages to identify stage-specific model failures."""

import asyncio
from backend.council import stage1_collect_responses, stage2_collect_rankings, stage3_synthesize_final
from backend.config import COUNCIL_MODELS

async def main():
    print("=" * 70)
    print("COUNCIL STAGE TESTING")
    print("=" * 70)
    print(f"\nConfigured models ({len(COUNCIL_MODELS)}):")
    for i, model in enumerate(COUNCIL_MODELS, 1):
        print(f"  {i}. {model}")
    
    test_query = "你好啊"
    
    # Stage 1 Test
    print("\n" + "=" * 70)
    print("STAGE 1: Collecting Individual Responses")
    print("=" * 70)
    stage1_results = await stage1_collect_responses(test_query)
    
    print(f"\nResults: {len(stage1_results)}/{len(COUNCIL_MODELS)} models responded")
    for result in stage1_results:
        model = result['model']
        response_preview = result['response'][:100] if result['response'] else "(empty)"
        print(f"\n✓ {model}")
        print(f"  Response: {response_preview}...")
    
    # Check which models failed
    responded_models = set(r['model'] for r in stage1_results)
    all_models = set(COUNCIL_MODELS)
    failed_models = all_models - responded_models
    
    if failed_models:
        print(f"\n✗ Failed models in Stage 1:")
        for model in failed_models:
            print(f"  - {model}")
    
    if len(stage1_results) == 0:
        print("\n❌ No models responded in Stage 1. Cannot continue to Stage 2.")
        return
    
    # Stage 2 Test
    print("\n" + "=" * 70)
    print("STAGE 2: Collecting Peer Rankings")
    print("=" * 70)
    stage2_results, label_to_model = await stage2_collect_rankings(test_query, stage1_results)
    
    print(f"\nResults: {len(stage2_results)}/{len(COUNCIL_MODELS)} models provided rankings")
    for result in stage2_results:
        model = result['model']
        print(f"\n✓ {model}")
        if result.get('parsed_ranking'):
            print(f"  Ranking: {', '.join(result['parsed_ranking'][:3])}...")
        else:
            print(f"  Ranking: (parsing failed)")
    
    # Check which models failed in stage 2
    ranked_models = set(r['model'] for r in stage2_results)
    failed_stage2 = all_models - ranked_models
    
    if failed_stage2:
        print(f"\n✗ Failed models in Stage 2:")
        for model in failed_stage2:
            print(f"  - {model}")
    
    if len(stage2_results) == 0:
        print("\n❌ No models provided rankings in Stage 2. Cannot continue to Stage 3.")
        return
    
    # Stage 3 Test
    print("\n" + "=" * 70)
    print("STAGE 3: Chairman Synthesis")
    print("=" * 70)
    stage3_result = await stage3_synthesize_final(test_query, stage1_results, stage2_results)
    
    if stage3_result['response']:
        print(f"\n✓ Chairman ({stage3_result['model']}) synthesis complete")
        print(f"  Response preview: {stage3_result['response'][:150]}...")
    else:
        print(f"\n✗ Chairman synthesis failed")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"\nTotal configured models: {len(COUNCIL_MODELS)}")
    print(f"Stage 1 responses: {len(stage1_results)}/{len(COUNCIL_MODELS)}")
    print(f"Stage 2 rankings: {len(stage2_results)}/{len(COUNCIL_MODELS)}")
    print(f"Stage 3 synthesis: {'✓ Success' if stage3_result['response'] else '✗ Failed'}")
    
    if failed_models:
        print(f"\n⚠️  Models failing in Stage 1:")
        for model in failed_models:
            print(f"  - {model}")
    
    if failed_stage2:
        print(f"\n⚠️  Models failing in Stage 2:")
        for model in failed_stage2:
            print(f"  - {model}")

if __name__ == "__main__":
    asyncio.run(main())
