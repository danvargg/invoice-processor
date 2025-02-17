import logging
from typing import Any, Dict

from fastapi import UploadFile

from api.services.openai_extractor import extract_invoice_data
from api.services.pdf_extractor import extract_text_from_pdf
from api.services.tax_calculator import compute_taxes


def process_invoice_file(file: UploadFile) -> Dict[str, Any]:
    try:
        text = extract_text_from_pdf(file)
        # sanitized_text = sanitize_text(text)  # TODO: implement
        extracted_data = extract_invoice_data(text)
        print(extracted_data)

        total = float(extracted_data.get("total", 0.0))
        gst = extracted_data.get("federal_tax")
        qst = extracted_data.get("provincial_tax")

        if gst is None or qst is None:
            subtotal, computed_gst, computed_qst = compute_taxes(total)
            gst = computed_gst if gst is None else float(gst)
            qst = computed_qst if qst is None else float(qst)
        else:
            subtotal = total - float(gst) - float(qst)

        return {
            "file_name": file.filename,
            "date": extracted_data.get("date", "N/A"),
            "supplier": extracted_data.get("supplier", "N/A"),
            "category": extracted_data.get("category", "N/A"),
            "description": extracted_data.get("description", "N/A"),
            "amount_subtotal": round(subtotal, 2),
            "federal_tax_gst": round(float(gst), 2),
            "provincial_tax_qst": round(float(qst), 2),
            "total": round(total, 2),
        }
    except Exception as e:
        logging.error(f"Error processing {file.filename}: {str(e)}")
        return {
            "file_name": file.filename,
            "error": str(e)
        }
