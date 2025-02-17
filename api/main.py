import csv
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
# from mangum import Mangum

from api.config import verify_api_key
from api.services.process_invoice import process_invoice_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(
    title="Canadian Invoice Processor (Quebec)",
    description="Upload PDF invoices, extract structured data using OpenAI, compute GST/QST, and return results."
)


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/invoices/", dependencies=[Depends(verify_api_key)], tags=["Invoices"])
async def process_invoices(files: List[UploadFile] = File(...)):
    """
    Accept multiple PDF files and process them.
    Returns a JSON response with the parsed data for each file.
    """
    results = [process_invoice_file(file) for file in files]
    print(results)

    csv_filename = "invoice_report.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = results[0].keys() if results else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    return JSONResponse(content={"invoices": results})  # TODO: send with json


# handler = Mangum(app)
