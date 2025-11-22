import json
from pathlib import Path
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch
import requests

OUTPUT_DIR = r"C:\BlogAgent\output"
MODELS_DIR = r"C:\BlogAgent\models"

Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


class OpenFDAManager:
    @staticmethod
    def fetch_detailed_drug_data(drug_name):
        """Fetch comprehensive drug data from OpenFDA API"""
        print(f"Fetching detailed data for {drug_name} from OpenFDA...\n")
        
        try:
            url = f"https://api.fda.gov/drug/label.json?search={drug_name}&limit=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'results' not in data or len(data['results']) == 0:
                return None
            
            result = data['results'][0]
            
            drug_info = {
                "name": drug_name,
                "brand_names": result.get('openfda', {}).get('brand_name', ['N/A'])[0],
                "manufacturer": result.get('openfda', {}).get('manufacturer_name', ['N/A'])[0],
                "indications": result.get('indications_and_usage', ['N/A'])[0][:400],
                "dosage": result.get('dosage_and_administration', ['N/A'])[0][:400],
                "side_effects": result.get('adverse_reactions', ['N/A'])[0][:400],
                "warnings": result.get('warnings', ['N/A'])[0][:400],
                "contraindications": result.get('contraindications', ['N/A'])[0][:200],
                "mechanism": result.get('mechanism_of_action', ['N/A'])[0][:200] if 'mechanism_of_action' in result else "N/A"
            }
            
            return drug_info
        
        except Exception as e:
            print(f"API Error: {e}\n")
            return None


class ModelManager:
    def __init__(self):
        print("Loading TinyLlama...\n")
        self.text_pipe = pipeline("text-generation", model=f"{MODELS_DIR}\\tinyllama", device=-1)
        
        print("Loading Stable Diffusion...\n")
        self.image_pipe = StableDiffusionPipeline.from_pretrained(f"{MODELS_DIR}\\stable_diffusion")
        self.image_pipe.enable_attention_slicing()
        self.image_pipe = self.image_pipe.to("cpu")
    
    def generate_text(self, prompt):
        result = self.text_pipe(prompt, max_new_tokens=300, truncation=True, do_sample=True, temperature=0.7)
        return result[0]["generated_text"]
    
    def generate_image(self, prompt):
        with torch.no_grad():
            image = self.image_pipe(prompt, height=512, width=512, num_inference_steps=35, guidance_scale=7.5).images[0]
        return image


class BlogGenerator:
    def __init__(self):
        self.fda_manager = OpenFDAManager()
        self.model_manager = ModelManager()
    
    def create_detailed_text_prompt(self, drug_info, title):
        """Create intelligent prompt using detailed FDA data"""
        prompt = f"""Write professional pharmaceutical blog about {drug_info['name']}.

Title: {title}

Uses: {drug_info['indications'][:200]}
Dosage: {drug_info['dosage'][:150]}
Side Effects: {drug_info['side_effects'][:150]}
Warnings: {drug_info['warnings'][:100]}

Write engaging blog with:
- Introduction
- What is it
- Benefits and uses
- Dosage
- Side effects
- Warnings
- Conclusion

Blog:"""
        
        return prompt
    
    def create_intelligent_image_prompt(self, drug_info, title):
        """Create image prompt based on drug characteristics"""
        drug_name = drug_info['name']
        brand = drug_info['brand_names']
        
        title_lower = title.lower()
        
        base = f"professional pharmaceutical medical illustration {drug_name}"
        
        if any(word in title_lower for word in ['benefit', 'help', 'treat']):
            return f"{base} therapeutic treatment healthcare clinical professional"
        elif any(word in title_lower for word in ['safe', 'safety', 'warning']):
            return f"{base} warning safety precaution clinical professional"
        elif any(word in title_lower for word in ['mechanism', 'how']):
            return f"{base} molecular scientific illustration clinical"
        elif any(word in title_lower for word in ['dosage', 'dose', 'administration']):
            return f"{base} tablets capsules medication administration clinical"
        else:
            return f"{base} medication pharmaceutical clinical professional medical"
    
    def generate(self, drug_name, custom_title=None):
        print("="*80)
        print("STARTING BLOG GENERATION")
        print("="*80 + "\n")
        
        drug_info = self.fda_manager.fetch_detailed_drug_data(drug_name)
        
        if not drug_info:
            return {"status": "error", "message": f"Drug '{drug_name}' not found in FDA database"}
        
        title = custom_title if custom_title else f"Complete Medical Guide to {drug_name}"
        
        print(f"Drug: {drug_info['name']}")
        print(f"Brand: {drug_info['brand_names']}")
        print(f"Title: {title}\n")
        
        print("-"*80)
        print("GENERATING BLOG CONTENT...")
        print("-"*80 + "\n")
        
        text_prompt = self.create_detailed_text_prompt(drug_info, title)
        blog_text = self.model_manager.generate_text(text_prompt)
        blog_content = blog_text.split("Blog:")[-1].strip() if "Blog:" in blog_text else blog_text.strip()
        
        print("✓ Blog content generated\n")
        
        print("-"*80)
        print("GENERATING FEATURED IMAGE...")
        print("-"*80 + "\n")
        
        image_prompt = self.create_intelligent_image_prompt(drug_info, title)
        print(f"Image Prompt: {image_prompt}\n")
        image = self.model_manager.generate_image(image_prompt)
        
        print("✓ Image generated\n")
        
        print("-"*80)
        print("SAVING FILES...")
        print("-"*80 + "\n")
        
        drug_lower = drug_name.lower()
        
        image_filename = f"{drug_lower}_blog.png"
        image_path = Path(OUTPUT_DIR) / image_filename
        image.save(image_path)
        
        json_filename = f"{drug_lower}_blog.json"
        json_path = Path(OUTPUT_DIR) / json_filename
        
        blog_data = {
            "drug_name": drug_info['name'],
            "brand_names": drug_info['brand_names'],
            "manufacturer": drug_info['manufacturer'],
            "title": title,
            "blog_content": blog_content,
            "image_filename": image_filename,
            "image_path": str(image_path),
            "fda_data": {
                "indications": drug_info['indications'][:200],
                "dosage": drug_info['dosage'][:200],
                "warnings": drug_info['warnings'][:200]
            },
            "status": "success"
        }
        
        with open(json_path, 'w') as f:
            json.dump(blog_data, f, indent=2)
        
        return blog_data


def display_result(result):
    if result["status"] == "error":
        print(f"\n❌ ERROR: {result['message']}\n")
        return
    
    print("\n" + "="*80)
    print("✓ PROFESSIONAL BLOG GENERATED SUCCESSFULLY")
    print("="*80 + "\n")
    
    print(f"Drug: {result['drug_name']}")
    print(f"Brand: {result['brand_names']}")
    print(f"Manufacturer: {result.get('manufacturer', 'N/A')}")
    print(f"Title: {result['title']}\n")
    
    print("-"*80)
    print("BLOG CONTENT:")
    print("-"*80 + "\n")
    print(result['blog_content'] + "\n")
    
    print("="*80)
    print("GENERATED FILES:")
    print("="*80)
    print(f"✓ Image: {result['image_path']}")
    json_file = Path(result['image_path']).parent / f"{result['drug_name'].lower()}_blog.json"
    print(f"✓ JSON Data: {json_file}")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print(" "*15 + "PHARMACEUTICAL BLOG GENERATOR WITH FDA DATA")
    print("="*80 + "\n")
    
    generator = BlogGenerator()
    
    drug_name = input("Enter drug name: ").strip()
    custom_title = input("Enter blog title (or press Enter for default): ").strip()
    
    if not custom_title:
        custom_title = None
    
    print("\nProcessing... This may take 3-4 minutes\n")
    
    result = generator.generate(drug_name, custom_title)
    display_result(result)