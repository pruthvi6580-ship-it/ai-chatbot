import os
import time
import threading
from flask import Flask
from google import genai

app = Flask(__name__)

# Initialize Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Web server health check (keeps the cloud server active)
@app.route('/')
def home():
    return "Bot is active and running 24/7!"

# Continuous Chat Loop Running in Background
def run_bot_loop():
    time.sleep(5) # Wait for server startup
    chat = client.chats.create(model="gemini-2.5-flash")
    prompt = "Hello! Tell me an interesting topic to start our endless chat."

    while True:
        try:
            response = chat.send_message(prompt)
            print(f"Bot Reply:\n{response.text}\n" + "="*40)
            
            # Follow-up prompt to keep the loop going
            prompt = "That's interesting! Tell me more or ask a follow-up question."
            time.sleep(15) # Pause 15 seconds between chats

        except Exception as e:
            print(f"Error: {e}. Retrying in 20 seconds...")
            time.sleep(20)

# Start continuous thread
threading.Thread(target=run_bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
