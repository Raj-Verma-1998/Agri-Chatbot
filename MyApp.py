import requests
from flask import Flask, request, render_template, jsonify
from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import nltk

load_dotenv()

# Instantiate the OpenAI object
client = OpenAI()
app = Flask(__name__, template_folder="templates")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")  # Load Data.gov.in API key from environment
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Load Weather API key from environment

nltk.download('punkt')

# Define the extract_location function
def extract_location(user_msg):
    # Your logic to extract the location from the user message goes here
    pass

@app.route('/')
def home():
    return render_template('try.html')

@app.route('/messager', methods=['POST'])
def messager():
    user_msg = request.get_json()['message']
    bot_response = ""

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Agriculture assistant."},
                {"role": "user", "content": user_msg}
            ]
        )
        bot_response = completion.choices[0].message.content.strip()

        # Logic to fetch commodity prices for all states
        if any(keyword in user_msg.lower() for keyword in ["commodity prices", "agriculture prices"]):
            try:
                # Construct parameters for the Data.gov.in API
                api_params = {
                    "api-key": DATA_GOV_API_KEY,
                    "format": "json"
                }
                response = requests.get("https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json", params=api_params)
                response.raise_for_status()

                commodity_prices = response.json()['records']
                price_info_string = {}

                # Iterate over the records and group commodity prices by state
                for record in commodity_prices:
                    state = record['state']
                    commodity = record['commodity']
                    price = record['modal_price']
                    if state not in price_info_string:
                        price_info_string[state] = []
                    price_info_string[state].append(f"{commodity} - Rs. {price}")

                # Format the commodity prices for each state
                formatted_prices = "\n".join([f"\nCommodity Prices in {state}:\n" + "\n".join(prices) for state, prices in price_info_string.items()])

                bot_response += formatted_prices

            except requests.exceptions.RequestException as e:
                print(f"Commodity API Error: {e}")
                bot_response += "\n\nSorry, commodity prices are currently unavailable. Please try again later."

        # Logic to fetch weather forecast if user asks about weather
        if "weather" in user_msg.lower():
            try:
                # Fetch weather forecast from Weather API
                # Extract location from user message
                location = extract_location(user_msg)

                # Fetch weather forecast from Weather API
                weather_api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={WEATHER_API_KEY}&units=metric"
                weather_response = requests.get(weather_api_url)
                weather_response.raise_for_status()

                weather_data = weather_response.json()
                forecast = weather_data['list']  # 'list' contains forecast data
                weather_info = f"\n\nWeather Forecast for {location}:\n"  # Fix: use f-string to format location
                for day in forecast:
                    date = day['dt_txt']
                    condition = day['weather'][0]['description']
                    max_temp = day['main']['temp_max']
                    min_temp = day['main']['temp_min']
                    weather_info += f"{date}: {condition}, Max Temp: {max_temp}°C, Min Temp: {min_temp}°C\n"

                bot_response += weather_info

            except requests.exceptions.RequestException as e:
                print(f"Weather API Error: {e}")
                bot_response += "\n\nSorry, weather forecast is currently unavailable. Please try again later."

    except OpenAIError as e:
        print(f"OpenAI API Error:")
        bot_response = "I'm currently having some trouble. Please try again later."

    return bot_response

