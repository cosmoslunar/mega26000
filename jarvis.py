import os import sys import subprocess import threading

Auto install required packages

required = [ "google-generativeai",  # Gemini API "speechrecognition", "pyaudio", "pyttsx3" ]

for pkg in required: try: import(pkg) except ImportError: subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import speech_recognition as sr import pyttsx3 import google.generativeai as genai

Initialize Gemini API

api_key = os.getenv("GOOGLE_API_KEY") if not api_key: print("[ERROR] Please set your Google API Key in the environment variable GOOGLE_API_KEY.") sys.exit(1)

genai.configure(api_key=api_key)

Text-to-speech engine

engine = pyttsx3.init() engine.setProperty('rate', 170)

Voice recognition

recognizer = sr.Recognizer() microphone = sr.Microphone()

running = False

def speak(text): print("Jarvis:", text) engine.say(text) engine.runAndWait()

def ask_gemini(prompt): try: model = genai.GenerativeModel("gemini-2.5-flash") response = model.generate_content(prompt) return response.text except Exception as e: print("Error with Gemini 2.5, trying Gemini 2.0...") model = genai.GenerativeModel("gemini-2.0-flash") response = model.generate_content(prompt) return response.text

def listen_loop(): global running with microphone as source: recognizer.adjust_for_ambient_noise(source) speak("Voice recognition started. Speak now.") while running: try: audio = recognizer.listen(source, timeout=5) command = recognizer.recognize_google(audio, language="en-US") print("You:", command)

if command.lower() in ["stop", "exit", "quit"]:
                running = False
                speak("Stopping voice recognition.")
                break

            reply = ask_gemini(command)
            speak(reply)

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except Exception as e:
            print("Error:", e)
            continue

if name == "main": print("JARVIS•AI") print("Usage: type 'start' to begin, 'end' to quit. Speak to interact.") while True: cmd = input("> ").strip().lower() if cmd == "start" and not running: running = True t = threading.Thread(target=listen_loop) t.start() elif cmd == "end": running = False speak("Goodbye.") break