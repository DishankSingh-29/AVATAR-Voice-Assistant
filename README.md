# AVATAR Voice Assistant

AVATAR is an advanced voice-controlled virtual assistant built with Python. It can perform various tasks like web searches, playing music, setting reminders, sending emails/WhatsApp messages, answering queries, and more.

## Features

### Core Capabilities
- **Voice Recognition**: Listens and responds to voice commands
- **Text-to-Speech**: Speaks responses using natural-sounding voices
- **Graphical Interface**: Tkinter-based UI with animated feedback

### Functional Features
- **Web Browsing**: Open websites (YouTube, Google, GitHub, LinkedIn)
- **Search**: Perform Google/Wikipedia searches
- **Media Control**: Play music from local files or YouTube
- **Communication**:
  - Send WhatsApp messages to saved contacts
  - Send emails using Gmail SMTP
- **Information**:
  - Get weather forecasts
  - Answer questions using Wolfram Alpha/Wikipedia
  - Tell jokes
- **Productivity**:
  - Set timed reminders
  - Check time/date
- **System Control**: Shutdown/restart computer (with confirmation)

- Instant web searches (Google, Wikipedia)
- Weather forecasts for any city worldwide
- Answers to complex questions using Wolfram Alpha
- Fun jokes to lighten your day

## 🛠️ Setup Guide

### Requirements
- Python 3.6+
- Decent microphone
- Internet connection

### Installation
1. Clone this repository
2. Install dependencies:

## Prerequisites

### Python Packages
Install required packages:
```bash
pip install speechrecognition pyttsx3 pygame requests wikipedia pyjokes wolframalpha pillow 
pip install -r requirements.txt
```

## API Keys and Configuration
**You need to configure these in the code:**
  - Wolfram Alpha API: Get from Wolfram Alpha
  - OpenWeatherMap API: Get from OpenWeather
  - Email Configuration: Gmail address and App Password
  - Contacts Dictionary: Add contacts for WhatsApp/email functionality
  - Music Directory: Set path to your local music folder

## Configuration
**Edit these in avatar.py before first run:**
```bash
# Essential API Keys (get free versions):
WOLFRAM_APP_ID = "your_key_here"  # From wolframalpha.com
OPENWEATHER_API_KEY = "your_key_here"  # From openweathermap.org

# Personalize these:
EMAIL_ADDRESS = "your.email@example.com"  # Gmail recommended
MUSIC_FOLDER = "C:/Users/You/Music"  # Where your songs live

# Add your frequent contacts:
CONTACTS = {
    "mom": {
        "phone": "+1234567890", 
        "email": "mom@example.com"
    },
    "boss": {
        "phone": "+1987654321",
        "email": "boss@company.com"
    }
}
```

## Troubleshooting
**1. Speech Recognition Issues:**
- Check microphone permissions
- Ensure internet connection (Google speech API requires internet)

**2. Email Not Sending:**
- Verify Gmail app password is correct
- Check less secure apps access or 2FA settings

**3. API Errors:**
- Confirm API keys are valid and properly inserted

**4. Music Playback:**
- Verify music files exist in specified directory
- Supported formats: .mp3, .wav, .ogg, .flac

## 🗣️ How to Use
**Just speak naturally after launching! Try these examples:**
- "Hellow AVATAR"
- "Send an Email"
- "Search, How has Narendra Modi Leadership change India Global image"
- "Send a WhatsApp Message"
- "Play Song"
- "Who is Mahendra Singh Dhoni"
- "Open Linkdin"
- "How is Weather today"
- "What is Current time"
- "Play my workout playlist"
- "Remind me to water plants in 2 hours"

## AVATAR Voice Assistant 🤖

![Screenshot 2025-06-07 221922](https://github.com/user-attachments/assets/7ec48be7-6b45-49c4-b766-dc5bf7238261)
*Live Demo of AVATAR in Action*

## Features ✨

| Feature | Description |
|---------|-------------|
| Voice Interaction | Natural language processing with animated feedback |
| Smart Knowledge | Wolfram Alpha and Wikipedia integration |
| Media Control | Play local music or YouTube videos |
| Communications | Send emails and WhatsApp messages |
