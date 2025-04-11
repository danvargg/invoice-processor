# Invoice Processor API

This is a Python-based API for processing invoices. The API is built using FastAPI and can be run in a Docker container. It supports uploading invoice files and requires API keys for authentication.

## How It Works

The Invoice Processor API allows users to upload invoice files (in PDF format) and processes them to extract relevant information. The API uses two types of API keys for authentication: an OpenAI API key and a custom API key.

The API uses an LLM to process and extract information from the uploaded invoice files. The LLM helps in understanding and extracting relevant data from the text within the invoices.

### API Endpoints

- **POST /invoices/**: This endpoint allows users to upload invoice files. The request must include the custom API key in the headers and the invoice files in the form data.

### Build and run the API

```bash
docker build -t invoice-app .
docker run -p 8000:80 --env-file .env invoice-app
```

### Example Request

```bash
curl.exe -X POST -H "x-api-key: YOUR_API_KEY" -F "files=@invoice1.pdf" -F "files=@invoice2.pdf" http://localhost:8000/invoices/
```

# Invoice Processor

Python FastAPI Streamlit Pandas Requests OpenAI

This is a generalized version of the project. The specific code, architecture, and data are property of the client and cannot be fully shared.

An invoice processing system designed to upload, process, and extract structured data from PDF invoices. The system uses a FastAPI backend and a Streamlit-based UI to provide a seamless user experience.

## Business Problem

The goal was to develop a system that allows users to upload multiple invoices, process them, and extract structured data such as invoice details, taxes (GST/QST), and totals. The system needed to provide a user-friendly interface for uploading files, display progress during processing, and allow users to download the results in CSV format.

## Implementation

### 1. Backend (FastAPI)
- **API Development**: A FastAPI backend was developed to handle invoice processing requests. It includes endpoints for health checks and invoice processing.
- **Authentication**: API key-based authentication was implemented to secure the endpoints.
- **Invoice Processing**: The backend processes uploaded PDF files and extracts structured data using OpenAI-powered models.

### 2. Frontend (Streamlit)
- **File Upload**: Users can upload multiple PDF invoices through a Streamlit-based UI.
- **Progress Bar**: A progress bar is displayed during the processing of invoices.
- **Data Display**: Processed invoice data is displayed in a table format.
- **CSV Download**: Users can download the processed data as a CSV file.

### 3. Environment Configuration
- **Environment Variables**: Sensitive information such as API keys is stored in a `.env` file and loaded using `python-dotenv`.
- **Dependencies**: Separate `requirements.txt` files are maintained for the backend and frontend to manage dependencies.

### 4. Deployment
- **Backend**: The FastAPI backend can be deployed using `uvicorn` or any ASGI-compatible server.
- **Frontend**: The Streamlit UI can be run locally or deployed to a cloud platform for wider accessibility.

## Business Results

The invoice processor provides businesses with an efficient and automated way to handle invoice data extraction. It reduces manual effort, improves accuracy, and allows users to process multiple invoices simultaneously. The system delivers structured data in a user-friendly format, enabling better financial management and reporting.