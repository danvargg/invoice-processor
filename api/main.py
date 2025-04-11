import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse

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
    return JSONResponse(content={"invoices": results})  # TODO: send with json

# uvicorn api.main:app --reload
