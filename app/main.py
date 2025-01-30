import csv
import io
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse, StreamingResponse

from app.config import verify_api_key
from app.services.process_invoice import process_invoice_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# TODO: more logging?
# TODO: add more columns: category and description

app = FastAPI(
    title="Canadian Invoice Processor (Quebec)",
    description="Upload PDF invoices, extract structured data using OpenAI, compute GST/QST, and return results."
)


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# TODO: check auto_error=False

@app.post("/invoices/", dependencies=[Depends(verify_api_key)], tags=["Invoices"])
async def process_invoices(files: List[UploadFile] = File(...)):
    """
    Accept multiple PDF files and process them.
    Returns a JSON response with the parsed data for each file.
    """
    results = [process_invoice_file(file) for file in files]

    # TODO: maybe remove?:
    csv_filename = "invoice_report.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        fieldnames = results[0].keys() if results else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    return JSONResponse(content={"invoices": results})


# @app.post("/invoices/csv/", dependencies=[Depends(verify_api_key)], tags=["Invoices"])
# async def process_invoices_csv(files: List[UploadFile] = File(...)):
#     """
#     Same as /invoices/, but returns a CSV file as a streaming response.
#     """
#     results = [process_invoice_file(file) for file in files]
#
#     logging.info("CSV Results: %s", results)
#
#     # print(results)
#
#     if results:
#         output = io.StringIO()
#         writer = csv.DictWriter(output, fieldnames=results[0].keys())
#         writer.writeheader()
#         writer.writerows(results)
#         output.seek(0)
#
#         return StreamingResponse(
#             content=iter([output.getvalue()]),
#             media_type="text/csv",
#             headers={"Content-Disposition": "attachment; filename=invoice_report.csv"}
#         )
#     else:
#         return JSONResponse(content={"detail": "No data processed"}, status_code=400)

# TODO:
# curl -X POST "http://localhost:8000/process_invoices" \
#      -H "X-API-Key: supersecretapikey" \
#      -F "files=@/path/to/invoice1.pdf" \
#      -F "files=@/path/to/invoice2.pdf"
