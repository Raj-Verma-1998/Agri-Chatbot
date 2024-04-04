import requests
from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup 
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

nltk.download('punkt')  # tokenizer data
nltk.download('averaged_perceptron_tagger')  # Part-of-speech tagger data
nltk.download('wordnet')  # WordNet data
nltk.download('stopwords')  # Stopwords data
# Define the extract_location function
def extract_location(user_msg):
    # Your logic to extract the location from the user message goes here
    pass

# Function to extract location from the market link
def extract_location(market_link):
    # Your logic to extract the location from the market link goes here
    pass

# Function to fetch and display market prices for all states
def fetch_market_prices(location):
    # Example API URL for fetching market prices based on location
    market_api_url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json"
    response = requests.get(market_api_url)
    response.raise_for_status()
    market_data = response.json()
    # Parse market data and format prices for all states
    market_prices_by_state = {}
    for market_info in market_data:
        state = market_info['state']
        commodity = market_info['commodity']
        price = market_info['price']
        if state not in market_prices_by_state:
            market_prices_by_state[state] = []
        market_prices_by_state[state].append(f"{commodity} - Rs. {price}")
    # Format the market prices for all states
    formatted_prices = "\n".join([f"\nMarket Prices in {state}:\n" + "\n".join(prices) for state, prices in market_prices_by_state.items()])
    return formatted_prices

# Function to fetch and display pest management information
def fetch_pest_management_info():
    # Your logic to fetch and format pest management information goes here
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

        # Logic to prompt the user for a market link and extract the location
        if "market prices" in user_msg.lower():  # Or a more specific trigger for market info
            prompt_user_for_link = "Please provide a link to a specific market."
            # Assume 'market_link' is the link provided by the user
            try:
                location = extract_location(market_link) 
                market_prices = fetch_market_prices(location)
                bot_response += market_prices
            except Exception as e:
                print(f"Location extraction failed: {e}")
                bot_response = "Sorry, couldn't find the location from the provided link."

        # Logic to fetch commodity prices for all states (existing logic)
        if any(keyword in user_msg.lower() for keyword in ["commodity prices", "agriculture prices"]):
            # Your existing logic for fetching commodity prices
            pass

        # Logic to fetch weather forecast if user asks about weather (existing logic)
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

        # Logic to fetch pest management information
        if "pest management" in user_msg.lower():
            pest_management_info = fetch_pest_management_info()
            bot_response += pest_management_info

    except OpenAIError as e:
        print(f"OpenAI API Error:")
        bot_response = "I'm currently having some trouble. Please try again later."

    return bot_response
