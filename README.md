# voice-helper

**voice-helper** is an advanced, modern voice assistant for Windows, powered by Python, PyQt5, and several speech and system libraries. This project lets you control your PC with your voice: open apps, check the time and date, control volume, run quick searches, and monitor your system—all in a slick, responsive GUI.

---

## 🎙️ What Can It Do?

- **Voice Recognition:** Listen for and execute spoken commands (using your microphone).
- **Text-to-Speech:** Talks back to you using pyttsx3.
- **System Control:** Open Notepad, Calculator, Browser, File Explorer, or control system power (shutdown, restart, sleep).
- **Volume Control:** Instantly change volume or mute with your voice.
- **Time & Date:** Ask for the current time or date.
- **Web Search:** Just say "search ..." and it Googles for you.
- **System Monitoring:** See real-time CPU, memory, and disk usage, with beautiful progress bars.
- **Command History:** Review what you’ve said and what was executed.
- **Quick Actions:** One-click buttons for common tasks.
- **Modern GUI:** Sleek, dark-themed PyQt5 interface, stylish buttons, and easy-to-read info panels.
- **Offline/Online:** If offline, will keep trying to get back online for voice services.

---

## 🛠️ Requirements

- **Windows OS**
- **Python 3.7+**
- **Required Python libraries:**
    - PyQt5
    - PyQtWebEngine
    - psutil
    - speechrecognition
    - pyttsx3
    - pywin32
    - requests
    - Pillow

Install them all with:
```bash
pip install PyQt5 PyQtWebEngine psutil SpeechRecognition pyttsx3 pywin32 requests Pillow
```

---

## 🚀 Getting Started

1. **Clone this repo:**
    ```bash
    git clone https://github.com/Enockdeghost/voice-helper.git
    cd voice-helper
    ```

2. **Install the requirements:**  
   (See above for the pip command.)

3. **Run the assistant:**
    ```bash
    python main.py
    ```
   (Or whatever your main file is called.)

---

## 🖥️ How to Use

- **Start the app.**
- **Click the microphone button** ("🎤 Click to Speak")—it will turn red and start listening.
- **Say a command!** Try things like:
    - "Open notepad"
    - "Search weather in Nairobi"
    - "What time is it?"
    - "Shutdown"
    - "Volume up"
    - "Open browser"
- **Check the history** below to see what you said and what action was taken.
- **Use quick-action buttons** for instant access to common tools.

If you get no response (offline), the app will keep trying to reconnect for voice recognition.

---

## 🧩 Project Structure

```
voice-helper/
└── main.py           # Main application file (all logic, GUI, and features)
└── README.md
```

---

## 💡 Customization

- **Add new commands:** Edit the `execute_command` function in the code.
- **Change voice:** You can customize the voice and speed in the pyttsx3 setup.
- **UI Styling:** All CSS-like styles are inline in the code, tweak as you like.

---

## ❓ Troubleshooting

- If you see ImportError, just install the missing library using `pip install <library>`.
- Make sure your microphone is connected and working.
- On some Windows systems, you may need to run as administrator for full access.

---


**Author:** [Enockdeghost](https://github.com/Enockdeghost)

---

> Built for productivity, accessibility, and fun.  
> If you have ideas or run into bugs, feel free to open an issue or pull request!
