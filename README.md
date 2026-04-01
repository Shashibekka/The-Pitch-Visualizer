# The Pitch Visualizer

## Vision & Context
This project is an automated storyboard generator designed to help sales teams turn narrative text into compelling visual aids. It takes a block of text, segments it into logical scenes, engineers descriptive prompts, and generates a cohesive visual storyboard using AI.

## Technical Stack
* **Language:** Python
* **Web Framework:** Flask
* **Text Segmentation:** NLTK (Natural Language Toolkit)
* **Image Generation:** Hugging Face Inference API (Stable Diffusion XL)

## Setup & Execution Instructions
1. Clone this repository.
2. Create a virtual environment and activate it.
3. Install the dependencies: `pip install -r requirements.txt`
4. Obtain a free API token from [Hugging Face](https://huggingface.co/settings/tokens).
5. Open `app.py` and replace `"YOUR_HUGGING_FACE_TOKEN_HERE"` with your actual token.
6. Run the application: `python app.py`
7. Open a web browser and navigate to `http://127.0.0.1:5000`

## Design Choices & Methodology
**Intelligent Prompt Engineering:** To satisfy the requirement of enhancing the base text, the application programmatically appends a specific style string to every segmented sentence. For example, a raw sentence is transformed into: `"{sentence}, highly detailed storyboard sketch, cinematic lighting, digital art, clear composition"`. 

This guarantees that the Hugging Face model receives enough visual context to generate high-quality images, while also enforcing a level of artistic consistency across the generated storyboard panels without requiring manual user input.