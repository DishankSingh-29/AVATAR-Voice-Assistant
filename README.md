# AVATAR Voice Assistant 🤖🎙️
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)


**AVATAR** is an intelligent voice assistant designed to make your digital life easier. With natural language processing and a friendly interface, it can perform various tasks from web searches to system control—all through voice commands.

# 🚀 Tech Stack

## Core Technologies

### Voice Processing
| Library               | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `speech_recognition`  | Converts microphone input to text using Google's speech recognition API |
| `pyttsx3`             | Offline text-to-speech synthesis (cross-platform)                       |
| `pygame`              | Audio playback for local music files                                    |

### Web & API Integrations
| Library               | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `webbrowser`          | Opens web URLs (YouTube, Google, etc.)                                 |
| `requests` + `json`   | Fetches data from OpenWeatherMap API                                   |
| `wolframalpha`        | Answers computational/factual queries                                  |
| `wikipedia`           | Retrieves knowledge summaries                                         |
| `smtplib` + `email`   | Sends emails via Gmail SMTP                                            |

### GUI Development
| Library               | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `tkinter`             | Creates desktop interface (windows, buttons, labels)                   |
| `Pillow` (PIL)        | Handles image/GIF manipulation for animations                         |
| `scrolledtext`        | Displays scrollable conversation history                              |

## Key Features

✨ **Voice Control**  
- Natural language commands for music, web search, reminders, emails  
- Offline text-to-speech capability  

🌐 **Smart Integrations**  
- Wolfram Alpha for calculations  
- Wikipedia for general knowledge  
- OpenWeatherMap for weather data  

💻 **Desktop Interface**  
- Interactive GUI with real-time feedback  
- Visual animations for listening/speaking states  

## API Services

| Service               | Purpose                                | Key Required  |
|-----------------------|----------------------------------------|---------------|
| OpenWeatherMap        | Real-time weather data                 | `OPENWEATHER_API_KEY` |
| Wolfram Alpha         | Computational knowledge engine         | `WOLFRAM_APP_ID`     |
| Gmail SMTP            | Email sending functionality            | `EMAIL_PASSWORD`     |

## Development Dependencies

```bash
pip install speechrecognition pyttsx3 pygame requests wolframalpha wikipedia pyjokes Pillow
```

## ✨ Features

- **Voice Interaction**: Speak naturally and get responses
- **Multi-functional Capabilities**:
  - 🌐 Web browsing (Google, YouTube, GitHub, etc.)
  - 🎵 Music playback (local files & YouTube)
  - 📅 Date/time information
  - 📧 Email composition
  - 📱 WhatsApp messaging (via web interface)
  - ⏰ Reminders
  - 📚 Wikipedia/Wolfram Alpha knowledge queries
  - ☀️ Weather forecasts
  - 😄 Jokes and entertainment
- **Beautiful GUI** with animated feedback
- **Cross-platform** (Windows/macOS/Linux compatible)

## 🛠️ Installation

1. **Prerequisites**:
   - Python 3.8+
   - Microphone
   - Internet connection

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

## API Keys and Configuration
**You need to configure these in the code:**
  - Wolfram Alpha API: Get from Wolfram Alpha
  - OpenWeatherMap API: Get from OpenWeather
  - Email Configuration: Gmail address and App Password
  - Contacts Dictionary: Add contacts for WhatsApp/email functionality
  - Music Directory: Set path to your local music folder


## 📁 Project Structure
```bash
AVATAR-Voice-Assistant/
├── avatar.py            # Main application
├── README.md            # This file
└── assets/              # GUI resources
    ├── listening.gif    # Animation
    └── speaking.gif     # Animation
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

## AVATAR Interface 🤖
<div align="center">
  <img src="https://github.com/user-attachments/assets/7ec48be7-6b45-49c4-b766-dc5bf7238261" width="800" height="450" />
</div>


## AVATAR Demo Video
[Click Here to see the Demo Video](https://www.linkedin.com/posts/dishanksingh29_ai-python-voiceassistant-activity-7337473715200282624-ZCkp?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEnD5boBuENKCr-Ncd2lCmqVZUdCFvBv1Fs)

## 📜 License
- AVATAR is licensed under the MIT License.

## 🤖 Contribution
- Contributions are welcome! Feel free to submit issues or pull requests.
