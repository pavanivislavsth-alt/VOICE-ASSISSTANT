# Importing necessary libraries
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import webbrowser
import random
import os

# Initializing speech recognition and text-to-speech engines
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to speak text
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize voice commands
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            
            # Remove wake word 'leo'
            if 'leo' in command:
                command = command.replace('leo', '')

    except:
        pass
    return command

# Main function to execute commands based on voice input
def run_leo():
    command = take_command()
    print(command)
    
    # Command handling based on keywords
    if 'play' in command:
        # Play music on YouTube
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        # Get and speak the current time
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        print('Current time is ' + time)
    elif 'tell me about' in command:
        # Fetch information from Wikipedia
        person = command.replace('tell me about', '')
        info = wikipedia.summary(person, 2)
        print(info)
        talk(info)
    elif 'joke' in command:
        # Tell a joke
        talk(pyjokes.get_joke())
        print(pyjokes.get_joke())
    elif 'weather' in command:
        # Get weather information for a specific city
        city = command.replace('weather in', '')
        weather_info = get_weather(city)
        print(weather_info)
        talk(weather_info)
    elif 'open website' in command:
        # Open a specific website
        website = command.replace('open website', '')
        url = f'https://www.google.com'
        webbrowser.open(url)
        talk(f'Opening Google website')
    elif 'search' in command:
        # Perform a web search
        search_query = command.replace('search', '')
        pywhatkit.search(search_query)
        talk(f'Searching for {search_query} on Google')
    elif 'send message' in command:
        # Send a WhatsApp message
        contact = 'pavani'
        message = 'Hello, how are you?'
        pywhatkit.sendwhatmsg(f'+916281696866', message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
        talk(f'Sending a WhatsApp message to {contact}')
    elif 'date' in command:
        # Get and speak the current date
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        print(date)
        talk(f'Today is {date}')
    elif 'compliment me' in command:
        # Generate and speak a compliment
        compliment = generate_compliment()
        talk(compliment)
        print(compliment)
    elif 'latest news' in command:
        # Get and speak the latest news headlines
        news_headlines = get_news()
        for headline in news_headlines:
            talk(headline)
            print(headline)
    elif 'shutdown' in command:
        # Shutdown the computer
        talk('Shutting down the computer.')
        os.system('shutdown /s /t 5')  # /s for shutdown, /t for time delay (1 second in this case)
    elif 'restart' in command:
        # Restart the computer
        talk('Restarting the computer.')
        os.system('shutdown /r /t 5')  # /r for restart, /t for time delay (1 second in this case)
    elif 'log off' in command:
        # Log off the computer
        talk('Logging off the computer.')
        os.system('shutdown /l')  # /l for log off
    elif 'start game' in command:
        # Start the trivia game
        trivia_game()
    elif 'quote of the day' in command:
        # Get and speak a quote of the day
        quote = get_quote_of_the_day()
        talk(quote)
        print(quote)
    elif 'your name' in command:
        # Introduce the virtual assistant
        talk("I'm your virtual assistant, but you can call me whatever you like!")
        print("I'm your virtual assistant, but you can call me whatever you like!")
    else:
        # Default response for unrecognized commands
        talk('Please say the command again')

# Function to get weather information for a city
def get_weather(city):
    base_url = f'https://api.open-meteo.com/weather?forecast=hourly&daily=7&timezone=Europe%2FBerlin&current_weather=yes&longitude=&latitude=&hourly=temperature_2m'

    try:
        params = {'city': city}
        weather_data = requests.get(base_url, params=params).json()
        current_temperature = weather_data['current_weather']['temperature_2m']
        return f'The current temperature in {city} is {current_temperature}°C.'
    except KeyError:
        return 'Sorry, I couldn\'t retrieve the weather information.'

# Function to generate a random compliment
def generate_compliment():
    compliments = [
        "You're doing great!",
        "You have a wonderful smile!",
        "You're incredibly smart!",
        "Your positive attitude is contagious!",
        "You're one of a kind!"
    ]
    return random.choice(compliments)

# Function to get the latest news headlines
def get_news():
    news_api_key = '5945632ecd7c4e928633891c85dc18e1'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}'
    response = requests.get(url)
    news_data = response.json()
    headlines = [article['title'] for article in news_data['articles']]
    return headlines

# Function to conduct a trivia game
def trivia_game():
    talk("Welcome to the Trivia Game! I will ask you three trivia questions. Let's see how many you can answer correctly.")
    print("Welcome to the Trivia Game! I will ask you three trivia questions. Let's see how many you can answer correctly.")
    questions = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "Which planet is known as the Red Planet?", "answer": "Mars"},
        {"question": "Who wrote Romeo and Juliet?", "answer": "William Shakespeare"},
    ]

    score = 0

    for question_data in questions:
        talk(question_data["question"])
        user_answer = take_command().lower()

        if user_answer == question_data["answer"].lower():
            talk("Correct! Well done.")
            print("Correct! Well done.")
            score += 1
        else:
            talk(f"Wrong! The correct answer is {question_data['answer']}.")
            print(f"Wrong! The correct answer is {question_data['answer']}.")

    talk(f"Game over. Your final score is {score} out of {len(questions)}.")
    print(f"Game over. Your final score is {score} out of {len(questions)}.")

# Function to get a quote of the day
def get_quote_of_the_day():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
    ]
    return random.choice(quotes)

# Main loop for continuously running the virtual assistant
while True:
    run_leo()
