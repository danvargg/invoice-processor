import csv
import io
import logging
from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse

from app.services.openai_extractor import extract_invoice_data
from app.services.pdf_extractor import extract_text_from_pdf
from app.services.tax_calculator import compute_taxes

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

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
    results = []

    for file in files:
        try:
            text = extract_text_from_pdf(file)  # FIXME: duplicate

            extracted_data = extract_invoice_data(text)

            total = float(extracted_data.get("total", 0.0))
            gst = extracted_data.get("federal_tax")
            qst = extracted_data.get("provincial_tax")

            if gst is None or qst is None:
                subtotal, computed_gst, computed_qst = compute_taxes(total)
                gst = computed_gst if gst is None else float(gst)
                qst = computed_qst if qst is None else float(qst)
            else:
                subtotal = total - float(gst) - float(qst)

            results.append({
                "file_name": file.filename,
                "date": extracted_data.get("date", "N/A"),
                "supplier": extracted_data.get("supplier", "N/A"),
                "amount_subtotal": round(subtotal, 2),
                "federal_tax_gst": round(float(gst), 2),
                "provincial_tax_qst": round(float(qst), 2),
                "total": round(total, 2),
            })
        except Exception as e:
            logging.error(f"Error processing {file.filename}: {str(e)}")
            results.append({
                "file_name": file.filename,
                "error": str(e)
            })

    return JSONResponse(content={"invoices": results})


@app.post("/invoices/csv/")
async def process_invoices_csv(files: List[UploadFile] = File(...)):
    """
    Same as /invoices/, but returns a CSV file as a streaming response.
    """
    # Process the same way
    results = []
    for file in files:
        try:
            text = extract_text_from_pdf(file)
            extracted_data = extract_invoice_data(text)

            total = float(extracted_data.get("total", 0.0))
            gst = extracted_data.get("federal_tax")
            qst = extracted_data.get("provincial_tax")

            if gst is None or qst is None:
                subtotal, computed_gst, computed_qst = compute_taxes(total)
                gst = computed_gst if gst is None else float(gst)
                qst = computed_qst if qst is None else float(qst)
            else:
                subtotal = total - float(gst) - float(qst)

            results.append({
                "File": file.filename,
                "Date": extracted_data.get("date", "N/A"),
                "Supplier": extracted_data.get("supplier", "N/A"),
                "Amount (CAD)": round(subtotal, 2),
                "Federal Tax (GST)": round(float(gst), 2),
                "Provincial Tax (QST)": round(float(qst), 2),
                "Total (CAD)": round(total, 2)
            })
        except Exception as e:
            logging.error(f"Error processing {file.filename}: {str(e)}")
            results.append({
                "File": file.filename,
                "Error": str(e)
            })

    # Convert results to CSV in-memory
    if results:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        output.seek(0)

        # Return as streaming response
        return StreamingResponse(
            content=iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=invoice_report.csv"}
        )
    else:
        return JSONResponse(content={"detail": "No data processed"}, status_code=400)
