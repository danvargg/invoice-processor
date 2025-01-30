import json
import os
from typing import Dict

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # TODO: move somewhere else

def extract_invoice_data(text: str) -> Dict:
    """
    Send invoice text to OpenAI Chat Completion API to get structured data.
    Expected output keys: date, supplier, total, federal_tax, provincial_tax
    """
    try:
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
                    "content": f"Extract data from this invoice:\n{text[:10000]}..."
                }
            ],
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise ValueError(f"OpenAI extraction failed: {str(e)}")
