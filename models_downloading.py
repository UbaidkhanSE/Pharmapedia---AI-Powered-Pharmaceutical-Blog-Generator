import os
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from diffusers import StableDiffusionPipeline


BASE_PATH = r"C:\BlogAgent\models"
os.makedirs(BASE_PATH, exist_ok=True)

MODELS = {
    "tinyllama": {
        "name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "path": os.path.join(BASE_PATH, "tinyllama"),
        "size": "2.2 GB"
    },
    "stable_diffusion": {
        "name": "runwayml/stable-diffusion-v1-5",
        "path": os.path.join(BASE_PATH, "stable_diffusion"),
        "size": "4 GB"
    }
}


def print_section(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")


def download_tinyllama():
    print_section("Downloading TinyLlama 1.1B")
    
    model_info = MODELS["tinyllama"]
    os.makedirs(model_info["path"], exist_ok=True)
    
    try:
        print("Step 1: Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_info["name"])
        tokenizer.save_pretrained(model_info["path"])
        print("Tokenizer saved")
        
        print("Step 2: Downloading model weights...")
        model = AutoModelForCausalLM.from_pretrained(
            model_info["name"],
            dtype=torch.float32
        )
        model.save_pretrained(model_info["path"])
        
        print(f"Success: {model_info['path']}")
        print(f"Size: {model_info['size']}\n")
        return True
        
    except Exception as e:
        print(f"Failed: {e}\n")
        return False


def download_stable_diffusion():
    print_section("Downloading Stable Diffusion v1.5")
    
    model_info = MODELS["stable_diffusion"]
    os.makedirs(model_info["path"], exist_ok=True)
    
    try:
        print("Step 1: Downloading image model...")
        print("This is large, it will take 5-10 minutes...\n")
        
        pipeline = StableDiffusionPipeline.from_pretrained(
            model_info["name"],
            dtype=torch.float32
        )
        pipeline.save_pretrained(model_info["path"])
        
        print(f"\nSuccess: {model_info['path']}")
        print(f"Size: {model_info['size']}\n")
        return True
        
    except Exception as e:
        print(f"Failed: {e}\n")
        return False


def get_dir_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except:
        pass
    return total


def verify_downloads():
    print_section("Verification")
    
    for key, model in MODELS.items():
        path = model["path"]
        
        if os.path.exists(path):
            try:
                files = sum(1 for _ in Path(path).rglob('*') if _.is_file())
                size_gb = get_dir_size(path) / (1024**3)
                
                print(f"{key.upper()}")
                print(f"Path: {path}")
                print(f"Files: {files} | Size: {size_gb:.2f} GB")
                
                if size_gb > 0.5:
                    print("Status: Downloaded")
                else:
                    print("Status: Incomplete or empty")
                print()
            except Exception as e:
                print(f"{key.upper()} - Error: {e}\n")
        else:
            print(f"{key.upper()} - NOT FOUND\n")


def main():
    print_section("Model Downloader for BlogAgent")
    print(f"Target: {BASE_PATH}\n")
    
    print("This will download:")
    print("- TinyLlama 1.1B (text generation)")
    print("- Stable Diffusion v1.5 (image generation)")
    print("- Total size: ~6 GB")
    print("- Time: 15-20 minutes\n")
    
    input("Press Enter to start downloading...")
    
    text_ok = download_tinyllama()
    image_ok = download_stable_diffusion()
    
    verify_downloads()
    
    print_section("Status")
    if text_ok and image_ok:
        print("All models downloaded successfully!")
        print("Ready for blog generator")
    else:
        print("Some downloads failed. Check errors above.")


if __name__ == "__main__":
    main()