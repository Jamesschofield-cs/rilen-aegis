from datetime import datetime
import subprocess
import webbrowser
import requests
import speech_recognition as sr
import aegis
import sys
from pathlib import Path

recognizer = sr.Recognizer()
aegis_process = None

def speak(text):
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "[Console]::InputEncoding = [System.Text.Encoding]::UTF8; "
            "Add-Type -AssemblyName System.Speech; "
            "$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$text = [Console]::In.ReadToEnd(); "
            "$voice.Speak($text)"
        ],
        input=text,
        text=True,
        encoding="utf-8"
    )

name = input("What is your name? ")
print("Hello, " + name + "!")

assistant_name = "RILEN"

intro = "RILEN online. Hello " + name + ". How can I help?"
print(intro)
speak(intro)

while True:
    if aegis_process is not None and aegis_process.poll() is not None:
        output, _ = aegis_process.communicate()
        return_code = aegis_process.returncode
        aegis_process = None

        if return_code == 0 and output.strip():
            print(output)
            report = output.strip().splitlines()[-1]
            speak(report)
        else:
            print(output)
            speak("AEGIS could not complete the security check.")
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)

        wake_words = ["rilen ", "rylan ", "riley ", "raining "]
        wake_word_found = False

        for wake_word in wake_words:
            if command.startswith(wake_word):
                command = command.replace(wake_word, "", 1)
                wake_word_found = True
                break

        if not wake_word_found:
            print("Waiting for the word RILEN...")
            continue
    except sr.WaitTimeoutError:
            continue
    except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            continue
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        continue

    if command == "say hello":
        message = "Hello again, " + name + "!"
        print(message)
        speak(message)

    elif command in ("help", "what can you do"):
        message = (
            "RILEN commands — start each one with 'RILEN':\n"
            "- say hello\n"
            "- who are you\n"
            "- help / what can you do\n"
            "- ask aegis to run a security check\n"
            "- stop aegis / cancel security check\n"
            "- show security log\n"
            "- time\n"
            "- date\n"
            "- open notepad\n"
            "- open google\n"
            "- search google for [your search]\n"
            "- open youtube\n"
            "- weather in [city]\n"
            "- exit"
        )
        print(message)
        speak(
            "Start each command with RILEN. "
            "I can tell you the time and date, open Notepad, Google or YouTube, "
            "search Google, check the weather, and ask AEGIS to check security "
            "or show your security log. "
            "The full command list is displayed in the terminal."
        )

    elif command == "who are you":
        message = "I am RILEN. Reasoning Intelligence for Learning, Execution and Navigation."
        print(message)
        speak(message)

    elif command in [
        "ask aegis to run a security check",
        "ask ages to run a security check",
        "ask aegis to run a security",
        "ask ages to run a security"
]:
        if aegis_process is not None and aegis_process.poll() is None:
            message = "AEGIS is already running a security check."
        else:
            aegis_process = subprocess.Popen(
                [sys.executable, str(Path(__file__).with_name("run_aegis.py"))],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
            )
            message = "AEGIS security check started."

        print(message)
        speak(message)

    elif command in ("stop aegis", "stop ages", "cancel security check"):
        if aegis_process is None or aegis_process.poll() is not None:
            message = "AEGIS is not running a security check."
        else:
            stopped = subprocess.run(
                ["taskkill", "/PID", str(aegis_process.pid), "/T", "/F"],
                capture_output=True,
                text=True,
            )
            if stopped.returncode == 0:
                aegis_process.communicate()
                aegis_process = None
                message = "AEGIS security check stopped."
            else:
                message = "I could not stop AEGIS. Check the terminal."

        print(message)
        speak(message)

    elif command == "show security log":
        result = aegis.view_audit_log()
        print(result)
        speak("The audit log result is displayed in the terminal.")
        
    elif command == "time":
        current_time = datetime.now()
        message = "The time is " + current_time.strftime("%H:%M")
        print(message)
        speak(message)

    elif command == "date":
        current_date = datetime.now()
        message = "Today's date is " + current_date.strftime("%d/%m/%Y")
        print(message)
        speak(message)

    elif command == "open notepad":
        subprocess.Popen(["notepad.exe"])
        print("Opening Notepad...")

    elif command == "open google":
        webbrowser.open("https://www.google.com")
        print("Opening Google...")
        
    elif command.startswith("search google for "):
        search = command.replace("search google for ", "")
        webbrowser.open("https://www.google.com/search?q=" + search)
        print("Searching Google for " + search + "...")

    elif command == "open youtube":
        webbrowser.open("https://www.youtube.com")
        print("Opening YouTube...")

    elif command.startswith("weather in "):
        city = command.replace("weather in ", "", 1).strip()

        if not city:
            message = "Please name a city. For example, weather in Leeds."
        else:
            try:
                response = requests.get(
                    "https://wttr.in/" + city,
                    params={"format": "3"},
                    timeout=10
                )
                response.raise_for_status()
                message = response.text.strip()
                if not message:
                    message = "The weather service returned no information. Please try again."
            except requests.exceptions.RequestException:
                message = "I couldn't get the weather right now. Please try again later."

        print(message)
        speak(message)

    elif command == "exit":
        if aegis_process is not None:
            if aegis_process.poll() is None:
                stopped = subprocess.run(
                    ["taskkill", "/PID", str(aegis_process.pid), "/T", "/F"],
                    capture_output=True,
                    text=True,
                )
                if stopped.returncode != 0:
                    print("Could not stop AEGIS; RILEN is staying open.")
                    continue

            aegis_process.communicate()
            aegis_process = None
        message = "Goodbye, " + name + "!"
        print(message)
        speak(message)
        break

    else:
        print("Sorry, I don't understand that command.")
