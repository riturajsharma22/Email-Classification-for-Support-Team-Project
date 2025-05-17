Absolutely! Here's the **entire `README.md`** in one clean, formatted shot — ready to copy or upload to your GitHub repo.

---

````markdown
# 📧 Email Classification API

This is a Python Flask API that:

- ✅ Finds and hides personal details (like names, emails, phone numbers) in support emails.
- ✅ Then classifies the email into one of four types:
  - `Incident`
  - `Request`
  - `Change`
  - `Problem`

The API is live and ready to use on **Hugging Face Spaces**. You can send an email to the API and it will return:
- The original email
- A masked version of the email
- A list of what was masked (with position, type, and value)
- The predicted category

---

## 📍 Live API Endpoint

- **URL**: `https://rituraj18-email2.hf.space/classify`  
- **Method**: `POST`  
- **Input format**:

```json
{
  "input_email_body": "Your email text here"
}
````

---

## ✅ Output Format

```json
{
  "input_email_body": "...",
  "list_of_masked_entities": [
    {
      "position": [start_index, end_index],
      "classification": "entity_type",
      "entity": "original_value"
    }
  ],
  "masked_email": "...",
  "category_of_the_email": "..."
}
```

---

## 🧪 How to Use the API (Example)

You can test the API using the Python script below:

```python
import requests

url = "https://rituraj18-email2.hf.space/classify"
email_text = (
    "My name is Rituraj, and I would like to request a change in the account type associated with the email address ritu@akaike.com"
)
payload = {"input_email_body": email_text}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Raw JSON response:")
print(response.text)
```

💡 This will return a JSON response with:

* Your **original email**
* A **masked version** like: `"My name is [full_name]..."`
* A **list of all detected personal information**
* The predicted **email category** (e.g., `"Request"`)

---

## ⚙️ How the API Works

1. **PII Masking**

   * Uses a pre-trained NER model (`dslim/bert-base-NER`) to detect names, emails, and dates.
   * Uses regex for detecting phone numbers, Aadhar numbers, CVVs, expiry dates, etc.

2. **Email Classification**

   * Uses a fine-tuned `TFDistilBertForSequenceClassification` model.
   * The model was trained using emails where all PII was already masked.
   * Achieved **97.73% accuracy** on the validation set.

---

## 🛠️ Run the Project Locally

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/email-classification-api.git
cd email-classification-api
```

### 2. Install Required Packages

Make sure you have Python 3.10+. Then run:

```bash
pip install -r requirements.txt
```

### 3. Make Sure the Model Files Are Present

Ensure the following are in your project folder:

* `label_encoder.joblib`
* `distilbert_email_classifier/` (with model weights and config files)

### 4. Run the Flask API

```bash
python app.py
```

The API will start at `http://localhost:7860/classify`.

---

## 📁 Project Structure

```
.
├── app.py                     # Main Flask application
├── request.py                 # Script to test the API
├── requirements.txt           # List of required Python libraries
├── label_encoder.joblib       # Label encoder used in classification
├── distilbert_email_classifier/  # Fine-tuned DistilBERT model files
└── README.md                  # This file
```

---

## 📌 Project Summary

| Requirement                           | Status |
| ------------------------------------- | ------ |
| API deployed on Hugging Face Spaces   | ✅      |
| Correct `/classify` POST endpoint     | ✅      |
| No frontend used (pure API)           | ✅      |
| PII masked using NER + regex          | ✅      |
| DistilBERT classification model used  | ✅      |
| JSON output matches assignment format | ✅      |
| GitHub code in root directory         | ✅      |
| Report and README included            | ✅      |

