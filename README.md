# Invoice Processor Assistant

![Python](https://img.shields.io/badge/-Python-000000?style=flat&logo=Python)
![FastAPI](https://img.shields.io/badge/-FastAPI-000000?style=flat&logo=FastAPI)
![OpenAI](https://img.shields.io/badge/-OpenAI-000000?style=flat&logo=OpenAI)
![Pandas](https://img.shields.io/badge/-Pandas-000000?style=flat&logo=Pandas)

> This a generalized and simplified version of the project.

An invoice processing system designed to upload, process, and extract structured data from PDF invoices.

<img width=30% height=30%  src="https://github.com/danvargg/invoice-processor/blob/main/img/ui.png">

## Business Problem

The goal was to develop a system that allows users to upload multiple invoices, process them, and extract structured data.

## Implementation

- **API**: A `FastAPI` backend was developed to handle invoice processing requests.
- **Authentication**: API key-based authentication to secure the endpoints.
- **Invoice Processing**: The backend processes extract structured data using `LLMs`, utilizing `function calling` and `structured output`.

## Business Results

The invoice processor provides businesses with an efficient and automated way to handle invoice data extraction. It reduces manual effort, improves accuracy, and allows users to process multiple invoices simultaneously.