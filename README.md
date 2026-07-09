# AI Metadata Extraction System

## Overview

This project extracts metadata from Rental Agreement documents using Google's Gemini AI.

The application supports both:

- DOCX documents
- PNG scanned agreements

The extracted metadata includes:

- Aggrement Value
- Aggrement Start Date
- Aggrement End Date
- Renewal Notice (Days)
- Party One
- Party Two

---

## Technologies Used

- Python
- Google Gemini 2.5 Flash
- EasyOCR
- python-docx
- Flask
- Pandas

---

## Project Structure

metadata_extraction_project/

├── app.py

├── predict.py

├── evaluate.py

├── requirements.txt

├── README.md

├── src/

├── data/

├── outputs/

└── .env

---

## Installation

Create Virtual Environment

python -m venv venv

Activate

Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

---

## Run Prediction

python predict.py

Predictions will be saved to

outputs/predictions.csv

---

## Evaluation

python evaluate.py

Evaluation results will be saved to

outputs/evaluation.csv

---

## Run API

python app.py

Server

http://127.0.0.1:5000

---

## API Endpoint

POST /predict

Input

DOCX or PNG

Output

JSON Metadata

---

## AI Approach

The solution uses Google's Gemini Large Language Model for semantic metadata extraction instead of rule-based techniques such as Regular Expressions.

The system first extracts document text using python-docx or EasyOCR and then uses Gemini to identify metadata fields.

This approach makes the solution template-independent and scalable.

---

## Author

A Tanya