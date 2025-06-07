import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import random
import time
import requests
import json
import wikipedia
import pyjokes
import pygame
import wolframalpha
import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import PhotoImage, scrolledtext
import threading
from PIL import Image, ImageTk # Pillow library for image manipulation

# --- Configuration ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')
try:
    engine.setProperty('voice', voices[4].id) # Attempt to set a female voice
except IndexError:
    print("Warning: Female voice not found, using default.")
engine.setProperty('rate', 170)

# IMPORTANT: Replace these with your actual API keys and paths!
# Get a free API key from https://developer.wolframalpha.com/portal/
WOLFRAM_APP_ID = "YOUR_WOLFRAM_APP_ID" # <--- CONFIGURE THIS
# You already have one for OpenWeatherMap, but ensure it's correct if issues arise
OPENWEATHER_API_KEY = "87ce813a15ad3d1c0f079934ed85ab26"

# IMPORTANT: Replace with your actual email and an app password (not your main email password)
# For Gmail, generate an app password: https://myaccount.google.com/apppasswords
EMAIL_ADDRESS = "dishanksingh36@gmail.com" # <--- CONFIGURE THIS
EMAIL_PASSWORD = "uawrvtubskpplooo" # <--- CONFIGURE THIS

# IMPORTANT: Update this path to your music directory
MUSIC_DIR = "C:\\Users\\Public\\Music\\Sample Music" # <--- CONFIGURE THIS

# IMPORTANT: Create a dictionary of contacts for WhatsApp/Email
# You'll need to manually add names and phone numbers/email addresses
CONTACTS = {
    "dhruv": {"phone": "+919335963323", "email": "dhruvkumar60229@gmail.com"},
    "divyansh": {"phone": "+916387814302", "email": "divyanshgup ta173@gmail.com"},
    # Add more contacts as needed
}

# Initialize pygame mixer (required for local music playback)
try:
    pygame.mixer.init()
except Exception as e:
    print(f"Pygame mixer initialization failed: {e}. Local music playback might not work.")

# Global variables for Tkinter UI elements
root = None
response_text_widget = None
user_input_label = None
status_label = None # New label for status messages
listening_animation_label = None # New label for listening animation
speaking_animation_label = None # New label for speaking animation
# List to hold PhotoImage objects for GIF animation
listening_frames = []
speaking_frames = []
animation_index = 0
animation_running = False

# --- SPEECH RECOGNITION ---
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_ui_status("Listening...")
        start_listening_animation()
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        stop_listening_animation()
    try:
        update_ui_status("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        update_ui_input(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        update_ui_input("You: (unclear audio)")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please check your internet connection.")
        return ""
    except Exception as e:
        print(f"Speech recognition error: {e}")
        speak("An unexpected error occurred during recognition. Please try again.")
        return ""

# --- TEXT-TO-SPEECH ---
def speak(text):
    print(f"AVATAR: {text}")
    update_ui_response(f"AVATAR: {text}")
    start_speaking_animation()
    engine.say(text)
    engine.runAndWait()
    stop_speaking_animation()

def update_ui_response(text):
    """Updates the Tkinter Text widget with new responses."""
    if response_text_widget and root:
        root.after(0, lambda: _update_text_widget(response_text_widget, text))

def _update_text_widget(widget, text):
    widget.config(state='normal')
    widget.insert(tk.END, text + "\n")
    widget.see(tk.END)
    widget.config(state='disabled')

def update_ui_status(text):
    """Updates the Tkinter status label."""
    if status_label and root:
        root.after(0, lambda: status_label.config(text=text))

def update_ui_input(text):
    """Updates the Tkinter user input label."""
    if user_input_label and root:
        root.after(0, lambda: user_input_label.config(text=text))

# --- ANIMATION FUNCTIONS ---
def load_gif_frames(gif_path, target_list):
    try:
        image = Image.open(gif_path)
        for i in range(image.n_frames):
            image.seek(i)
            # Resize frames for consistency and performance
            resized_frame = image.resize((80, 80), Image.Resampling.LANCZOS)
            target_list.append(ImageTk.PhotoImage(resized_frame))
    except Exception as e:
        print(f"Error loading GIF from {gif_path}: {e}")
        return False
    return True

def animate_listening(ind):
    global animation_index, animation_running
    if not animation_running:
        listening_animation_label.config(image='')
        return

    animation_index = ind
    frame = listening_frames[animation_index]
    listening_animation_label.config(image=frame)
    animation_index = (animation_index + 1) % len(listening_frames)
    root.after(100, lambda: animate_listening(animation_index)) # Adjust speed here

def start_listening_animation():
    global animation_running
    if not listening_frames:
        return
    animation_running = True
    listening_animation_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    animate_listening(0)

def stop_listening_animation():
    global animation_running
    animation_running = False
    if listening_animation_label:
        listening_animation_label.place_forget() # Hide the label

def animate_speaking(ind):
    global animation_index, animation_running
    if not animation_running:
        speaking_animation_label.config(image='')
        return

    animation_index = ind
    frame = speaking_frames[animation_index]
    speaking_animation_label.config(image=frame)
    animation_index = (animation_index + 1) % len(speaking_frames)
    root.after(100, lambda: animate_speaking(animation_index)) # Adjust speed here

def start_speaking_animation():
    global animation_running
    if not speaking_frames:
        return
    animation_running = True
    speaking_animation_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)
    animate_speaking(0)

def stop_speaking_animation():
    global animation_running
    animation_running = False
    if speaking_animation_label:
        speaking_animation_label.place_forget() # Hide the label

# --- WOLFRAM ALPHA ---
def wolfram_query(query_text):
    """Queries Wolfram Alpha for an answer."""
    if not WOLFRAM_APP_ID or WOLFRAM_APP_ID == "YOUR_WOLFRAM_APP_ID":
        return None
    try:
        client = wolframalpha.Client(WOLFRAM_APP_ID)
        res = client.query(query_text)
        answer = next(res.results).text
        return answer
    except StopIteration:
        return None
    except Exception as e:
        print(f"Wolfram Alpha error: {e}")
        return None

# --- EMAIL FUNCTION ---
def send_email(receiver_email, subject, body):
    """Sends an email using the configured Gmail account."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD or EMAIL_ADDRESS == "your_email@gmail.com":
        speak("Email sender address or app password is not configured. Please add them in the code.")
        return False
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending error: {e}. Ensure App Password is correct for Gmail and less secure apps access is on (or 2FA with App Password).")
        speak("Sorry, I encountered an error while sending the email. Please check your email configuration and internet connection.")
        return False


# --- WHATSAPP FUNCTION ---
def send_whatsapp_message(receiver_name, message):
    """Sends a WhatsApp message to a contact."""
    receiver_name_lower = receiver_name.lower()
    if receiver_name_lower in CONTACTS and "phone" in CONTACTS[receiver_name_lower]:
        phone_number = CONTACTS[receiver_name_lower]["phone"]
        speak(f"Composing WhatsApp message for {receiver_name}.")
        # Use web.whatsapp.com for sending messages
        whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={requests.utils.quote(message)}"
        webbrowser.open(whatsapp_url)
        speak("I've opened WhatsApp Web with your message. You may need to press send in the browser.")
        return True
    else:
        speak(f"Sorry, I don't have a phone number for {receiver_name} in my contacts.")
        speak("Please add the contact and their phone number in the 'CONTACTS' dictionary in the code.")
        return False

# --- TASK HANDLING ---
def handle_command(query):
    """Processes the user's spoken command."""
    if not query:
        return True

    # Open specific websites
    if "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open github" in query:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")
    elif "open linkedin" in query:
        speak("Opening LinkedIn.")
        webbrowser.open("https://www.linkedin.com")

    # Search on Google
    elif "search" in query:
        search_query = query.replace("search", "").strip()
        if search_query:
            speak(f"Searching Google for {search_query}.")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            speak("What would you like me to search for?")

    # Play music
    elif "play" in query and "on youtube" in query:
        song_name = query.replace("play", "").replace("on youtube", "").strip()
        if song_name:
            speak(f"Searching YouTube for {song_name} and attempting to play the first result.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}")
        else:
            speak("What song would you like me to play on YouTube?")

    elif "play music" in query or "play song" in query or "play a song" in query:
        generic_music_phrases = ["play music", "play song", "play a song", "play some music", "play something"]
        song_name = query
        for phrase in generic_music_phrases:
            song_name = song_name.replace(phrase, "", 1).strip()

        song_name = song_name.replace("please", "").strip()
        song_name = song_name.replace("for me", "").strip()

        if song_name and len(song_name.split()) >= 1:
            speak(f"Searching YouTube for {song_name} and attempting to play the first result.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}")
        else:
            songs = []
            if os.path.exists(MUSIC_DIR):
                songs = [os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR)
                                if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]

            if songs:
                speak("Playing a random song from your local directory.")
                try:
                    pygame.mixer.music.load(random.choice(songs))
                    pygame.mixer.music.play()
                except pygame.error as e:
                    print(f"Error playing local music: {e}. Opening YouTube for random music.")
                    speak("Error playing local music. Opening YouTube for random music.")
                    webbrowser.open("https://www.youtube.com/feed/trending")
            else:
                speak("No local music found. Opening YouTube for random music.")
                webbrowser.open("https://www.youtube.com/feed/trending")

    elif "stop music" in query:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            speak("Music stopped.")
        else:
            speak("No music is currently playing.")
    elif "pause music" in query:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            speak("Music paused.")
        else:
            speak("No music is currently playing.")
    elif "unpause music" in query or "resume music" in query:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.unpause()
            speak("Music resumed.")
        elif pygame.mixer.music.get_pos() > -1:
            pygame.mixer.music.unpause()
            speak("Resuming playback.")
        else:
            speak("No music was paused or playing to resume.")

    # Greetings
    elif any(word in query for word in ["hello", "hi", "hey", "avatar", "hello avatar"]):
        greetings = ["Hello Dishank! How can I help you today?",
                    "Hey Dishank! What can I do for you?",
                    ]
        speak(random.choice(greetings))
        
    elif any(word in query for word in ["Turn off", "Quit now", "Deactivate Yourself", "exit", "stop", "shutdown avatar", "close program"]):
        speak("Goodbye! Have a great day.")
        return False

    # Date and Time
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")

    # System Control (Use with caution!)
    elif "shutdown computer" in query or "shutdown system" in query:
        speak("Are you sure you want to shut down the system? Say 'yes' to confirm.")
        confirmation = listen()
        if "yes" in confirmation:
            speak("Shutting down the system. Goodbye!")
            if os.name == 'nt': # For Windows
                os.system("shutdown /s /t 1")
            else: # For Linux/macOS
                os.system("sudo shutdown -h now")
        else:
            speak("Shutdown cancelled.")
    elif "restart computer" in query or "restart system" in query:
        speak("Are you sure you want to restart the system? Say 'yes' to confirm.")
        confirmation = listen()
        if "yes" in confirmation:
            speak("Restarting the system.")
            if os.name == 'nt': # For Windows
                os.system("shutdown /r /t 1")
            else: # For Linux/macOS
                os.system("sudo shutdown -r now")
        else:
            speak("Restart cancelled.")

    # Wikipedia Search
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query_wiki = query.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query_wiki, sentences=3)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple matches. Can you be more specific?")
            print(f"Disambiguation options: {e.options}")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find that on Wikipedia.")
        except Exception as e:
            print(f"Wikipedia error: {e}")
            speak("An error occurred while searching Wikipedia.")

    # Weather Information
    elif "weather" in query:
        speak("Which city's weather would you like to know?")
        city = listen()
        if city:
            country_code = "in"

            if " in " in city:
                parts = city.split(" in ")
                city = parts[0].strip()
                country_part = parts[1].strip().lower()

                if "india" in country_part: country_code = "in"
                elif "usa" in country_part or "united states" in country_part: country_code = "us"
                elif "uk" in country_part or "united kingdom" in country_part: country_code = "gb"
                elif "canada" in country_part: country_code = "ca"
                elif "australia" in country_part: country_code = "au"
                elif "germany" in country_part: country_code = "de"
                elif "france" in country_part: country_code = "fr"
                elif "japan" in country_part: country_code = "jp"
                else:
                    speak(f"I couldn't determine the country for '{country_part}'. Assuming India.")

            if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
                speak("OpenWeatherMap API key is not configured. Please add it to the code.")
                return True

            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={OPENWEATHER_API_KEY}&units=metric"
                response = requests.get(url)
                data = json.loads(response.text)

                if data["cod"] == 200:
                    weather = data["weather"][0]["description"]
                    temp = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    speak(f"Weather in {city}: {weather}. Temperature: {temp}°C, Humidity: {humidity}%.")
                else:
                    if data["cod"] == "404":
                        speak(f"Sorry, I couldn't find weather data for '{city}'. Please try a different city or specify the country.")
                    elif data["cod"] == 401:
                        speak("I'm having trouble with the weather service. It seems my Open Weather Map API key is invalid or not activated. Please check your API key on the Open Weather Map website.")
                        print(f"OpenWeatherMap API Error: Invalid API key. Please see https://openweathermap.org/faq#error401 for more info.")
                    else:
                        speak(f"An error occurred while fetching weather for '{city}'. Error code: {data['cod']}.")
                        print(f"OpenWeatherMap API Error: {data.get('message', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                print(f"Network error fetching weather: {e}")
                speak("Sorry, I'm having trouble connecting to the weather service. Please check your internet connection.")
            except Exception as e:
                print(f"An unexpected error occurred while fetching weather: {e}")
                speak("Sorry, I couldn't fetch the weather information right now due to an unexpected error.")
        else:
            speak("Please specify a city.")

    # Jokes
    elif "tell me a joke" in query or "joke" in query:
        speak(pyjokes.get_joke())


    # Set Reminders
    elif "set a reminder" in query or "remind me" in query:
        speak("What should I remind you about?")
        reminder_text = listen()
        if reminder_text:
            speak("When should I remind you? Please say in a format like 'in 5 minutes' or 'in 1 hour and 30 minutes'.")
            try:
                time_input = listen()
                total_seconds = 0
                if "hour" in time_input:
                    try:
                        parts = time_input.split()
                        for i, part in enumerate(parts):
                            if "hour" in part and i > 0 and parts[i-1].isdigit():
                                total_seconds += int(parts[i-1]) * 3600
                                break
                    except ValueError: pass
                if "minute" in time_input:
                    try:
                        parts = time_input.split()
                        for i, part in enumerate(parts):
                            if "minute" in part and i > 0 and parts[i-1].isdigit():
                                total_seconds += int(parts[i-1]) * 60
                                break
                    except ValueError: pass
                if "second" in time_input:
                    try:
                        parts = time_input.split()
                        for i, part in enumerate(parts):
                            if "second" in part and i > 0 and parts[i-1].isdigit():
                                total_seconds += int(parts[i-1])
                                break
                    except ValueError: pass

                if total_seconds > 0:
                    hours_display = total_seconds // 3600
                    minutes_display = (total_seconds % 3600) // 60
                    seconds_display = total_seconds % 60

                    time_string = []
                    if hours_display > 0: time_string.append(f"{hours_display} hours")
                    if minutes_display > 0: time_string.append(f"{minutes_display} minutes")
                    if seconds_display > 0: time_string.append(f"{seconds_display} seconds")

                    speak(f"I'll remind you about {reminder_text} in {' and '.join(time_string)}.")
                    threading.Thread(target=set_timed_reminder, args=(total_seconds, reminder_text), daemon=True).start()
                else:
                    speak("Invalid time duration provided. Please try again.")
            except Exception as e:
                print(f"Reminder setup error: {e}")
                speak("Sorry, I couldn't set the reminder.")
        else:
            speak("I need to know what to remind you about.")

    # Send WhatsApp Message
    elif "send whatsapp message" in query or "whatsapp" in query:
        speak("Who would you like to send a message to?")
        receiver_name = listen()
        if receiver_name:
            speak(f"What message would you like to send to {receiver_name}?")
            message_content = listen()
            if message_content:
                send_whatsapp_message(receiver_name, message_content)
            else:
                speak("What's the message you want to send?")
        else:
            speak("Please tell me the name of the recipient.")

    # Send Email (already present, just explicitly handled here)
    elif "send an email" in query or "send email" in query:
        speak("Who is the recipient of the email?")
        recipient_name = listen()
        if recipient_name:
            recipient_email = CONTACTS.get(recipient_name.lower(), {}).get("email")
            if recipient_email:
                speak("What is the subject of the email?")
                subject = listen()
                speak("What is the body of the email?")
                body = listen()
                if send_email(recipient_email, subject, body):
                    speak("Email sent successfully!")
                else:
                    speak("Failed to send email.")
            else:
                speak(f"I don't have an email address for {recipient_name} in my contacts.")
                speak("Please add the contact and their email address in the 'CONTACTS' dictionary in the code.")
        else:
            speak("Please tell me the name of the recipient.")

    # Calculations and General Knowledge (Wolfram Alpha / Wikipedia)
    elif "calculate" in query or "what is" in query or "who is" in query or "tell me about" in query:
        search_term = query.replace("calculate", "").replace("what is", "").replace("who is", "").replace("tell me about", "").strip()
        if not search_term:
            speak("What would you like me to calculate or tell you about?")
            return True

        wolfram_attempted = False
        if WOLFRAM_APP_ID and WOLFRAM_APP_ID != "YOUR_WOLFRAM_APP_ID":
            wolfram_attempted = True
            speak(f"Searching Wolfram Alpha for {search_term}...")
            wolfram_result = wolfram_query(search_term)
            if wolfram_result:
                speak(wolfram_result)
                return True
            else:
                pass

        speak(f"Searching Wikipedia for {search_term}...")
        try:
            summary = wikipedia.summary(search_term, sentences=3)
            speak(summary)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple matches. Can you be more specific?")
            print(f"Disambiguation options for '{search_term}': {e.options}")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I couldn't find any information about {search_term} on Wikipedia.")
        except Exception as e:
            print(f"Wikipedia error for '{search_term}': {e}")
            speak("An error occurred while searching for that information.")

    # Exit Commands
    elif any(word in query for word in ["exit", "stop", "goodbye", "bye", "shutdown avatar", "close program"]):
        speak("Goodbye! Have a great day.")
        return False

    # Default/Fallback Response
    else:
        responses = [
            "I'm not sure I understand that. Could you rephrase or try a different command?",
            "I don't have that capability yet. I'm still learning.",
            "Sorry, I can't help with that right now. Please try something else.",
            "I am programmed to assist with specific tasks. What would you like me to do?"
        ]
        speak(random.choice(responses))

    return True

# --- Reminder Thread Function ---
def set_timed_reminder(seconds, reminder_text):
    """Waits for specified seconds and then speaks the reminder."""
    time.sleep(seconds)
    speak(f"Reminder: {reminder_text}")

# --- UI Setup ---
def create_ui():
    """Sets up the Tkinter graphical user interface."""
    global root, response_text_widget, user_input_label, status_label, listening_animation_label, speaking_animation_label, listening_frames, speaking_frames

    root = tk.Tk()
    root.title("AVATAR Voice Assistant")

    # Desired window size
    window_width = 1366
    window_height = 660

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate x and y coordinates to center the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set geometry with center position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")  # Deep dark blue


    # Load GIF frames for animations
    if not load_gif_frames("listening_animation.gif", listening_frames): # Replace with your GIF path
        print("Listening animation GIF not found or corrupted. Animations will not play.")
    if not load_gif_frames("speaking_animation.gif", speaking_frames): # Replace with your GIF path
        print("Speaking animation GIF not found or corrupted. Animations will not play.")

    # Title label with gradient-like effect using multiple labels (or canvas for true gradient)
    title_frame = tk.Frame(root, bg="#1a1a2e")
    title_frame.pack(pady=(20, 10))

    title_colors = ["#e0e0e0", "#b0c4de", "#87ceeb"] # Light grey, light steel blue, sky blue
    for i, char in enumerate("AVATAR"):
        label = tk.Label(title_frame, text=char, font=('Orbitron', 36, 'bold'), fg=title_colors[i % len(title_colors)], bg="#1a1a2e")
        label.pack(side=tk.LEFT)

    # Status label (e.g., "Initializing AVATAR...", "Listening...", "Speaking...")
    status_label = tk.Label(root, text="Initializing AVATAR...", font=('Arial', 14, 'italic'), fg="#7f8c8d", bg="#1a1a2e")
    status_label.pack(pady=(0, 10))

    # Frame for response text
    response_frame = tk.Frame(root, bg="#2c3e50", bd=2, relief="flat", highlightbackground="#3498db", highlightthickness=2) # Blue border
    response_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # ScrolledText widget for AVATAR's responses
    response_text_widget = scrolledtext.ScrolledText(response_frame, height=15, width=70, state='disabled', wrap='word',
                                                    font=('Consolas', 11), fg="#e0f2f7", bg="#2c3e50",
                                                    insertbackground="#e0f2f7", selectbackground="#3498db",
                                                    relief="flat", padx=10, pady=10)
    response_text_widget.pack(fill="both", expand=True)

    # Label to display user input (e.g., "You: What is the weather?")
    user_input_label = tk.Label(root, text="", font=('Arial', 14, 'bold'), fg="#f39c12", bg="#1a1a2e") # Orange for user input
    user_input_label.pack(pady=(10, 5))

    # Animation labels
    listening_animation_label = tk.Label(root, bg="#1a1a2e")
    speaking_animation_label = tk.Label(root, bg="#1a1a2e")

    # Start the voice assistant loop in a separate thread
    threading.Thread(target=start_voice_assistant, daemon=True).start()

    root.mainloop()

# --- MAIN EXECUTION LOOP FOR VOICE ASSISTANT ---
def start_voice_assistant():
    """Main loop for the voice assistant's operations."""
    speak("Welcome to AVATAR. How can I help you today?")
    update_ui_status("Ready.")

    running = True
    while running:
        try:
            command = listen()
            if command:
                running = handle_command(command)
            else:
                update_ui_status("Ready.") # Reset status if nothing recognized
                pass
        except KeyboardInterrupt:
            speak("AVATAR shutting down via keyboard interrupt.")
            running = False
        except Exception as e:
            print(f"Error in main assistant loop: {e}")
            speak("Sorry, I encountered a critical error and need to shut down. Please check the console for details.")
            running = False

    speak("AVATAR session ended.")
    if root:
        root.after(100, root.destroy)

# --- Entry Point ---
if __name__ == "__main__":
    create_ui()