import csv
import json
import os

import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# TODO: add logging with timestamp
# TODO: add more columns
# TODO: modularize code:


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    # print(f"processing {pdf_file.name}")
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def compute_taxes(total):
    """Compute GST/QST from total (assuming total includes taxes)."""
    rate_gst = 0.05
    rate_qst = 0.09975
    subtotal = total / (1 + rate_gst) / (1 + rate_qst)
    gst = subtotal * rate_gst
    qst = (subtotal + gst) * rate_qst
    return round(subtotal, 2), round(gst, 2), round(qst, 2)


# Streamlit UI
st.title("📑 Canadian Invoice Processor (Quebec)")
uploaded_files = st.file_uploader(
    "Upload PDF Invoices",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files and st.button("Process Invoices"):
    processed_data = []
    progress_bar = st.progress(0)
    total_files = len(uploaded_files)

    for i, file in enumerate(uploaded_files):
        try:
            # Step 1: Extract text from PDF
            text = extract_text_from_pdf(file)

            # Step 2: Use OpenAI to extract structured data
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Extract invoice data as JSON with:
                        - date (YYYY-MM-DD)
                        - supplier (text)
                        - total (float, CAD)
                        - federal_tax (float, GST or null)
                        - provincial_tax (float, QST or null)"""
                    },
                    {
                        "role": "user",
                        "content": f"Extract data from this invoice:\n{text[:3000]}..."  # TODO: fix this
                        # Truncate to avoid token limits
                    }
                ],
            )

            # Parse JSON response
            data = json.loads(response.choices[0].message.content)
            total = float(data.get("total", 0))

            # Step 3: Compute taxes if missing
            gst = data.get("federal_tax")
            qst = data.get("provincial_tax")

            if gst is None or qst is None:
                subtotal, computed_gst, computed_qst = compute_taxes(total)
                gst = computed_gst if gst is None else float(gst)
                qst = computed_qst if qst is None else float(qst)
            else:
                subtotal = total - float(gst) - float(qst)

            # Add to results
            processed_data.append({
                "File": file.name,
                "Date": data.get("date", "N/A"),
                "Supplier": data.get("supplier", "N/A"),
                "Amount (CAD)": round(subtotal, 2),
                "Federal Tax (GST)": round(float(gst), 2),
                "Provincial Tax (QST)": round(float(qst), 2),
                "Total (CAD)": round(total, 2)
            })

        except Exception as e:
            st.error(f"Error processing {file.name}: {str(e)}")

        # Update progress bar
        progress_bar.progress((i + 1) / total_files)

    # Display the table of processed data
    if processed_data:
        st.table(processed_data)

        # Step 4: Export to CSV
        csv_filename = "invoice_report.csv"
        with open(csv_filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=processed_data[0].keys())
            writer.writeheader()
            writer.writerows(processed_data)

        st.success(f"Processed {len(processed_data)} invoices!")
        st.download_button(
            "Download CSV",
            data=open(csv_filename, "rb").read(),
            file_name=csv_filename,
            mime="text/csv"
        )
