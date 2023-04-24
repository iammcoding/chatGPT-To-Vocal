import json
import requests
import speech_recognition as sr
import pyttsx3

# Create a recognizer instance
r = sr.Recognizer()

# Define the function to capture speech and convert it to text
def speech_to_text():
    with sr.Microphone() as source:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)

        # Listen for user input
        print("Speak something...")
        audio = r.listen(source)

        # Use Google Speech Recognition to convert audio to text
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print(f"Request error: {e}")

# Define the function to generate AI response from user input
def gpt(user_input):
    # Set the endpoint URL
    url = "https://api.openai.com/v1/chat/completions"

    # Set the authorization header with your OpenAI API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer <OpenAI API KEY>"
    }

    # Set the data payload for the chat completion request, including the user's spoken input
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}]
    }

    # Send the POST request to the OpenAI API endpoint
    response = requests.post(url, headers=headers, data=json.dumps(data),verify=False)

    # Get the response data in JSON format
    response_data = response.json()

    # Extract AI response from the response data
    ai_response = response_data["choices"][0]["message"]["content"]

    # Return the AI response
    return ai_response

# Define the function to convert text to speech
def text_to_speech(text):
    # Create a new text-to-speech engine
    engine = pyttsx3.init()
    
    # Set the speed and volume of the speech
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
    
    # Say the text out loud
    engine.say(text)
    engine.runAndWait()

# Run the chatbot
while True:
    # Call the speech_to_text function to capture user input
    user_input = speech_to_text()

    # Generate AI response from user input
    ai_response = gpt(user_input)

    # Say the AI response out loud
    text_to_speech(ai_response)
