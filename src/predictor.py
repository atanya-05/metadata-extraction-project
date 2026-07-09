import os
import re

import pandas as pd

from src.document_reader import DocumentReader
from src.ocr_reader import OCRReader
from src.preprocessing import TextPreprocessor
from src.gemini_extractor import GeminiExtractor
from src.utils import TEST_FOLDER, OUTPUT_DIR


class MetadataPredictor:

    def __init__(self):
        self.ocr = OCRReader()
        self.extractor = GeminiExtractor()

    def get_text(self, file_path):
        """
        Extract text from DOCX or image documents.
        """

        if file_path.lower().endswith(".docx"):
            text = DocumentReader.read_docx(file_path)
        else:
            text = self.ocr.read_image(file_path)

        return TextPreprocessor.clean(text)

    def clean_filename(self, filename):
        """
        Convert filenames into the same format used in test.csv.

        Examples:
        --------------------------------------------
        24158401-Rental-Agreement (10).png
        -> 24158401-Rental-Agreement

        156155545-Rental-Agreement-Kns-Home.pdf (3).docx
        -> 156155545-Rental-Agreement-Kns-Home
        """

        name = os.path.splitext(filename)[0]

        # Remove embedded ".pdf"
        name = name.replace(".pdf", "")

        # Remove duplicate suffixes like (3), (8), (10)
        name = re.sub(r"\s*\(\d+\)$", "", name)

        return name.strip()

    def predict_document(self, file_path):
        """
        Predict metadata for a single document.
        """

        text = self.get_text(file_path)

        prediction = self.extractor.extract(text)

        return prediction

    def predict(self):
        """
        Predict metadata for every file inside data/test.
        """

        predictions = []

        files = sorted(os.listdir(TEST_FOLDER))

        for file in files:

            path = os.path.join(TEST_FOLDER, file)

            print(f"Processing {file}")

            metadata = self.predict_document(path)

            metadata["File Name"] = self.clean_filename(file)

            predictions.append(metadata)

        df = pd.DataFrame(predictions)

        columns = [
            "File Name",
            "Aggrement Value",
            "Aggrement Start Date",
            "Aggrement End Date",
            "Renewal Notice (Days)",
            "Party One",
            "Party Two",
        ]

        df = df[columns]

        OUTPUT_DIR.mkdir(exist_ok=True)

        output_path = OUTPUT_DIR / "predictions.csv"

        df.to_csv(output_path, index=False)

        print("\n======================================")
        print("Prediction Completed Successfully")
        print("======================================")
        print(f"Saved to : {output_path}")