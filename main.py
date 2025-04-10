from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace this with your verify token (any string you make up)
VERIFY_TOKEN = "crossfit"

# Your Page Access Token (paste your actual Page token here)
PAGE_ACCESS_TOKEN = "EAAOM5Y4Ob84BOZBZC2DUcxDbO7kvZAWzd9EXLZAuFe319Abr7QKKQdxpboRGIT4UCbO7Gck5FVZBE7KgyPVXz0tt4C51nVOxjMgL39tDWSoB2VFDar93KHinDxPzKr33tdZAhrx4VK3FnIOsJVUlyjtB41pmBhkCqzXjdbEmJ7PUqHbAqIfZAfhZC5UgTwZCXjZAyBdxJH0P0XcTIZBLZBCP0gZDZD"

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
