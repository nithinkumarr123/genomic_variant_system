import httpx
import asyncio

async def test_colab():
    COLAB_URL = input("Enter your Colab URL: ").strip()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {"ngrok-skip-browser-warning": "true"}
        
        print(f"\nTesting connection to {COLAB_URL}")
        print("-" * 50)
        
        # Test health
        try:
            response = await client.get(f"{COLAB_URL}/health", headers=headers)
            print(f"✅ Health check: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
        
        # Test DNA scoring
        try:
            dna_request = {
                "ref": "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
                "alt": "ATGCGTACTTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
                "pos": 15
            }
            response = await client.post(f"{COLAB_URL}/score_dna", json=dna_request, headers=headers)
            print(f"\n✅ DNA scoring: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Delta: {result['delta_score']:.3f}")
                print(f"   Interpretation: {result['interpretation']}")
        except Exception as e:
            print(f"❌ DNA scoring failed: {e}")
        
        # Test protein scoring
        try:
            protein_request = {
                "sequence": "MKTIIALSYIFCLVFA",
                "position": 5,
                "ref_aa": "I",
                "alt_aa": "V"
            }
            response = await client.post(f"{COLAB_URL}/score_protein", json=protein_request, headers=headers)
            print(f"\n✅ Protein scoring: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Delta: {result['delta_score']:.3f}")
                print(f"   Impact: {result['impact']}")
        except Exception as e:
            print(f"❌ Protein scoring failed: {e}")
        
        return True

if __name__ == "__main__":
    asyncio.run(test_colab())