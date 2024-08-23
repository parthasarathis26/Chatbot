from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("User Message:", user_message)

    try:
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response.raise_for_status()
        rasa_response_json = rasa_response.json()
        print("Rasa Response:", rasa_response_json)
        bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I didn\'t understand that.'
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        bot_response = "Error: Couldn't connect to the chatbot server."

    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=3000)