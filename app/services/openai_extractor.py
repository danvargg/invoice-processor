import json
from typing import Dict

import openai


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
                    "content": f"Extract data from this invoice:\n{text}..."
                }
            ],
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        raise ValueError(f"OpenAI extraction failed: {str(e)}")
