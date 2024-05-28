# PDF Data Extractor

This project is a Flask-based web application that extracts structured data from PDF documents using the OpenAI GPT-4 model. The application converts PDF pages to images, sends the images to the GPT-4 model along with a prompt, and returns the extracted information in JSON format.

## Features

- **PDF to Image Conversion**: Converts PDF pages to images.
- **Data Extraction**: Extracts structured data from images using OpenAI GPT-4.
- **Supports Multiple Document Types**: Handles various document types like Statements of Fact (SoF), Tariffs, Invoices, and Statements of Account.
- **File Size Validation**: Ensures the uploaded file does not exceed the maximum allowed size.
- **Error Handling**: Provides detailed error messages and logging.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key
- Required Python packages (see `requirements.txt`)

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/amphitter/pdf-data-extractor.git
    cd pdf-data-extractor
    ```

2. **Create a Virtual Environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory of the project and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the Application**:
    ```sh
    python app.py
    ```

## API Endpoint

### Extract Data from PDF

- **URL**: `/extract`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): The PDF file to be processed.
  - `document_type` (required): The type of document (e.g., 'SoF', 'Tariffs', 'Invoices', 'Statement of Account').

#### Example Request

```sh
curl -X POST http://127.0.0.1:5000/extract \
  -F "file=@path_to_your_pdf_file.pdf" \
  -F "document_type=Invoices"
```

#### Example Response

```json
{
  "output": {
    "invoice_number": "12345",
    "date": "2023-01-01",
    "total": "$1000.00"
  }
}
```

## Code Explanation

### Key Components

- **Flask App Initialization**:
  The Flask app is initialized and configured to use the OpenAI API key from the environment variables.

- **Temporary Directory Setup**:
  Ensures a temporary directory exists for saving uploaded PDF files.

- **API Endpoint**:
  The `/extract` endpoint handles the POST request, validates the input, converts the PDF to images, and sends the images to the GPT-4 model for data extraction.

- **Image Conversion**:
  Uses `pdf2image` to convert PDF pages to images.

- **Data Extraction**:
  Prepares a prompt based on the document type and sends the images and prompt to the GPT-4 model using `aiohttp` for asynchronous HTTP requests.

- **Error Handling**:
  Provides detailed error messages and logging for better traceability.

### Function Descriptions

- **extract()**:
  Main function for handling the `/extract` endpoint. Validates inputs, saves the PDF, converts it to images, sends the images to the GPT-4 model, and returns the extracted data in JSON format.

- **image_to_data(image)**:
  Converts a PIL image to a base64-encoded string.

- **get_prompt_and_format(document_type)**:
  Returns the appropriate prompt and expected JSON output format for the specified document type.

- **query_chatgpt(images, prompt)**:
  Sends the images and prompt to the GPT-4 model and returns the extracted data.

## Document Extraction API

This API extracts structured information from PDF documents. It uses the OpenAI GPT-4 model to analyze and interpret the content of PDF files converted into images. The API supports different document types such as Statements of Facts (SoF), Tariffs, Invoices, and Statements of Account.

## Features

- **Upload PDF**: Allows uploading PDF files for extraction.
- **Document Type Validation**: Validates the type of document being uploaded.
- **File Size Check**: Ensures the uploaded file does not exceed the maximum allowed size.
- **PDF to Image Conversion**: Converts each page of the PDF to an image.
- **Image Processing with OpenAI**: Sends images to the OpenAI GPT-4 model for extracting structured information.
- **Custom Prompts**: Uses specific prompts for different document types to tailor the extraction process.
- **Temporary File Handling**: Manages temporary files securely and efficiently.

## Setup

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/amphitter/pdf-data-extractor.git
cd pdf-data-extractor
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the application**:
    ```bash
    python app.py
    ```

## API Endpoints

### POST /extract

#### Description

Extracts structured information from an uploaded PDF document.

#### Request

- **Headers**:
  - `Content-Type: multipart/form-data`

- **Body**:
  - `file`: The PDF file to be uploaded.
  - `document_type`: The type of the document. Allowed values are `SoF`, `Tariffs`, `Invoices`, `Statement of Account`.

#### Example

```bash
curl -X POST http://localhost:5000/extract \
  -F "file=@path_to_your_file.pdf" \
  -F "document_type=Invoices"
```

#### Response

- **Success** (200):
  ```json
  {
    "output": {
      "invoice_number": "12345",
      "date": "2024-05-28",
      "total": "$1000.00"
    }
  }
  ```

- **Errors**:
  - **400 Bad Request**: Missing file or document type, invalid file type, file size exceeds the limit, invalid document type.
  - **500 Internal Server Error**: Any other errors during processing.

## Working

1. **Upload and Validate**: The API receives a PDF file and validates its type and size.
2. **Secure Filename**: The filename is sanitized using `secure_filename` to prevent security issues.
3. **Save Temporarily**: The PDF file is saved temporarily for processing.
4. **Convert to Images**: Each page of the PDF is converted into an image using `pdf2image`.
5. **Prepare Data**: Each image is converted to base64-encoded strings for sending to the OpenAI API.
6. **Query OpenAI**: The API sends a request to the OpenAI GPT-4 model with the images and a specific prompt based on the document type.
7. **Extract and Respond**: The structured information is extracted from the response and returned as JSON.
8. **Clean Up**: The temporary PDF file is deleted after processing.

## Error Handling

- The API provides detailed error messages for invalid input or processing issues.
- Logs errors with stack traces for easier debugging.

## Security Considerations

- Uses `secure_filename` to prevent directory traversal attacks.
- Limits file size to prevent denial-of-service attacks from large files.
- Cleans up temporary files to avoid clutter and potential security risks.

## Future Improvements

- Enhance document type handling to support more formats.
- Improve error messages for better user experience.
- Add authentication and authorization for secure access.

## Contributing

Feel free to open issues or submit pull requests for improvements and bug fixes. Make sure to follow the contribution guidelines and code of conduct.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
