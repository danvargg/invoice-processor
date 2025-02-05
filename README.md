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