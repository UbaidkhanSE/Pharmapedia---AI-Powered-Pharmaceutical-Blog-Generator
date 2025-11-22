Pharmapedia - AI-Powered Pharmaceutical Blog Generator
Pharmapedia is an intelligent blog generation system that combines FDA drug data with AI models to automatically create professional pharmaceutical blogs with generated images.
Features

FDA Data Integration: Real-time drug information fetching from OpenFDA API
AI-Powered Content Generation: Uses TinyLlama for intelligent blog text generation
Image Generation: Automatically generates relevant pharmaceutical images using Stable Diffusion
Modern Web Interface: Beautiful, responsive frontend for easy interaction
RESTful API: FastAPI backend for seamless integration
Structured Output: JSON data with organized drug information and generated content

Tech Stack
ComponentTechnologyBackendFastAPI, Python 3.8+FrontendHTML5, CSS3, JavaScriptAI ModelsTinyLlama (text), Stable Diffusion (images)Data SourceOpenFDA APIML FrameworkHugging Face Transformers, DiffusersAPI ClientRequests
📋 Prerequisites
Before you begin, ensure you have the following installed:

Python 3.9 or higher
pip or conda package manager
8GB+ RAM (recommended for model inference)
10GB+ disk space (for models)
CUDA-capable GPU (optional but recommended)

Installation
1. Clone or Download the Project
bashcd BlogAgent
2. Create Virtual Environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bashpip install fastapi uvicorn transformers diffusers torch requests pydantic python-multipart
4. Create Required Directories
bashmkdir models
mkdir output
mkdir data
5. Download Models
Download the required models and place them in the models/ directory:

TinyLlama: models/tinyllama/
Stable Diffusion: models/stable_diffusion/

Alternatively, the models will auto-download on first run (may take 10-15 minutes).
Usage
Starting the Server
bashpython main.py
The API will be available at http://127.0.0.1:8000
API Endpoints
Generate Blog
POST /generate-blog
Request body:
json{
  "drug_name": "aspirin",
  "title": "Complete Guide to Aspirin"
}
Response:
json{
  "status": "success",
  "drug_name": "Aspirin",
  "brand_names": "Bayer",
  "title": "Complete Guide to Aspirin",
  "blog_content": "...",
  "image_filename": "aspirin_blog.png",
  "image_path": "C:\\BlogAgent\\output\\aspirin_blog.png",
  "fda_data": {
    "indications": "...",
    "dosage": "...",
    "warnings": "..."
  }
}
Home Endpoint
GET /
Returns API information and version.
Serve Images
GET /images/{filename}
Retrieves generated images from the output directory.
Web Interface
Open index.html in your browser to access the Pharmapedia web interface:

Enter a drug name (e.g., "Aspirin", "Ibuprofen")
Optionally provide a custom blog title
Click "Generate Blog"
View the generated content in multiple tabs:

Blog Content: AI-generated pharmaceutical blog
Image: Generated featured image
FDA Data: Structured drug information



Command Line Usage
Use the Python script directly:
bashpython rag_agent.py
Follow the prompts to enter:

Drug name
Custom blog title (optional)

Output Files
Each generated blog produces two files:
JSON File: {drug_name}_blog.json
json{
  "drug_name": "Aspirin",
  "brand_names": "Bayer",
  "title": "Complete Medical Guide to Aspirin",
  "blog_content": "...",
  "image_filename": "aspirin_blog.png",
  "fda_data": { ... },
  "status": "success"
}
Image File: {drug_name}_blog.png
Generated pharmaceutical illustration (512x512px)
How It Works
1. Data Fetching

Queries OpenFDA API for drug information
Extracts indications, dosage, side effects, warnings, and contraindications

2. Content Generation

Creates intelligent prompts based on FDA data
Uses TinyLlama to generate professional blog content
Adapts tone and structure based on context

3. Image Generation

Analyzes blog title to determine image context
Generates contextual prompts for Stable Diffusion
Creates professional pharmaceutical illustrations

4. Output Assembly

Combines all elements into structured JSON
Saves images in high quality
Stores metadata for future reference

⚙️ Configuration
Edit the following in rag_agent.py:
pythonOUTPUT_DIR = r"C:\BlogAgent\output"      # Output directory
MODELS_DIR = r"C:\BlogAgent\models"      # Models directory
Edit API settings in main.py:
pythonapp = FastAPI(title="Pharmapedia API")
OUTPUT_DIR = Path(r"C:\BlogAgent\output")
🔧 Performance Optimization

Reduce Image Steps: Lower num_inference_steps in generate_image() for faster generation (trade-off with quality)
Use GPU: Install CUDA and set device to "cuda" instead of "cpu"
Batch Processing: Generate multiple blogs sequentially
Model Quantization: Use quantized models for faster inference

Troubleshooting
Models Not Loading
Error: Model not found
Solution: Download models to models/ directory or let them auto-download on first run.
API Connection Error
Error: Could not connect to API
Solution: Ensure FastAPI server is running on http://127.0.0.1:8000
Out of Memory
RuntimeError: CUDA out of memory
Solution: Use CPU mode or reduce model precision. Edit generate_image():
pythonself.image_pipe = self.image_pipe.to("cpu")
Drug Not Found
Drug 'xyz' not found in FDA database
Solution: Try alternative drug names or verify the drug exists on OpenFDA database.
 Example Workflow
pythonfrom rag_agent import BlogGenerator

generator = BlogGenerator()
result = generator.generate("metformin", "Managing Diabetes with Metformin")

if result["status"] == "success":
    print(f"Blog generated: {result['title']}")
    print(f"Image saved: {result['image_path']}")
Security Considerations

FDA API is rate-limited (requests per second may apply)
No sensitive user data is stored
Generated content is for informational purposes only
Always verify medical information with official sources

Legal Disclaimer
This tool generates content for informational purposes only. Generated blogs should not be used as medical advice. Always consult with healthcare professionals for medical decisions.
Contributing
Feel free to extend Pharmapedia with:

Additional data sources
Different AI models
Enhanced UI features
Performance optimizations

License
This project is open source and available for educational and commercial use.
Resources

OpenFDA API Documentation
Hugging Face Transformers
Stable Diffusion
FastAPI Documentation

Support
For issues or questions:

Check the Troubleshooting section
Review FastAPI logs for backend errors
Check browser console for frontend errors
Verify API endpoint connectivity

Features Coming Soon

 Batch blog generation
 Multiple language support
 Custom branding options
 Database integration for blog history
 Advanced content customization
 SEO optimization features
 Export to multiple formats (PDF, Markdown, HTML)
