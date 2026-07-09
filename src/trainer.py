import os
import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from src.document_reader import DocumentReader
from src.ocr_reader import OCRReader
from src.preprocessing import TextPreprocessor
from src.embeddings import EmbeddingModel
from src.utils import TRAIN_FOLDER, TRAIN_CSV, MODEL_DIR


class MetadataTrainer:

    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.ocr = OCRReader()

    def find_matching_file(self, filename):

        filename = filename.strip().lower()

        for file in os.listdir(TRAIN_FOLDER):

            full_path = os.path.join(TRAIN_FOLDER, file)

            if not os.path.isfile(full_path):
                continue

            file_without_extension = os.path.splitext(file)[0].strip().lower()

            # Exact Match
            if file_without_extension == filename:
                return full_path

            # Windows duplicate names like "(8)"
            if file_without_extension.startswith(filename + " ("):
                return full_path

        return None

    def load_training_data(self):

        df = pd.read_csv(TRAIN_CSV)

        documents = []
        metadata = []
        filenames = []

        print(f"\nFound {len(df)} records in train.csv\n")

        for index, row in df.iterrows():

            filename = str(row["File Name"])

            file_path = self.find_matching_file(filename)

            if file_path is None:

                print("=" * 70)
                print(f"WARNING : {filename} was listed in train.csv")
                print("but the file is not present inside data/train.")
                print("Skipping this file and continuing training...")
                print("=" * 70)

                continue

            print(f"✅ Reading : {os.path.basename(file_path)}")

            try:

                if file_path.lower().endswith(".docx"):

                    text = DocumentReader.read_docx(file_path)

                elif file_path.lower().endswith(".png"):

                    text = self.ocr.read_image(file_path)

                else:

                    print(f"Unsupported file : {file_path}")

                    continue

                text = TextPreprocessor.clean(text)

                documents.append(text)

                metadata.append(row.to_dict())
                filenames.append(os.path.basename(file_path))

            except Exception as e:

                print(f"Error while reading {filename}")
                print(e)

        return documents, metadata, filenames

    def train(self):

        print("\n==============================")
        print("Loading Training Data...")
        print("==============================")

        documents, metadata, filenames = self.load_training_data()

        if len(documents) == 0:

            raise Exception("No training documents found.")

        print("\nGenerating Embeddings...")

        embeddings = self.embedding_model.encode(documents)

        print("Embeddings Shape :", embeddings.shape)

        print("\nTraining Similarity Model...")

        model = NearestNeighbors(
            n_neighbors=1,
            metric="cosine"
        )

        model.fit(embeddings)

        joblib.dump(model, MODEL_DIR / "similarity_model.pkl")
        joblib.dump(metadata, MODEL_DIR / "metadata.pkl")
        joblib.dump(filenames, MODEL_DIR / "filenames.pkl")
        joblib.dump(embeddings, MODEL_DIR / "embeddings.pkl")

        print("\n====================================")
        print("Training Completed Successfully")
        print("====================================")
        print(f"Documents Used : {len(documents)}")
        print("Model Saved Successfully")