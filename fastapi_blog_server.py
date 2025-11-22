from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import sys

sys.path.append(r"C:\BlogAgent")
from rag_agent import BlogGenerator

app = FastAPI(title="Pharmapedia API")

OUTPUT_DIR = Path(r"C:\BlogAgent\output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=OUTPUT_DIR), name="images")

generator = BlogGenerator()

class BlogRequest(BaseModel):
    drug_name: str
    title: str = None

@app.post("/generate-blog")
def generate_blog(request: BlogRequest):
    return generator.generate(request.drug_name, request.title)

@app.get("/")
def home():
    return {"message": "Pharmapedia Blog Generator API", "version": "1.0"}