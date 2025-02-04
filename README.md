# Invoice processor

## Local test

```bash
docker build -t invoice-app .
docker run -p 8000:80 --env-file .env invoice-app
curl.exe -X POST -H "x-api-key: YOUR_API_KEY" -F "files=@invoice_0.pdf" http://localhost:8000/invoices/
```