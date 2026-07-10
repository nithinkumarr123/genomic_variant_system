import httpx
import asyncio
import json

async def test_real_ensembl():
    """Test fetching real data from Ensembl API"""
    print("\n" + "="*70)
    print("🔍 TESTING REAL DATA FROM ENSEMBL API")
    print("="*70)
    
    genes = ["BRCA1", "TP53", "CFTR"]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for gene in genes:
            print(f"\n📊 Fetching data for {gene}...")
            print("-" * 50)
            
            try:
                # Get gene info
                url = f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}"
                headers = {"Content-Type": "application/json"}
                
                response = await client.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    print(f"  ✅ Gene ID: {data.get('id')}")
                    print(f"  ✅ Location: {data.get('seq_region_name')}:{data.get('start')}-{data.get('end')}")
                    print(f"  ✅ Strand: {data.get('strand')}")
                    print(f"  ✅ Description: {data.get('description', 'N/A')[:100]}")
                    
                    # Get transcripts
                    transcript_url = f"https://rest.ensembl.org/lookup/id/{data['id']}?expand=1"
                    response = await client.get(transcript_url, headers=headers)
                    if response.status_code == 200:
                        transcript_data = response.json()
                        
                        # Find canonical transcript
                        for transcript in transcript_data.get('Transcript', []):
                            if transcript.get('is_canonical'):
                                print(f"  ✅ Canonical Transcript: {transcript['id']}")
                                
                                # Get CDS sequence
                                cds_url = f"https://rest.ensembl.org/sequence/id/{transcript['id']}?type=cds"
                                response = await client.get(cds_url, headers=headers)
                                if response.status_code == 200:
                                    cds_data = response.json()
                                    cds_seq = cds_data.get('seq', '')
                                    print(f"  ✅ CDS Length: {len(cds_seq)} bp")
                                    print(f"  ✅ CDS Preview: {cds_seq[:50]}...")
                                break
                else:
                    print(f"  ❌ Failed: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")

async def test_real_clinvar():
    """Test fetching real data from ClinVar API"""
    print("\n" + "="*70)
    print("🔍 TESTING REAL DATA FROM CLINVAR API")
    print("="*70)
    
    variants = [
        {"gene": "BRCA1", "variant": "c.68_69delAG"},
        {"gene": "TP53", "variant": "c.524G>A"},
        {"gene": "CFTR", "variant": "c.1521_1523delCTT"}
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for item in variants:
            print(f"\n📊 Searching ClinVar for {item['gene']} {item['variant']}...")
            print("-" * 50)
            
            try:
                # Search ClinVar
                search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                params = {
                    "db": "clinvar",
                    "term": f"{item['gene']}[gene] AND {item['variant']}[variant]",
                    "retmode": "json",
                    "retmax": 5
                }
                
                response = await client.get(search_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    ids = data.get('esearchresult', {}).get('idlist', [])
                    
                    if ids:
                        print(f"  ✅ Found {len(ids)} ClinVar entries")
                        
                        # Fetch details
                        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                        params = {
                            "db": "clinvar",
                            "id": ",".join(ids[:2]),
                            "retmode": "json"
                        }
                        
                        response = await client.get(summary_url, params=params)
                        if response.status_code == 200:
                            summary = response.json()
                            
                            for uid, doc in summary.get('result', {}).items():
                                if uid != 'uidlist':
                                    # Extract significance
                                    significance = "Unknown"
                                    if 'clinical_significance' in doc:
                                        cs = doc['clinical_significance']
                                        if isinstance(cs, dict):
                                            significance = cs.get('description', 'Unknown')
                                        elif isinstance(cs, list):
                                            significance = cs[0].get('description', 'Unknown')
                                    
                                    print(f"  ✅ Clinical Significance: {significance}")
                                    
                                    # Extract conditions
                                    if 'trait_set' in doc:
                                        conditions = []
                                        for trait in doc['trait_set']:
                                            if isinstance(trait, dict):
                                                trait_name = trait.get('trait_name')
                                                if trait_name:
                                                    conditions.append(trait_name)
                                        if conditions:
                                            print(f"  ✅ Conditions: {', '.join(conditions[:2])}")
                                    
                                    # Review status
                                    review = doc.get('review_status', 'No review')
                                    print(f"  ✅ Review Status: {review}")
                                    break
                    else:
                        print(f"  ⚠️ No ClinVar entries found")
                else:
                    print(f"  ❌ Failed: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")

async def test_complete_pipeline():
    """Test the complete pipeline with real data"""
    print("\n" + "="*70)
    print("🚀 TESTING COMPLETE PIPELINE WITH REAL DATA")
    print("="*70)
    
    # Test variants with real genomic coordinates
    test_variants = [
        {
            "name": "BRCA1 Pathogenic (185delAG)",
            "chromosome": "17",
            "position": 43092995,
            "ref": "AG",
            "alt": "A",
            "gene": "BRCA1"
        },
        {
            "name": "BRCA1 Missense",
            "chromosome": "17",
            "position": 43092995,
            "ref": "A",
            "alt": "G",
            "gene": "BRCA1"
        },
        {
            "name": "TP53 Missense (R175H)",
            "chromosome": "17",
            "position": 7676152,
            "ref": "C",
            "alt": "T",
            "gene": "TP53"
        }
    ]
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for variant in test_variants:
            print(f"\n🔬 Testing: {variant['name']}")
            print("-" * 50)
            
            # Prepare request
            request = {
                "chromosome": variant["chromosome"],
                "position": variant["position"],
                "reference_allele": variant["ref"],
                "alternate_allele": variant["alt"],
                "gene": variant["gene"],
                "genome_build": "GRCh38"
            }
            
            try:
                # Call your local API
                response = await client.post(
                    "http://localhost:8000/analyze",
                    json=request
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"  ✅ DNA Score: {result['dna_score']['delta_score']:.3f} ({result['dna_score']['interpretation']})")
                    print(f"  ✅ Protein Score: {result['protein_analysis']['protein_score']['delta_score']:.3f} ({result['protein_analysis']['protein_score']['impact']})")
                    print(f"  ✅ ACMG: {result['acmg']['classification']} (Score: {result['acmg']['score']:.1f})")
                    
                    if result.get('clinvar'):
                        print(f"  ✅ ClinVar: {result['clinvar']['significance']}")
                        if result['clinvar']['conditions']:
                            print(f"  ✅ Associated Conditions: {', '.join(result['clinvar']['conditions'][:2])}")
                else:
                    print(f"  ❌ API Error: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ Connection Error: {e}")
                print(f"  💡 Make sure your local server is running: python main.py")

async def main():
    """Run all real data tests"""
    print("\n" + "🎯" * 35)
    print("REAL-TIME DATA TESTING SUITE")
    print("🎯" * 35)
    
    # Test 1: Ensembl API
    await test_real_ensembl()
    
    # Test 2: ClinVar API
    await test_real_clinvar()
    
    # Test 3: Complete pipeline
    await test_complete_pipeline()
    
    print("\n" + "="*70)
    print("✅ TESTING COMPLETE")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())