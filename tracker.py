import sys
import os
import subprocess
import psutil
import speech_recognition as sr
import pyttsx3
import webbrowser
import json
import requests
import datetime
import threading
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import win32api
import win32con
import win32gui
import win32process

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)

# Voice recognition setup
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Global variables
listening = False
assistant_active = True

def speak(text):
    """Text to speech function"""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_for_command():
    """Listen for voice commands"""
    global listening
    if not listening:
        return None
    
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        with microphone as source:
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
        
        command = recognizer.recognize_google(audio).lower()
        return command
    except:
        return None

def execute_command(command):
    """Execute voice commands"""
    if not command:
        return "No command received"
    
    # System commands
    if "shutdown" in command or "turn off" in command:
        speak("Shutting down the system")
        os.system("shutdown /s /t 1")
        return "Shutting down system"
    
    elif "restart" in command or "reboot" in command:
        speak("Restarting the system")
        os.system("shutdown /r /t 1")
        return "Restarting system"
    
    elif "sleep" in command:
        speak("Putting system to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "System going to sleep"
    
    # Application commands
    elif "open notepad" in command:
        subprocess.Popen("notepad.exe")
        speak("Opening Notepad")
        return "Opened Notepad"
    
    elif "open calculator" in command:
        subprocess.Popen("calc.exe")
        speak("Opening Calculator")
        return "Opened Calculator"
    
    elif "open browser" in command or "open chrome" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening browser")
        return "Opened browser"
    
    elif "open file explorer" in command:
        subprocess.Popen("explorer.exe")
        speak("Opening File Explorer")
        return "Opened File Explorer"
    
    # Volume control
    elif "volume up" in command:
        for i in range(5):
            win32api.keybd_event(0xAF, 0, 0, 0)  # Volume up
            win32api.keybd_event(0xAF, 0, win32con.KEYEVENTF_KEYUP, 0)
        speak("Volume increased")
        return "Volume increased"
    
    elif "volume down" in command:
        for i in range(5):
            win32api.keybd_event(0xAE, 0, 0, 0)  # Volume down
            win32api.keybd_event(0xAE, 0, win32con.KEYEVENTF_KEYUP, 0)
        speak("Volume decreased")
        return "Volume decreased"
    
    elif "mute" in command:
        win32api.keybd_event(0xAD, 0, 0, 0)  # Mute
        win32api.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        speak("Audio muted")
        return "Audio muted"
    
    # Time and date
    elif "time" in command or "what time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        return f"Current time: {current_time}"
    
    elif "date" in command or "what date" in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {current_date}")
        return f"Today's date: {current_date}"
    
    # Search commands
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Searching for {search_query}")
            return f"Searching for: {search_query}"

def get_system_info():
    """Get system information"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu': cpu_usage,
        'memory': memory.percent,
        'disk': disk.percent,
        'memory_total': round(memory.total / (1024**3), 2),
        'memory_used': round(memory.used / (1024**3), 2),
        'disk_total': round(disk.total / (1024**3), 2),
        'disk_used': round(disk.used / (1024**3), 2)
    }

class VoiceAssistantWorker(QThread):
    """Worker thread for voice recognition"""
    command_received = pyqtSignal(str)
    status_update = pyqtSignal(str)
    
    def run(self):
        global listening, assistant_active
        while assistant_active:
            if listening:
                self.status_update.emit("Listening...")
                command = listen_for_command()
                if command:
                    self.command_received.emit(command)
                    result = execute_command(command)
                    self.status_update.emit(f"Executed: {result}")
                else:
                    self.status_update.emit("Ready - Click to speak")
            time.sleep(0.1)

class SystemMonitorWorker(QThread):
    """Worker thread for system monitoring"""
    system_update = pyqtSignal(dict)
    
    def run(self):
        while assistant_active:
            system_info = get_system_info()
            self.system_update.emit(system_info)
            time.sleep(2)

# Create main application
app = QApplication(sys.argv)

# Main window
main_window = QMainWindow()
main_window.setWindowTitle("EnoVoice assistant")
main_window.setGeometry(100, 100, 1200, 800)
main_window.setStyleSheet("""
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                   stop:0 #1a1a2e, stop:1 #16213e);
    }
""")

# Central widget
central_widget = QWidget()
main_window.setCentralWidget(central_widget)

# Main layout
main_layout = QVBoxLayout(central_widget)
main_layout.setSpacing(20)
main_layout.setContentsMargins(20, 20, 20, 20)

# Header section
header_layout = QHBoxLayout()

# Logo and title
title_layout = QVBoxLayout()
title_label = QLabel("eno-assistant")
title_label.setStyleSheet("""
    QLabel {
        font-size: 36px;
        font-weight: bold;
        color: #00d4ff;
        text-align: center;
    }
""")
subtitle_label = QLabel("Advanced Voice Assistant")
subtitle_label.setStyleSheet("""
    QLabel {
        font-size: 16px;
        color: #ffffff;
        text-align: center;
    }
""")
title_layout.addWidget(title_label)
title_layout.addWidget(subtitle_label)

# Status indicator
status_indicator = QLabel("●")
status_indicator.setStyleSheet("""
    QLabel {
        font-size: 48px;
        color: #ff4757;
    }
""")

header_layout.addLayout(title_layout)
header_layout.addStretch()
header_layout.addWidget(status_indicator)

main_layout.addLayout(header_layout)

# Control panel
control_frame = QFrame()
control_frame.setStyleSheet("""
    QFrame {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.3);
    }
""")
control_layout = QHBoxLayout(control_frame)

# Voice control button
voice_button = QPushButton("🎤 Click to Speak")
voice_button.setStyleSheet("""
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #00d4ff, stop:1 #0099cc);
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #00b8e6, stop:1 #0088bb);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                   stop:0 #009acc, stop:1 #0077aa);
    }
""")

# Status display
status_display = QLabel("Ready - Click to speak")
status_display.setStyleSheet("""
    QLabel {
        font-size: 16px;
        color: #ffffff;
        padding: 15px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
""")

control_layout.addWidget(voice_button)
control_layout.addWidget(status_display)

main_layout.addWidget(control_frame)

# System information panel
system_frame = QFrame()
system_frame.setStyleSheet("""
    QFrame {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.3);
    }
""")
system_layout = QGridLayout(system_frame)

# System info labels
system_title = QLabel("System Monitor")
system_title.setStyleSheet("""
    QLabel {
        font-size: 20px;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 10px;
    }
""")

cpu_label = QLabel("CPU Usage: 0%")
memory_label = QLabel("Memory Usage: 0%")
disk_label = QLabel("Disk Usage: 0%")

for label in [cpu_label, memory_label, disk_label]:
    label.setStyleSheet("""
        QLabel {
            font-size: 14px;
            color: #ffffff;
            padding: 5px;
        }
    """)

# Progress bars
cpu_bar = QProgressBar()
memory_bar = QProgressBar()
disk_bar = QProgressBar()

for bar in [cpu_bar, memory_bar, disk_bar]:
    bar.setStyleSheet("""
        QProgressBar {
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
            color: white;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #00d4ff, stop:1 #0099cc);
            border-radius: 3px;
        }
    """)

system_layout.addWidget(system_title, 0, 0, 1, 2)
system_layout.addWidget(cpu_label, 1, 0)
system_layout.addWidget(cpu_bar, 1, 1)
system_layout.addWidget(memory_label, 2, 0)
system_layout.addWidget(memory_bar, 2, 1)
system_layout.addWidget(disk_label, 3, 0)
system_layout.addWidget(disk_bar, 3, 1)

main_layout.addWidget(system_frame)

# Command history
history_frame = QFrame()
history_frame.setStyleSheet("""
    QFrame {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.3);
    }
""")
history_layout = QVBoxLayout(history_frame)

history_title = QLabel("Command History")
history_title.setStyleSheet("""
    QLabel {
        font-size: 20px;
        font-weight: bold;
        color: #00d4ff;
        margin-bottom: 10px;
    }
""")

command_history = QTextEdit()
command_history.setStyleSheet("""
    QTextEdit {
        background: rgba(0, 0, 0, 0.3);
        color: #ffffff;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 5px;
        font-family: 'Consolas', monospace;
        font-size: 12px;
    }
""")
command_history.setMaximumHeight(150)

history_layout.addWidget(history_title)
history_layout.addWidget(command_history)

main_layout.addWidget(history_frame)

# Quick actions
actions_frame = QFrame()
actions_frame.setStyleSheet("""
    QFrame {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px solid rgba(0, 212, 255, 0.3);
    }
""")
actions_layout = QHBoxLayout(actions_frame)

# Quick action buttons
quick_buttons = [
    ("🔧 System Info", lambda: show_system_info()),
    ("🌐 Open Browser", lambda: webbrowser.open("https://www.google.com")),
    ("📁 File Explorer", lambda: subprocess.Popen("explorer.exe")),
    ("🧮 Calculator", lambda: subprocess.Popen("calc.exe")),
    ("📝 Notepad", lambda: subprocess.Popen("notepad.exe"))
]

for text, func in quick_buttons:
    btn = QPushButton(text)
    btn.setStyleSheet("""
        QPushButton {
            background: rgba(0, 212, 255, 0.2);
            color: white;
            font-size: 12px;
            border: 1px solid rgba(0, 212, 255, 0.5);
            border-radius: 8px;
            padding: 10px;
        }
        QPushButton:hover {
            background: rgba(0, 212, 255, 0.4);
        }
    """)
    btn.clicked.connect(func)
    actions_layout.addWidget(btn)

main_layout.addWidget(actions_frame)

def show_system_info():
    """Show detailed system information"""
    info = get_system_info()
    msg = QMessageBox()
    msg.setWindowTitle("System Information")
    msg.setText(f"""
    CPU Usage: {info['cpu']}%
    Memory: {info['memory_used']}GB / {info['memory_total']}GB ({info['memory']}%)
    Disk: {info['disk_used']}GB / {info['disk_total']}GB ({info['disk']}%)
    """)
    msg.setStyleSheet("""
        QMessageBox {
            background: #1a1a2e;
            color: white;
        }
        QPushButton {
            background: #00d4ff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
    """)
    msg.exec_()

def toggle_listening():
    """Toggle voice listening"""
    global listening
    listening = not listening
    if listening:
        voice_button.setText("🔴 Listening...")
        voice_button.setStyleSheet(voice_button.styleSheet().replace("#00d4ff", "#ff4757").replace("#0099cc", "#ff3742"))
        status_indicator.setStyleSheet("QLabel { font-size: 48px; color: #2ed573; }")
    else:
        voice_button.setText("🎤 Click to Speak")
        voice_button.setStyleSheet(voice_button.styleSheet().replace("#ff4757", "#00d4ff").replace("#ff3742", "#0099cc"))
        status_indicator.setStyleSheet("QLabel { font-size: 48px; color: #ff4757; }")

def update_status(status):
    """Update status display"""
    status_display.setText(status)

def update_system_info(info):
    """Update system information display"""
    cpu_label.setText(f"CPU Usage: {info['cpu']}%")
    memory_label.setText(f"Memory: {info['memory_used']}GB / {info['memory_total']}GB")
    disk_label.setText(f"Disk: {info['disk_used']}GB / {info['disk_total']}GB")
    
    cpu_bar.setValue(int(info['cpu']))
    memory_bar.setValue(int(info['memory']))
    disk_bar.setValue(int(info['disk']))

def add_to_history(command):
    """Add command to history"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    command_history.append(f"[{timestamp}] {command}")

# Connect signals
voice_button.clicked.connect(toggle_listening)

# Create worker threads
voice_worker = VoiceAssistantWorker()
voice_worker.command_received.connect(add_to_history)
voice_worker.status_update.connect(update_status)

system_worker = SystemMonitorWorker()
system_worker.system_update.connect(update_system_info)

# Start worker threads
voice_worker.start()
system_worker.start()

# Show window and run app
main_window.show()

# Initial system info update
initial_info = get_system_info()
update_system_info(initial_info)

# Welcome message
speak("eno-assistant voice assistant initialized and ready for commands")
add_to_history("System initialized - eno-assistant ready")

sys.exit(app.exec_())