# Smart-Assistant-AM-Agent
*Your day, intelligently curated.*

Smart Assistant AM-Agent is a comprehensive GenAI dashboard designed to streamline your morning routine. By leveraging the Gemini 2.5 Flash model and real-time data integrations, this agent transforms raw data into actionable daily insights—from human-friendly weather reports to curated news summaries and personalized travel itineraries.

**Key Features**

    Smart Planning Agent: Generates a chronological daily itinerary (Morning, Afternoon, Evening) by intelligently cross-referencing weather forecasts, local events, and tourist attractions.

    Conversational Weather Reports: Converts complex JSON data from the OpenWeather API into a friendly report that includes practical clothing and gear suggestions (e.g., suggesting an umbrella if rain is forecasted).

    AI News Summarizer: Fetches the latest headlines based on your specific interests (e.g., Tech, Sports) and provides "clear and crisp" summaries for quick reading.

    Real-Time Event Discovery: Integrates with SerpApi to find local events happening in your city, including venues and direct ticket links.

    Morning Inspiration: Features a dedicated home page with motivational quotes and refreshing imagery to start your day on a positive note.

**Tech Stack**

    Frontend: Streamlit

    LLM: Google Gemini 2.5 Flash & 2.5 Flash-Lite

    External APIs:

        OpenWeather API: Real-time weather data.

        NewsAPI: Global news headlines.

        SerpApi: Google Search and Google Events data.

        Google Search Grounding: Used for forecasted weather and tourist recommendations.
