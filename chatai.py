import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

# This loads the secret variables from your .env file into memory
load_dotenv()
app = Flask(__name__)

# Initialize your Gemini client
# Replace with your actual API key
# ADD THESE LINES INSTEAD
SECRET_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=SECRET_KEY)


chat_session = client.chats.create(
    model="gemini-3.1-flash-lite", # Or whichever model you are using
    config={
        "system_instruction": "You are a helpful, calming AI assistant named Breathe AI. Always keep your responses concise, engaging, and end with a..."
    }
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you repeat it?"})

    try:
        # Send the message to the continuous session (it remembers history)
        response = chat_session.send_message(user_message)
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"Error connecting to AI: {str(e)}"

    return jsonify({"response": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)

