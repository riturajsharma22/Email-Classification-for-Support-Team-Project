import os
import re
import json
import joblib

from flask import Flask, request, Response
from transformers import (
    TFDistilBertForSequenceClassification,
    DistilBertTokenizerFast,
    pipeline
)
import tensorflow as tf

# Create Flask app
app = Flask(__name__)

# Load the trained model and tokenizer
model = TFDistilBertForSequenceClassification.from_pretrained(
    "distilbert_email_classifier"
)
tokenizer = DistilBertTokenizerFast.from_pretrained(
    "distilbert_email_classifier"
)

# Load the label encoder to convert model output to category name
le = joblib.load("label_encoder.joblib")

# Define regular expressions to catch common PII patterns
REGEX_PATTERNS = {
    "phone_number": r"(\+\d{1,3}[-\s]?)?(\d{1,4}[-\s]?){2,4}\d{1,4}",
    "email":         r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "aadhar_num":    r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no":        r"\b\d{3}\b",
    "expiry_no":     r"\b(0[1-9]|1[0-2])\/(\d{2,4})\b",
    "dob":           r"\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b"
}


# Load a lightweight NER model from Hugging Face
ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

# Mapping NER tags to the required format
NER_TAG_MAP = {
    "PER": "full_name",
    "EMAIL": "email",
    "DATE": "dob"
}


def mask_pii(text):
    """
    Mask personal info using NER first, then regex fallback.
    Returns masked_text and a list of entity dicts.
    """
    masked_text = text
    entities = []
    offset = 0  # Track shift in indices after each mask

    # 1) NER-based masking
    ner_result = ner_pipeline(text)
    for ent in ner_result:
        tag = ent["entity_group"]
        if tag in NER_TAG_MAP:
            label = NER_TAG_MAP[tag]
            start = ent["start"] + offset
            end = ent["end"] + offset
            original = masked_text[start:end]
            if not re.match(r"\[.*?\]", original):
                placeholder = f"[{label}]"
                entities.append({
                    "position": [int(start), int(end)],
                    "classification": label,
                    "entity": original
                })
                masked_text = masked_text[:start] + placeholder + masked_text[end:]
                offset += len(placeholder) - (end - start)

    # 2) Regex fallback masking
    for label, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, masked_text):
            start = match.start()
            raw_end = match.end()
            original = match.group().rstrip('.')   # strip trailing dots
            end = start + len(original)
            placeholder = f"[{label}]"
            if not re.match(r"\[.*?\]", original):
                entities.append({
                    "position": [int(start), int(end)],
                    "classification": label,
                    "entity": original
                })
                masked_text = (
                    masked_text[:start]
                    + placeholder
                    + masked_text[raw_end:]
                )

    return masked_text, entities


def predict_category(text):
    """
    Predict email category from masked text.
    """
    inputs = tokenizer(
        text,
        return_tensors="tf",
        truncation=True,
        padding=True,
        max_length=128
    )
    logits = model(inputs)[0]
    pred_id = tf.argmax(logits, axis=1).numpy()[0]
    return str(le.inverse_transform([int(pred_id)])[0])


@app.route("/classify", methods=["POST"])
def classify_email():
    """
    POST /classify
    Input JSON: { "input_email_body": "<email text>" }
    Output JSON (keys in this exact order):
      {
        "input_email_body": "...",
        "list_of_masked_entities": [...],
        "masked_email": "...",
        "category_of_the_email": "..."
      }
    """
    data = request.get_json()
    if not data or "input_email_body" not in data:
        error_payload = json.dumps({"error": "Missing 'input_email_body'"})
        return Response(error_payload, status=400, mimetype="application/json")

    input_email = data["input_email_body"]
    masked_email, entities = mask_pii(input_email)
    category = predict_category(masked_email)

    # Build response dict in the exact desired order
    response_data = {
        "input_email_body": input_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
    payload = json.dumps(response_data)
    return Response(payload, mimetype="application/json")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
