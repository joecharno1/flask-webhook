from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "crossfit"
PAGE_ACCESS_TOKEN = "EAAOM5Y4Ob84BOZBecngBuHaRToLWPqxS0iIapwEZCJCgW5A9pYbAvFN0ZAJRvPDAZB6LMe9mCp6Ozjq5ysZCIL9D9RUyKrwpZAtRoGHBMn5W1ZBDUYnB0L9Di6Pp6ZBOGU584S2hyyxZCyOVBDDmzioIoUgrhX4ZCln6BOhN3gFaqMklK4xTg2tr0lCYtG8j5ZChZBwhu1qkTDODI028wZAgjE7K9wX5b4wZDZD"
USER_ACCESS_TOKEN = "EAAOM5Y4Ob84BOZBecngBuHaRToLWPqxS0iIapwEZCJCgW5A9pYbAvFN0ZAJRvPDAZB6LMe9mCp6Ozjq5ysZCIL9D9RUyKrwpZAtRoGHBMn5W1ZBDUYnB0L9Di6Pp6ZBOGU584S2hyyxZCyOVBDDmzioIoUgrhX4ZCln6BOhN3gFaqMklK4xTg2tr0lCYtG8j5ZChZBwhu1qkTDODI028wZAgjE7K9wX5b4wZDZD"

ZEN_PLANNER_ENDPOINT = "https://api2.zenplanner.com/elements/api-v2/widgets/leadCapture"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403

    if request.method == 'POST':
        data = request.json
        print("🔔 New Webhook Event:", data)

        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                leadgen_id = change["value"].get("leadgen_id")
                page_id = change["value"].get("page_id")

                lead_data = get_lead_data(leadgen_id)
                print("📅 Full Lead Data:", lead_data)

                send_to_zenplanner(lead_data)

        return "Received", 200

def get_lead_data(lead_id):
    url = f"https://graph.facebook.com/v22.0/{lead_id}"
    params = {
        "access_token": USER_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()

def send_to_zenplanner(lead_data):
    try:
        fields = lead_data.get("field_data", [])
        payload = {
            "firstName": get_field(fields, "full_name").split(" ")[0],
            "lastName": get_field(fields, "full_name").split(" ")[-1],
            "email": get_field(fields, "email"),
            "phone": get_field(fields, "phone_number")
        }
        print("📤 Sending to Zen Planner:", payload)
        response = requests.post(ZEN_PLANNER_ENDPOINT, json=payload)
        print("✅ Zen Planner Response:", response.text)
    except Exception as e:
        print("❌ Error sending to Zen Planner:", str(e))

def get_field(fields, name):
    for field in fields:
        if field.get("name") == name:
            return field.get("values", [""])[0]
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
