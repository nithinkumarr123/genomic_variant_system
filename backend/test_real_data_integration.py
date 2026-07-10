import httpx
import asyncio

async def test_real_data_integration():
    """Test that real data is being used"""
    
    print("\n" + "="*70)
    print("🔬 TESTING REAL DATA INTEGRATION")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Check health endpoint to see if real data mode is enabled
        health = await client.get("http://localhost:8000/health")
        if health.status_code == 200:
            health_data = health.json()
            print(f"\n✅ Server Status: {health_data['status']}")
            print(f"✅ Real Data Mode: {health_data.get('real_data_mode', False)}")
            print(f"✅ Colab API: {health_data['colab_api']}")
        
        # Test with BRCA1
        print("\n" + "-"*70)
        print("Testing BRCA1 with REAL Ensembl data...")
        print("-"*70)
        
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
            
            print(f"\n📊 Transcript Information:")
            print(f"  Transcript ID: {result['transcript']['transcript_id']}")
            print(f"  CDS Length: {len(result['transcript']['cds_sequence'])} bp")
            print(f"  Protein Length: {len(result['transcript']['protein_sequence'])} aa")
            print(f"  Protein Preview: {result['transcript']['protein_sequence'][:50]}...")
            
            if result.get('clinvar'):
                print(f"\n📋 ClinVar Information:")
                print(f"  Significance: {result['clinvar']['significance']}")
                print(f"  Conditions: {', '.join(result['clinvar']['conditions'])}")
                print(f"  Review Status: {result['clinvar']['review_status']}")
            
            print(f"\n⚖️ ACMG Classification:")
            print(f"  {result['acmg']['classification']} (Score: {result['acmg']['score']:.1f})")
            print(f"  {result['acmg']['summary']}")
            
            if result['acmg']['evidence']:
                print(f"\n  Evidence:")
                for criterion, evidence_list in result['acmg']['evidence'].items():
                    for evidence_item in evidence_list:
                        print(f"    • {criterion}: {evidence_item}")
        else:
            print(f"❌ Error: {response.status_code}")

async def main():
    print("🎯" * 35)
    print("REAL DATA INTEGRATION TEST")
    print("🎯" * 35)
    
    await test_real_data_integration()
    
    print("\n" + "="*70)
    print("✅ Test Complete")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())