import httpx
import asyncio
import json

async def test_brca1():
    """Test BRCA1 missense variant"""
    
    variant = {
        "chromosome": "17",
        "position": 43092995,
        "reference_allele": "A",
        "alternate_allele": "G",
        "gene": "BRCA1",
        "genome_build": "GRCh38"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        print("\n🔬 Testing BRCA1 Missense Variant")
        print("-" * 50)
        
        response = await client.post("http://localhost:8000/analyze", json=variant)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Mutation Type: {result['protein_analysis']['mutation_type']}")
            print(f"✅ DNA Score: {result['dna_score']['delta_score']:.3f} ({result['dna_score']['interpretation']})")
            print(f"✅ Protein Score: {result['protein_analysis']['protein_score']['delta_score']:.3f} ({result['protein_analysis']['protein_score']['impact']})")
            print(f"✅ ACMG: {result['acmg']['classification']} (score: {result['acmg']['score']})")
            print(f"✅ Protein: {result['uniprot']['protein_name']}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False

async def main():
    print("=" * 60)
    print("🧬 Genomic Variant Interpretation System Test")
    print("=" * 60)
    
    # Check if local server is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Local server running")
                print(f"📡 Colab API: {data['colab_api']}")
            else:
                print("\n❌ Local server not running. Start with: python main.py")
                return
    except:
        print("\n❌ Local server not running. Start with: python main.py")
        return
    
    # Run test
    success = await test_brca1()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Test successful! System is working.")
        print("=" * 60)
        print("\n📝 Example curl command:")
        print("""curl -X POST 'http://localhost:8000/analyze' \\
  -H 'Content-Type: application/json' \\
  -d '{"chromosome":"17","position":43092995,"reference_allele":"A","alternate_allele":"G","gene":"BRCA1"}'""")

if __name__ == "__main__":
    asyncio.run(main())