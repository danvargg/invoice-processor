# invoice-processor

```bash
invoice_api/
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py
│   │   ├── openai_extractor.py
│   │   └── tax_calculator.py
│   └── models
│       ├── __init__.py
│       └── invoice.py
├── requirements.txt
├── Dockerfile
└── .env
```