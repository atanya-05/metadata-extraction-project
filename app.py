import os

from flask import Flask, request, jsonify

from src.predictor import MetadataPredictor

app = Flask(__name__)

predictor = MetadataPredictor()


@app.route("/")
def home():

    prediction = predictor.predict_document(
        "data/test/156155545-Rental-Agreement-Kns-Home.pdf (3).docx"
    )

    return prediction


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]

    os.makedirs("temp", exist_ok=True)

    temp_path = os.path.join(
        "temp",
        uploaded_file.filename
    )

    uploaded_file.save(temp_path)

    try:

        prediction = predictor.predict_document(temp_path)

        return jsonify(prediction)

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )