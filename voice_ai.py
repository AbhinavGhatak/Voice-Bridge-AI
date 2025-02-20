import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from transformers import pipeline
from googletrans import Translator
from langdetect import detect
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

# Initialize models and tools
emotion_classifier = pipeline("sentiment-analysis", model="j-hartmann/emotion-english-distilroberta-base")
translator = Translator()
recognizer = sr.Recognizer()

API_URL = "https://api.mistral.ai/v1/completions"  # Switched to Mistral AI
API_KEY = "your_mistral_api_key"  # Replace with actual key

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def speech_to_text():
    """Captures real-time speech input and converts it to text."""
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣 Recognized Speech: {text}")
        return text
    except Exception as e:
        print("🚨 Error in Speech-to-Text:", e)
        return ""

def detect_emotion(text):
    """Detects emotion from text."""
    try:
        emotions = emotion_classifier(text)
        dominant_emotion = max(emotions, key=lambda x: x['score'])['label']
        return dominant_emotion
    except Exception as e:
        print("🚨 Error detecting emotion:", e)
        return "neutral"

def generate_response(prompt, emotion):
    """Generates a response using Mistral AI API."""
    if not API_KEY or API_KEY == "your_mistral_api_key":
        print("🚨 Error: Missing or Invalid API Key!")
        return "I'm sorry, but I couldn't process your request due to API issues."
    
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "mistral-tiny", "prompt": f"You are an AI. Respond in a {emotion} tone.\nUser: {prompt}\nAI:", "max_tokens": 100}
        
        response = requests.post(API_URL, json=payload, headers=headers)
        response_data = response.json()
        
        # Debugging: Print API response
        print("🔍 Raw API Response:", response_data)
        
        return response_data.get("choices", [{}])[0].get("text", "I'm sorry, but I couldn't process your request.").strip()
    except Exception as e:
        print("🚨 AI API Error:", e)
        return "I'm sorry, but I couldn't process your request."

def text_to_speech(text, lang='en'):
    """Converts text to speech using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang)
        output_path = "output.mp3"
        tts.save(output_path)
        playsound.playsound(output_path)
        os.remove(output_path)
    except Exception as e:
        print("🚨 Text-to-Speech Error:", e)

@app.get("/start")
def start_voice_assistant():
    """Runs the full voice assistant loop."""
    while True:
        user_query = speech_to_text()
        if user_query.lower() == "exit":
            print("👋 Exiting Voice Bridge AI.")
            break
        if not user_query:
            continue
        
        emotion = detect_emotion(user_query)
        ai_response = generate_response(user_query, emotion)
        print(f"🤖 AI: {ai_response} [{emotion}]")
        text_to_speech(ai_response)
    return {"message": "Voice Assistant Stopped"}

if __name__ == "__main__":
    print("🚀 Voice Bridge AI Assistant is running! (Say 'exit' to stop)")
    start_voice_assistant()
