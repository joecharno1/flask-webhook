from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your verify token (any string you make up)
VERIFY_TOKEN = "crossfit"

# Your Page Access Token (paste your actual Page token here)
PAGE_ACCESS_TOKEN = "EAAOM5Y4Ob84BO7kAxXDFYFHyz872pVj7Ikd2ZCZBNS16kejcPnw8PgqY1Wd5u2hAAXmXsSstLiKOvZCZBHpk9YZAJqyPmiWIOzcU3twQI5t3Hf6adLHZCMIKH34mZBI34HKK7ynMRwl8dz9gFInaSK4AYJ5FsF5wCGfAAYqe0N1ZBEgDa22OUSHEJHyBGbaOLhEGs9x3MHgZC8EZAi2s1xoIcsWBU1"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook sends a challenge when you first set up the webhook
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification token mismatch", 403

    if request.method == 'POST':
        data = request.json
        print("🔔 New Webhook Event:", data)

        # Extract leadgen ID and page ID
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                leadgen_id = change["value"].get("leadgen_id")
                page_id = change["value"].get("page_id")

                # Get lead details from Facebook
                lead_data = get_lead_data(leadgen_id)
                print("📥 Full Lead Data:", lead_data)

                # TODO: Send this data to Zen Planner via API or form redirect

        return "Received", 200

def get_lead_data(lead_id):
    url = f"https://graph.facebook.com/v22.0/{lead_id}"
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
