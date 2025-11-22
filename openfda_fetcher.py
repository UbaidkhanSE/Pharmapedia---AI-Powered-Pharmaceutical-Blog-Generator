import requests
import json
from pathlib import Path


OUTPUT_DIR = r"C:\BlogAgent\data"
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def fetch_drug_data(drug_name):
    """Fetch drug data from OpenFDA API"""
    print(f"Fetching data for: {drug_name}")
    
    url = f"https://api.fda.gov/drug/label.json?search={drug_name}&limit=1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            print(f"No data found for {drug_name}")
            return None
        
        result = data['results'][0]
        
        drug_info = {
            "name": drug_name,
            "brand_names": result.get('openfda', {}).get('brand_name', ['N/A'])[0],
            "indications": result.get('indications_and_usage', ['N/A'])[0][:300],
            "warnings": result.get('warnings', ['N/A'])[0][:200],
            "dosage": result.get('dosage_and_administration', ['N/A'])[0][:200],
            "side_effects": result.get('adverse_reactions', ['N/A'])[0][:200]
        }
        
        print(f"Success: {drug_info['brand_names']}")
        return drug_info
    
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_drug_data(drug_info, filename=None):
    """Save drug data to JSON"""
    if filename is None:
        filename = f"{drug_info['name'].lower()}.json"
    
    filepath = Path(OUTPUT_DIR) / filename
    
    with open(filepath, 'w') as f:
        json.dump(drug_info, f, indent=2)
    
    print(f"Saved: {filepath}\n")
    return filepath


def main():
    drugs = ["aspirin", "ibuprofen", "metformin", "lisinopril", "amoxicillin"]
    
    for drug in drugs:
        data = fetch_drug_data(drug)
        
        if data:
            save_drug_data(data)


if __name__ == "__main__":
    main()