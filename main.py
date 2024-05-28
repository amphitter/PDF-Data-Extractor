from flask import Flask, request, jsonify
from pdf2image import convert_from_path
import openai
import os
import base64
from io import BytesIO
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load configuration from environment variables or configuration files
openai.api_key = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

# Ensure the temp directory exists
TEMP_DIR = 'temp'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Allowed document types
ALLOWED_DOCUMENT_TYPES = ['SoF', 'Tariffs', 'Invoices', 'Statement of Account']

# Maximum file size (10 MB in this example)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@app.route('/extract', methods=['POST'])
def extract():
    try:
        # Validate request
        if 'file' not in request.files or 'document_type' not in request.form:
            return jsonify({"error": "File and document_type are required"}), 400
        
        file = request.files['file']
        document_type = request.form['document_type']

        # Validate file size
        if file.content_length > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds the limit"}), 400

        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Validate file type (assuming only PDFs are allowed)
        if not filename.lower().endswith('.pdf'):
            return jsonify({"error": "Invalid file type. Only PDF files are allowed"}), 400
        
        # Validate the document type
        if document_type not in ALLOWED_DOCUMENT_TYPES:
            return jsonify({"error": "Invalid document type"}), 400
        
        # Save PDF file temporarily
        pdf_path = os.path.join(TEMP_DIR, filename)
        file.save(pdf_path)
        
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            # Prepare images for ChatGPT
            image_data = [image_to_data(image) for image in images]
            
            # Get the prompt and JSON format for the document type
            prompt, output_format = get_prompt_and_format(document_type)
            
            # Query ChatGPT
            response = query_chatgpt(image_data, prompt)
            
            # Process and return JSON response
            return jsonify({"output": response})
        
        finally:
            # Clean up the saved PDF file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    except Exception as e:
        logging.error(f"Error during extraction: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred during processing"}), 500

def image_to_data(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def get_prompt_and_format(document_type):
    prompts = {
        'SoF': ('Extract fields from the Statement of Facts and provide a structured JSON output.', '{"field1": "", "field2": ""}'),
        'Tariffs': ('Extract tariff information and provide a structured JSON output.', '{"tariff1": "", "tariff2": ""}'),
        'Invoices': ('Extract invoice details and provide a structured JSON output.', '{"invoice_number": "", "date": "", "total": ""}'),
        'Statement of Account': ('Extract account statement details and provide a structured JSON output.', '{"account_number": "", "balance": "", "transactions": []}')
    }
    return prompts.get(document_type, ("", ""))

def query_chatgpt(images, prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "user", "content": prompt})
    for img in images:
        messages.append({"role": "user", "content": f"Image data: {img}"})
    
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages
    )
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(debug=True)
