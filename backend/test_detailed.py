import httpx
import asyncio
import json

async def test_detailed():
    """Test with detailed output"""
    
    variant = {
        "chromosome": "17",
        "position": 43092995,
        "reference_allele": "A",
        "alternate_allele": "G",
        "gene": "BRCA1"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        print("\n" + "="*70)
        print("🔬 GENOMIC VARIANT INTERPRETATION REPORT")
        print("="*70)
        
        response = await client.post("http://localhost:8000/analyze", json=variant)
        
        if response.status_code == 200:
            result = response.json()
            
            # Variant Information
            print("\n📌 VARIANT INFORMATION")
            print("-" * 70)
            print(f"  Gene: {result['variant']['gene']}")
            print(f"  Chromosome: {result['variant']['chromosome']}")
            print(f"  Position: {result['variant']['position']}")
            print(f"  Change: {result['variant']['reference_allele']} → {result['variant']['alternate_allele']}")
            print(f"  Genome Build: {result['variant']['genome_build']}")
            
            # Transcript Information
            print("\n📋 TRANSCRIPT INFORMATION")
            print("-" * 70)
            print(f"  Transcript ID: {result['transcript']['transcript_id']}")
            print(f"  Gene Symbol: {result['transcript']['gene_symbol']}")
            print(f"  CDS Position: {result['transcript']['cds_position']}")
            print(f"  Amino Acid Position: {result['transcript']['aa_position']}")
            
            # DNA Analysis
            print("\n🧬 DNA SEQUENCE ANALYSIS")
            print("-" * 70)
            dna = result['dna_score']
            print(f"  Reference PLL: {dna['ref_pll']:.4f}")
            print(f"  Alternate PLL: {dna['alt_pll']:.4f}")
            print(f"  Delta Score: {dna['delta_score']:.4f}")
            print(f"  Interpretation: {dna['interpretation'].upper()}")
            
            # Protein Analysis
            print("\n🔬 PROTEIN ANALYSIS")
            print("-" * 70)
            protein = result['protein_analysis']
            print(f"  Mutation Type: {protein['mutation_type'].upper()}")
            print(f"  Amino Acid Change: {protein['ref_aa']} → {protein['alt_aa']} at position {protein['aa_position']}")
            print(f"  Reference Fragment: {protein['ref_fragment']}")
            print(f"  Altered Fragment: {protein['alt_fragment']}")
            print(f"\n  ESM-2 Scores:")
            print(f"    Reference AA Score: {protein['protein_score']['ref_score']:.4f}")
            print(f"    Alternate AA Score: {protein['protein_score']['alt_score']:.4f}")
            print(f"    Delta Score: {protein['protein_score']['delta_score']:.4f}")
            print(f"    Impact: {protein['protein_score']['impact'].upper()}")
            
            # Protein Function
            print("\n💊 PROTEIN FUNCTION")
            print("-" * 70)
            uniprot = result['uniprot']
            print(f"  Protein Name: {uniprot['protein_name']}")
            print(f"  Function: {uniprot['function']}")
            print(f"  Tissue Expression: {', '.join(uniprot['tissue_expression'])}")
            
            # ACMG Classification
            print("\n⚖️ ACMG CLASSIFICATION")
            print("-" * 70)
            acmg = result['acmg']
            print(f"  Classification: {acmg['classification']}")
            print(f"  Score: {acmg['score']:.1f}")
            print(f"  Summary: {acmg['summary']}")
            
            if acmg['evidence']:
                print(f"\n  Evidence Applied:")
                for criterion, descriptions in acmg['evidence'].items():
                    for desc in descriptions:
                        print(f"    • {criterion}: {desc}")
            
            # Clinical Interpretation
            print("\n🏥 CLINICAL INTERPRETATION")
            print("-" * 70)
            if "Pathogenic" in acmg['classification']:
                print("  This variant is likely disease-causing and may increase")
                print("  the risk for hereditary cancer syndromes. Genetic counseling")
                print("  and clinical correlation are recommended.")
            elif "Benign" in acmg['classification']:
                print("  This variant is likely not disease-causing and is probably")
                print("  a benign polymorphism. No clinical action recommended.")
            else:
                print("  This variant has uncertain clinical significance. Further")
                print("  studies, family segregation analysis, and functional assays")
                print("  may be needed to determine its clinical relevance.")
            
            print("\n" + "="*70)
            print("✅ END OF REPORT")
            print("="*70)
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    asyncio.run(test_detailed())