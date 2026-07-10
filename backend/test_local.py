import httpx
import asyncio

async def test_local():
    async with httpx.AsyncClient(timeout=60.0) as client:
        print("Testing local server...")
        print("-" * 50)
        
        # Test health
        response = await client.get("http://localhost:8000/health")
        print(f"✅ Health: {response.json()}")
        
        # Test analyze
        variant = {
            "chromosome": "17",
            "position": 43092995,
            "reference_allele": "A",
            "alternate_allele": "G",
            "gene": "BRCA1"
        }
        
        response = await client.post("http://localhost:8000/analyze", json=variant)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Analysis successful!")
            print(f"   DNA Score: {result['dna_score']['delta_score']:.3f} ({result['dna_score']['interpretation']})")
            print(f"   Protein Score: {result['protein_analysis']['protein_score']['delta_score']:.3f} ({result['protein_analysis']['protein_score']['impact']})")
            print(f"   ACMG: {result['acmg']['classification']}")
        else:
            print(f"❌ Failed: {response.status_code}")

if __name__ == "__main__":
    asyncio.run(test_local())