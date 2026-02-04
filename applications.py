import requests.exceptions
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
import requests
import datetime


load_dotenv()


api_key= os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise  ValueError("API key  not found")

client= genai.Client(api_key=api_key)



# FUNCTION TO GET WEATHER OF A CITY.
def get_weather(city: str):
    """
    featches current weather for a given city using API

    args:
    city(str): city name(eg: Dehradun)


    returns:
    dict: weather details in json format
    """
    try:
        api_key="your_api_key"
        url= f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response =requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return{"error": str(e)}



# GEMINI CODE TO USE THE FUNCTION TO GET DETAILS OF THE CITY
def temperature_of_city(city):
    system_instructions = """
       You are given weather data in JSON format from the OpenWeather API.
       Your job is to convert it into a clear, human-friendly weather update.  
    
       Guidelines:
       1. Always mention the city and country.
       2. Convert temperature from Kelvin to Celsius (°C), rounded to 1 decimal.
       3. Include: current temperature, feels-like temperature, main weather description,
          humidity, wind speed, and sunrise/sunset times (converted from UNIX timestamp).
       4. Use natural, conversational language.
       5. Based on the current conditions, suggest what the person should carry or wear.
          - If rain/clouds: suggest umbrella/raincoat.
          - If very hot (>30°C): suggest light cotton clothes, sunglasses, stay hydrated.
          - If cold (<15°C): suggest warm clothes, jacket.
          - If windy: suggest windbreaker, secure loose items.
          - If humid: suggest breathable clothes, water bottle.
       6. If any field is missing, gracefully ignore it.
    
       """
    response= client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Generate a clear, friendly weather report with temperatures in °C, humidity, wind, sunrise/sunset for the {city} and practical suggestions on what to wear or carry.",
        config=types.GenerateContentConfig(system_instruction=system_instructions,tools=[get_weather])
    )

    return(response.candidates[0].content.parts[0].text)




# FUNCTION TO GET NEWS OF INTEREST
def get_news(topic: str):
    """
    fetches latest news headlines from an API

    args:
    topic(str):topic top search news for(eg- technology , cricket etc)
    """
    try:
        api_key="YOUR_API_KEY"
        url= f"https://newsapi.org/v2/everything?q={topic}&apiKey={api_key}&pageSize=5&sortBy=publishedAt"
        response =requests.get(url)
        return response.json().get("articles",[])
    except requests.exceptions.RequestException as e:
        return{"error": str(e)}


# FUNCTION TO SUMMARIZE THE NEWS
def news_summarizer(url):
    response= client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"summarize news from the url:- {url}, dont add sentences like from where the articles is ,in this article etc. Just give clear and crisp summary.",
    )

    return response.text



# FUNCTION TO GET FORECAST OF ENTIRE DAY FOR AN CITY AND PLACES TO VISIT FOR AN CITY.
def get_forcasted_weather(city: str):
    """
    LLM TOOL:- fetches forecasted weather and tourist places to visit for the given city.

    args:
      city(str):city name (eg. Delhi , Dehradun)
    """

    try:

        grounding_tool=types.Tool(
            google_search=types.GoogleSearch()
        )

        response= client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"""
            Provide the detailed weather forecast for {city} on {datetime.date.today()}.
            Then also list the top recommended places to visit in {city} on the same date.
            Format the response clearly so it can be used by another planning agent.
            """,
            config= types.GenerateContentConfig(
                    tools=[grounding_tool]
               )
        )


        return response.text

    except Exception as e:
        return {"error": str(e)}



# FUNCTION TO FIND THE LOCAL EVENTS
def find_local_events(city: str):
    """
    finds local events for a given city using an API.

    args:
    city(str):city name (eg :- Dehradun , Delhi)
    """

    try:
        api_key="YOUR_API_KEY"
        url= f"https://serpapi.com/search.json?engine=google_events&q=Events in {city}&api_key={api_key}"
        response =requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return{"error": str(e)}




# FUNCTION FOR SMART PLANNER
def smart_plan(city):
    prompt=f"""
    You are a smart travel and event planner assistant.
    Your job is to create a personalized day itinerary for the user in a given {city}.

    You are given:

    Weather forecast for the {city} (with temperature, rain chances, humidity, etc.).

    Upcoming events in the {city} (with title, date, time, venue, description, and link).

    List of recommended places to visit in the {city}.

    The user’s available time window for the day.

    Instructions:

    Always use weather conditions to decide between indoor and outdoor activities.

    Organize the plan chronologically (Morning → Afternoon → Evening).

    Mix tourist attractions + events + leisure breaks so the day feels balanced.

    When recommending events, check if the event timing fits the user’s availability.

    Always include event links when mentioning them.

    Suggest lunch/dinner breaks with general recommendations (local cuisine or malls).

    If multiple good options exist (e.g., 2 events at the same time), present them as choices.

    Keep the tone friendly and actionable, like a local guide making the plan.
    Always give the events happening in the city.

    Input Example:

    Weather Forecast:
    On Saturday, August 23, 2025, Chandigarh is expected to be cloudy with a maximum temperature ranging from 30°C to 34°C (86°F to 93°F) and a minimum temperature between 25°C and 26°C (77°F to 79°F). There is a 25% to 65% chance of rain during the day and a 40% to 45% chance of rain at night. The humidity is anticipated to be around 82% to 86%.

    Places to Visit:

    Rock Garden

    Sukhna Lake

    Rose Garden

    Elante Mall

    Events:

    🎤 Halki Halki Fati by Vikas Kush Sharma
    📅 Sat, Aug 23, 5:30 – 8:00 PM
    📍 The Laugh Club, Chandigarh
    🔗 https://allevents.in/chandigarh/halki-halki-fati-by-vikas-kush-sharma/3900027700476104

    🎤 Founders Meet | Chandigarh
    📅 Sat, Aug 23, 4 – 7 PM
    📍 Innovation Mission Punjab
    🔗 https://www.district.in/events/founders-meet-chandigarh-august-23-aug23-2025-buy-tickets

    🎤 Saturday Comedy Evening At Tagore Theatre
    📅 Sat, Aug 23, 7 – 9:30 PM
    📍 Tagore Theatre, Chandigarh
    🔗 https://www.shoutlo.com/events/saturday-comedy-evening-chandigarh

    User’s Available Time:
    9:00 AM – 9:00 PM

    Output Example:

    ✨ Your Personalized Day Plan for Chandigarh (Aug 23, 2025):

    🌤️ Morning (9:00 AM – 12:00 PM)

    Begin your day at Sukhna Lake with a peaceful lakeside walk (perfect in cloudy weather).

    Visit the artistic Rock Garden, which is outdoors but comfortable in today’s mild temperature.

    🍴 Lunch (12:30 PM – 2:00 PM)

    Try Chandigarh’s local food at Pal Dhaba, or if it rains, head to Elante Mall for indoor dining.

    🎭 Afternoon (2:30 PM – 5:30 PM)

    If you’re into startups and networking, attend Founders Meet | Chandigarh (4–7 PM) 👉 Event Link
    .

    Otherwise, enjoy a stroll at the Rose Garden.

    🎤 Evening Entertainment (6:00 PM – 9:00 PM)

    Comedy lovers can catch Halki Halki Fati by Vikas Kush Sharma (5:30–8:00 PM) 👉 Event Link
    .

    Alternatively, laugh your heart out at Saturday Comedy Evening At Tagore Theatre (7–9:30 PM) 👉 Event Link
    .

    ✅ This plan balances sightseeing, food, and entertainment while considering today’s cloudy weather.
    """

    response= client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config= types.GenerateContentConfig(
            tools=[find_local_events,get_forcasted_weather]
        )
    )

    return response.candidates[0].content.parts[0].text

abc=smart_plan("delhi")
print(abc)
