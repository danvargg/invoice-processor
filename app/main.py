import csv
import io
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse

from app.services.process_invoice import process_invoice_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# TODO: more logging?

app = FastAPI()


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/invoices/")
async def process_invoices(files: List[UploadFile] = File(...)):
    """
    Accept multiple PDF files and process them.
    Returns a JSON response with the parsed data for each file.
    """
    results = [process_invoice_file(file) for file in files]
    return JSONResponse(content={"invoices": results})


@app.post("/invoices/csv/")
async def process_invoices_csv(files: List[UploadFile] = File(...)):
    """
    Same as /invoices/, but returns a CSV file as a streaming response.
    """
    results = [process_invoice_file(file) for file in files]

    if results:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        output.seek(0)

        return StreamingResponse(
            content=iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=invoice_report.csv"}
        )
    else:
        return JSONResponse(content={"detail": "No data processed"}, status_code=400)
