from flask import Flask, request, render_template, send_file, flash, redirect, url_for
import google.generativeai as genai
import google.api_core.exceptions  # Import the exceptions module
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

def extract_name_and_html(text):
    # Extract the name and HTML content from the text
    name_match = re.search(r'##\s([A-Za-z\s]+)', text)
    name = name_match.group(1).replace(' ', '_') if name_match else 'resume'
    
    html_match = re.search(r'```html\n(.*)```', text, re.DOTALL)
    html_content = html_match.group(1) if html_match else ''
    
    return name, html_content

def generate_html(file_path):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        sample_file = genai.upload_file(path=file_path)
        
        prompt = "Extract the name and convert this LinkedIn PDF resume to HTML format. Ensure the output is clean and readable."
        response = model.generate_content([prompt, sample_file])
        
        # Debug: Print the response to check the content
        print("API Response:", response)
        
        text_content = response.text
        
        # Extract the name and HTML content
        name, html_content = extract_name_and_html(text_content)
        
        # Debug: Print the extracted name and HTML content
        print("Extracted Name:", name)
        print("HTML Content:", html_content)
        
        html_filename = f"{name}.html"
        
        # Save HTML content to a file
        with open(html_filename, 'w') as f:
            f.write(html_content)
        
        # Debug: Print the path of the generated HTML file
        print("Generated HTML File:", html_filename)
        
        return send_file(html_filename, as_attachment=True)
    except google.api_core.exceptions.GoogleAPIError as e:
        flash(f"An error occurred with the Google API: {e.message}")
        print(f"Google API Error: {e.message}")
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}")
        print(f"Unexpected Error: {str(e)}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
