import pyttsx3
import speech_recognition as sr
import subprocess
import datetime
import requests
import os
import psutil

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        user_input = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {user_input}")
        return user_input.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Request error: {e}")
        return ""

# Function to respond to greetings or farewell messages
def respond_to_greeting(user_input):
    hour = datetime.datetime.now().hour
    if "good morning" in user_input:
        speak("Good morning! How are you ?")
    elif "good afternoon" in user_input:
        speak("Good afternoon! How can I help you?")
    elif "good evening" in user_input:
        speak("Good evening! What's on your mind?")
    elif any(greeting in user_input for greeting in ["good night", "goodbye"]):
        speak("Goodbye! Have a great day.")
        exit()
    else:
        speak("Hello! What can I do for you now?")

# Function to open applications
def open_application(app_path, app_name):
    try:
        subprocess.Popen([app_path])
        speak(f"Opening {app_name}.")
    except Exception as e:
        speak(f"Unable to open {app_name}. Error: {str(e)}")

# Function to close applications
def close_application(app_name, display_name):
    try:
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == app_name.lower():
                proc.terminate()
                found = True
                speak(f"Closing {display_name}.")
        if not found:
            speak(f"{display_name} is not running.")
    except Exception as e:
        speak(f"Unable to close {display_name}. Error: {str(e)}")

# Function to open camera
def open_camera():
    try:
        os.system("start microsoft.windows.camera:")
        speak("Opening camera.")
    except Exception as e:
        speak(f"Unable to open camera. Error: {str(e)}")

# Function to tell a joke
def tell_joke():
    speak("Why did the scarecrow win an award? Because he was outstanding in his field!")

# Function to get weather information
def get_weather(city):
    api_key = "2166713b06098ce4ae01e3fec5a73233"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"The weather in {city} is currently {weather_description} with a temperature of {temp} degrees Celsius.")
        else:
            speak("Sorry, I couldn't fetch the weather information.")
    except requests.exceptions.RequestException as e:
        speak(f"Error fetching weather: {e}")

# Function to get current year
def get_current_year():
    current_year = datetime.datetime.now().year
    speak(f"The current year is {current_year}.")

# Function to get current date
def get_current_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {current_date}.")

# Function to terminate the assistant
def terminate_assistant():
    speak("Goodbye! Have a great day.")
    exit()

# Function for small talk
def small_talk():
    speak("I'm sorry, I didn't understand that. Can you ask me something else?")

# Function to process commands
def process_command(user_input):
    if "hello" in user_input:
        respond_to_greeting(user_input)
    elif "i am fine" in user_input:
        speak("Okay . Have a Nice day ..Now Tell Me  How can I help you?")
    elif "open notepad" in user_input:
        open_application("notepad.exe", "Notepad")
    elif "open calculator" in user_input:
        open_application("calc.exe", "Calculator")
    elif "open paint" in user_input:
        open_application("mspaint.exe", "Paint")
    elif "open browser" in user_input:
        open_application("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", "Google Chrome")  # Update path if necessary
    elif "open camera" in user_input:
        open_camera()
    elif "tell me a joke" in user_input:
        tell_joke()
    elif "tell me weather" in user_input:
        get_weather("Tekkali")  # Replace with user's location or ask for location input
    elif "what is the year" in user_input:
        get_current_year()
    elif "what is the date" in user_input:
        get_current_date()
    elif "close notepad" in user_input:
        close_application("notepad.exe", "Notepad")
    elif "close calculator" in user_input:
        close_application("calc.exe", "Calculator")
    elif "close paint" in user_input:
        close_application("mspaint.exe", "Paint")
    elif "close browser" in user_input:
        close_application("chrome.exe", "Google Chrome")
    elif any(greeting in user_input for greeting in
             ["good morning", "good afternoon", "good evening", "good night", "goodbye"]):
        respond_to_greeting(user_input)
    elif "exit" in user_input:
        terminate_assistant()
    else:
        small_talk()
# Main function to handle interaction
def main():
    speak("Hello! I am your Talking bot. How can I help you today?")

    while True:
        # Listen for user input
        user_input = recognize_speech()

        if user_input:
            process_command(user_input)

if __name__ == "__main__":
    main()
