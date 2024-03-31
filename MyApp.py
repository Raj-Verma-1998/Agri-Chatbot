from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import nltk

load_dotenv()

# Instantiate the OpenAI object
client = OpenAI()
app = Flask(__name__, template_folder="templates")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Download required NLTK resources
nltk.download('punkt')

@app.route('/')
def home():
    return render_template('try.html')


@app.route('/messager', methods=['POST'])
def messager():
    user_msg = request.get_json()['message']
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Agriculture assistant."},
                {"role": "user", "content": user_msg}
            ]
        )
        bot_response = completion.choices[0].message.content.strip()
        return bot_response

    except OpenAI.error.APIError as e:
        print(f"OpenAI API Error: {e}")
        return "I'm currently having some trouble. Please try again later."


if __name__ == '__main__':
    app.run(debug=True)