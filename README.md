# LinkedIn PDF to HTML Resume Converter

This Flask application converts LinkedIn PDF resumes to HTML format using the Gemini API.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```python
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```python
   pip install -r requirements.txt
   ```
4. Set up a Gemini API key at [Google AI Studio](https://makersuite.google.com/)
5. Run the application:
   ```python
   python app.py
   ```

## Usage

1. Open the application in your web browser
2. Enter your Gemini API key
3. Upload your LinkedIn PDF resume
4. Download the generated HTML file

## How it works

The application uses the Gemini API to extract text from the uploaded PDF and generate an HTML version of the resume. It leverages Gemini's natural language processing capabilities to structure the content appropriately.

## Deployment

To deploy on platforms like Vercel or GitHub Pages, consider using a serverless function approach or choose a hosting platform that supports Python web applications.
