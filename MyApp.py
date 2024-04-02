from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import nltk
import random 

load_dotenv()

# Instantiate the OpenAI object
client = OpenAI()
app = Flask(__name__, template_folder="templates")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nltk.download('punkt')
with open('intents.json') as f:  # Ensure file closure
    intents = json.load(f)

# Download required NLTK resources
nltk.download('punkt')

@app.route('/')
def home():
    return render_template('try.html')


@app.route('/messager', methods=['POST'])
def messager():
    user_msg = request.get_json()['message']

    # Intent Matching
    matched_intent = None
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_msg.lower():  # Case-insensitive matching
                matched_intent = intent
                break
        if matched_intent:
            break

    # Response Generation
    if matched_intent:
        bot_response = random.choice(matched_intent['responses'])
    else:  # Fallback to OpenAI if no intent matches
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Agriculture assistant."},
                    {"role": "user", "content": user_msg}
                ]
            )
            bot_response = completion.choices[0].message.content.strip()

        except OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            bot_response = "I'm currently having some trouble. Please try again later."

    return bot_response
