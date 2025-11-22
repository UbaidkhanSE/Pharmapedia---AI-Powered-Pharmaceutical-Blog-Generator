import google.generativeai as genai
import requests
from datetime import datetime
from pathlib import Path
import logging
import html2text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEVTO_API_KEY = os.getenv("DEVTO_API_KEY")
MODEL_NAME = "gemini-2.5-flash"

genai.configure(api_key=GEMINI_API_KEY)


class BlogGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)
        
    def generate_content(self, topic):
        """Generate blog content with clear structure and headings"""
        logger.info(f"Generating blog content for topic: {topic}")
        
        prompt = f"""Create a comprehensive professional blog post about '{topic}'. 
        
Use this EXACT structure with clear markdown headings:


# Introduction to {topic}
Write 2-3 engaging paragraphs introducing the topic.


## Key Concept 1: [Specific heading about main idea]
Write 2-3 detailed paragraphs explaining this concept with examples.


## Key Concept 2: [Specific heading about another important aspect]
Write 2-3 detailed paragraphs with practical insights.


## Key Concept 3: [Specific heading about third important aspect]
Write 2-3 detailed paragraphs with expert perspective.


## Practical Applications and Benefits
Write 2-3 paragraphs on how this applies in real-world scenarios.


## Conclusion and Key Takeaways
Summarize the main points and provide concluding thoughts.


Total length: 1500-2000 words. Use clear, professional language with proper spacing between sections."""
        
        try:
            response = self.model.generate_content(prompt)
            logger.info("Blog content generated successfully")
            return response.text
        except Exception as error:
            logger.error(f"Error generating content: {error}")
            raise
    
    def get_image_urls(self, topic, count=4):
        """Get quality image URLs using reliable service"""
        logger.info(f"Preparing image URLs for: {topic}")
        
        images = []
        
        for i in range(count):
            url = f"https://picsum.photos/1200/700?random={i}&t={datetime.now().timestamp()}"
            images.append(url)
        
        logger.info(f"Prepared {len(images)} image URLs")
        return images
    
    def parse_content_with_headings(self, content, images):
        """Convert markdown content to HTML with proper headings and images"""
        lines = content.split('\n')
        html_sections = []
        image_index = 0
        section_count = 0
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            if line.startswith('# '):
                heading = line.replace('# ', '')
                html_sections.append(f'<h1>{heading}</h1>')
                section_count += 1
                
            elif line.startswith('## '):
                heading = line.replace('## ', '')
                html_sections.append(f'<h2>{heading}</h2>')
                section_count += 1
                
                if section_count > 1 and section_count % 2 == 0 and image_index < len(images):
                    html_sections.append(f'''
                    <div class="section-image">
                        <img src="{images[image_index]}" alt="Illustration" class="blog-img">
                    </div>
                    ''')
                    image_index += 1
                    
            elif line.startswith('### '):
                heading = line.replace('### ', '')
                html_sections.append(f'<h3>{heading}</h3>')
                
            else:
                if line:
                    html_sections.append(f'<p>{line}</p>')
        
        return '\n'.join(html_sections)
    
    def create_html(self, topic, content, image_urls):
        """Create professional, well-structured HTML blog"""
        logger.info("Creating HTML document")
        
        timestamp = datetime.now().strftime("%B %d, %Y")
        content_html = self.parse_content_with_headings(content, image_urls)
        
        featured_image = f'<img src="{image_urls[0]}" alt="{topic}" class="featured-img">'
        
        css_styles = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', 'Segoe UI', serif;
            line-height: 1.9;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 40px 20px;
        }
        
        .wrapper {
            max-width: 850px;
            margin: 0 auto;
            background: white;
            padding: 60px 50px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        
        header {
            margin-bottom: 50px;
            border-bottom: 4px solid #3498db;
            padding-bottom: 30px;
        }
        
        h1 {
            font-size: 3.2em;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.2;
            font-weight: 700;
        }
        
        .date {
            color: #7f8c8d;
            font-size: 1em;
            font-style: italic;
            letter-spacing: 0.5px;
        }
        
        .featured-img {
            width: 100%;
            height: auto;
            max-height: 500px;
            border-radius: 10px;
            margin: 40px 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            object-fit: cover;
        }
        
        .blog-content {
            font-size: 1.15em;
            line-height: 2;
            color: #34495e;
        }
        
        h2 {
            font-size: 2.2em;
            color: #2980b9;
            margin-top: 50px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
            font-weight: 700;
        }
        
        h3 {
            font-size: 1.6em;
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        p {
            margin-bottom: 22px;
            text-align: justify;
            text-indent: 2em;
            color: #455a64;
            line-height: 2;
        }
        
        .section-image {
            margin: 40px 0;
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .blog-img {
            width: 100%;
            height: auto;
            max-height: 400px;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
            object-fit: cover;
        }
        
        footer {
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.95em;
        }
        
        @media (max-width: 768px) {
            .wrapper {
                padding: 30px 20px;
            }
            
            h1 {
                font-size: 2.2em;
            }
            
            h2 {
                font-size: 1.8em;
            }
            
            h3 {
                font-size: 1.3em;
            }
            
            p {
                font-size: 1em;
                text-indent: 1.5em;
            }
        }
        """
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} - Professional Blog</title>
    <style>
{css_styles}
    </style>
</head>
<body>
    <div class="wrapper">
        <header>
            <h1>{topic}</h1>
            <div class="date">Published on {timestamp}</div>
        </header>
        
        {featured_image}
        
        <article class="blog-content">
            {content_html}
        </article>
        
        <footer>
            <p>Generated using Gemini AI. All rights reserved. {datetime.now().year}</p>
        </footer>
    </div>
</body>
</html>"""
        
        logger.info("HTML document created successfully")
        return html_template
    
    def save_blog(self, topic, html_content):
        """Save blog to file"""
        filename = f"blog_{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = Path(filename)
        
        try:
            filepath.write_text(html_content, encoding='utf-8')
            logger.info(f"Blog saved to {filepath}")
            return str(filepath)
        except Exception as error:
            logger.error(f"Error saving blog: {error}")
            raise
    
    def publish_to_devto(self, topic, html_content):
        """Publish blog content to dev.to using API"""
        logger.info("Converting HTML to Markdown for dev.to publishing")
        markdown_content = html2text.html2text(html_content)  # convert HTML to Markdown
        
        url = "https://dev.to/api/articles"
        
        headers = {
            "api-key": DEVTO_API_KEY,
            "Content-Type": "application/json"
        }
        
        data = {
            "article": {
                "title": topic,
                "published": True,
                "body_markdown": markdown_content,
                "tags": ["blog", "ai", "development"],
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            url_posted = response.json().get("url", "Unknown URL")
            logger.info(f"Published successfully on dev.to: {url_posted}")
            print(f"Published successfully on dev.to: {url_posted}")
            return url_posted
        else:
            logger.error(f"Failed to publish: {response.status_code} - {response.text}")
            print(f"Failed to publish: {response.status_code} - {response.text}")
            return None
    
    def generate_blog(self, topic):
        """Main method to generate complete blog"""
        logger.info(f"Starting blog generation for: {topic}")
        
        try:
            content = self.generate_content(topic)
            images = self.get_image_urls(topic, count=4)
            
            logger.info("Creating HTML blog with proper structure")
            html_blog = self.create_html(topic, content, images)
            
            filepath = self.save_blog(topic, html_blog)
            
            publish_choice = input("Do you want to publish this blog to dev.to? (yes/no): ").strip().lower()
            if publish_choice == 'yes':
                self.publish_to_devto(topic, html_blog)
            else:
                print("Skipping publishing to dev.to.")
            
            logger.info(f"Blog generation completed")
            logger.info(f"File saved at: {filepath}")
            
            return filepath
        
        except Exception as error:
            logger.error(f"Failed to generate blog: {error}")
            raise


def main():
    """Main entry point"""
    try:
        topic = input("Enter blog topic: ").strip()
        
        if not topic:
            logger.warning("No topic provided")
            return
        
        generator = BlogGenerator()
        filepath = generator.generate_blog(topic)
        
        print(f"\nBlog generated successfully!")
        print(f"Saved at: {filepath}")
        print(f"Open the file in your browser to view.")
        
    except Exception as error:
        logger.error(f"Application error: {error}")


if __name__ == "__main__":
    main()
