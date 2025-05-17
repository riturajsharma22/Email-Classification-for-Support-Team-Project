import requests

url = "https://rituraj18-email2.hf.space/classify"
email_text = (
    "My name is Rituraj, and I would like to request a change in the account type associated with the email address ritu@akaike.com"
)
payload = {"input_email_body": email_text}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
# Print the exact JSON your API sent, with keys in the order Flask emitted them
print("Raw JSON response:")
print(response.text)
