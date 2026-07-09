import os
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

    def get_text(self, file):

        if file.lower().endswith(".docx"):

            text = DocumentReader.read_docx(file)

        else:

            text = self.ocr.read_image(file)

        return TextPreprocessor.clean(text)
    def predict_document(self, file_path):

        text = self.get_text(file_path)

        prediction = self.extractor.extract(text)

        return prediction

    def predict(self):

        rows = []

        files = sorted(os.listdir(TEST_FOLDER))

        for file in files:

            path = os.path.join(TEST_FOLDER, file)

            print(f"Processing {file}")

            text = self.get_text(path)

            metadata = self.extractor.extract(text)

            metadata["File Name"] = os.path.splitext(file)[0]

            rows.append(metadata)

        df = pd.DataFrame(rows)

        columns = [
            "File Name",
            "Aggrement Value",
            "Aggrement Start Date",
            "Aggrement End Date",
            "Renewal Notice (Days)",
            "Party One",
            "Party Two"
        ]

        df = df[columns]

        OUTPUT_DIR.mkdir(exist_ok=True)

        df.to_csv(
            OUTPUT_DIR / "predictions.csv",
            index=False
        )

        print("Prediction Finished")