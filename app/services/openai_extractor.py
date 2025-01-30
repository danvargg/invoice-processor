import os
import json
import openai
from typing import Dict

# Make sure to set openai.api_key somewhere (e.g., in config.py or here).
# openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_invoice_data(text: str) -> Dict:
    """
    Send invoice text to OpenAI Chat Completion API to get structured data.
    Expected output keys: date, supplier, total, federal_tax, provincial_tax
    """
    try:
        response = openai.ChatCompletion.create(
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
                    "content": f"Extract data from this invoice:\n{text[:3000]}..."
                    # truncated for token limits, as you do in your Streamlit
                }
            ],
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise ValueError(f"OpenAI extraction failed: {str(e)}")