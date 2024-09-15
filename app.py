from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import google.generativeai as genai
import os
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        api_key = request.form['api_key']
        genai.configure(api_key=api_key)
        # Store API key securely (e.g., in session)
        return render_template('upload.html')
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return generate_html(file_path)

def extract_name(text):
    # Simple regex to find a name (assuming the name is the first line in the resume)
    match = re.search(r'^[A-Z][a-z]*\s[A-Z][a-z]*', text, re.MULTILINE)
    if match:
        return match.group(0).replace(' ', '_')
    return 'resume'

def generate_html(file_path):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        sample_file = genai.upload_file(path=file_path)
        
        prompt = "Extract the name and convert this LinkedIn PDF resume to HTML format. Ensure the output is clean and readable."
        response = model.generate_content([prompt, sample_file])
        
        text_content = response.text
        name = extract_name(text_content)
        html_filename = f"{name}.html"
        
        # Save HTML content to a file
        with open(html_filename, 'w') as f:
            f.write(text_content)
        
        return send_file(html_filename, as_attachment=True)
    except google.api_core.exceptions.GoogleAPIError as e:
        flash(f"An error occurred: {e.message}")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
