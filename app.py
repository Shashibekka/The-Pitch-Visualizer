import os
import uuid
import time
import requests
from flask import Flask, render_template, request, url_for
import nltk

# Download NLTK sentence tokenizer data (only runs once)
nltk.download('punkt')
nltk.download('punkt_tab')

app = Flask(__name__)

# --- CONFIGURATION ---
HF_API_TOKEN = "YOUR_HUGGING_FACE_TOKEN_HERE" # Paste your token here

# Using Stable Diffusion XL on the new Hugging Face router
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Accept": "image/jpeg"
}

# Ensure the images directory exists
os.makedirs("static/images", exist_ok=True)

def generate_image(prompt, filename):
    """Sends a request to Hugging Face and saves the image."""
    payload = {"inputs": prompt}
    
    # The free API sometimes needs a moment to load the model. 
    for attempt in range(5):
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            filepath = os.path.join("static/images", filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            return True
        elif response.status_code == 503:
            print(f"Model is loading... attempt {attempt + 1}/5. Waiting 20 seconds.")
            time.sleep(20) 
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            break
    return False

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_text = request.form.get('narrative')
    selected_style = request.form.get('style')
    
    if not user_text:
        return "Please provide some text.", 400

    # 1. Narrative Segmentation
    sentences = nltk.tokenize.sent_tokenize(user_text)
    storyboard_data = []

    # Dictionary of heavy style modifiers optimized for SDXL
    style_prompts = {
        "cinematic": "cinematic film still, 8k resolution, highly detailed, dramatic lighting, photorealistic, depth of field",
        "sketch": "professional storyboard pencil sketch, black and white, rough outlines, expressive lines, studio illustration",
        "comic": "vibrant comic book panel, cel shading, ink outlines, graphic novel style, pop art colors",
        "watercolor": "beautiful watercolor painting, soft edges, dreamy atmosphere, vivid colors, artistic masterpiece"
    }
    
    # Fallback to cinematic if nothing is selected
    modifier = style_prompts.get(selected_style, style_prompts["cinematic"])

    for sentence in sentences:
        if len(sentence.strip()) < 5:
            continue
            
        # 2. Intelligent Prompt Engineering
        enhanced_prompt = f"{sentence}. {modifier}, clear composition, focused subject."
        
        # 3. Image Generation
        image_filename = f"{uuid.uuid4().hex}.jpg"
        success = generate_image(enhanced_prompt, image_filename)
        
        if success:
            storyboard_data.append({
                "text": sentence,
                "image_url": url_for('static', filename=f'images/{image_filename}')
            })
        else:
            storyboard_data.append({
                "text": sentence,
                "image_url": "" 
            })

    # 4. Storyboard Presentation
    return render_template('result.html', storyboard=storyboard_data)

if __name__ == '__main__':
    app.run(debug=True)