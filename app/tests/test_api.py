import os

import requests
from dotenv import load_dotenv

load_dotenv()

# TODO: can a csv be sent from a server?

# Define the API endpoints
json_endpoint = "http://localhost:8000/invoices/"
# csv_endpoint = "http://localhost:8000/invoices/csv/"

# Define the directory containing the invoice files
invoices_dir = "./app/tests/invoices"

# Check if the directory exists
if not os.path.exists(invoices_dir):
    raise FileNotFoundError(f"The directory {invoices_dir} does not exist")

# Get all PDF files in the invoices directory
files = [
    ("files", (file_name, open(os.path.join(invoices_dir, file_name), "rb"), "application/pdf"))
    for file_name in os.listdir(invoices_dir) if file_name.endswith(".pdf")
]

# Define the headers with the API key
headers = {
    "X-API-Key": os.getenv("MY_API_KEY")
}

# print(headers)

# Send request to the JSON endpoint
response_json = requests.post(json_endpoint, files=files, headers=headers)
if response_json.status_code == 200:
    print("JSON Response:")
    print(response_json.json())
else:
    print(f"Failed to get JSON response: {response_json.status_code}")
#
# # Send request to the CSV endpoint
# response_csv = requests.post(csv_endpoint, files=files, headers=headers)
# if response_csv.status_code == 200:
#     with open("invoice_report.csv", "w") as f:
#         f.write(response_csv.text)
#     print("CSV response saved to invoice_report.csv")
# else:
#     print(f"Failed to get CSV response: {response_csv.status_code}")
