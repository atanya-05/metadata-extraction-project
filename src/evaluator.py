import pandas as pd
from pathlib import Path

from src.utils import TEST_CSV, OUTPUT_DIR


class MetadataEvaluator:

    def __init__(self):
        self.actual = pd.read_csv(TEST_CSV)
        self.predicted = pd.read_csv(OUTPUT_DIR / "predictions.csv")

    def normalize(self, value):
        if pd.isna(value):
            return ""

        return (
            str(value)
            .strip()
            .lower()
            .replace(",", "")
            .replace("rs.", "")
            .replace("rs", "")
        )

    def evaluate(self):

        self.actual = self.actual.set_index("File Name")
        self.predicted = self.predicted.set_index("File Name")

        fields = [
            "Aggrement Value",
            "Aggrement Start Date",
            "Aggrement End Date",
            "Renewal Notice (Days)",
            "Party One",
            "Party Two"
        ]

        results = []

        print("\n==============================")
        print("Evaluation Report")
        print("==============================")

        for field in fields:

            correct = 0
            total = 0

            for file_name in self.actual.index:

                if file_name not in self.predicted.index:
                    continue

                actual = self.normalize(self.actual.loc[file_name, field])
                predicted = self.normalize(self.predicted.loc[file_name, field])

                total += 1

                if actual == predicted:
                    correct += 1

            recall = round(correct / total, 2) if total else 0

            print(f"{field:<30} {recall}")

            results.append({
                "Field": field,
                "Correct": correct,
                "Total": total,
                "Recall": recall
            })

        df = pd.DataFrame(results)

        df.to_csv(
            OUTPUT_DIR / "evaluation.csv",
            index=False
        )

        print("\nEvaluation Saved Successfully")