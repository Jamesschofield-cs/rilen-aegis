from datetime import datetime
import subprocess
import webbrowser
import requests
import speech_recognition as sr
import aegis

recognizer = sr.Recognizer()

def speak(text):
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Add-Type -AssemblyName System.Speech; "
            "$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            "$text = [Console]::In.ReadToEnd(); "
            "$voice.Speak($text)"
        ],
        input=text,
        text=True
    )

name = input("What is your name? ")
print("Hello, " + name + "!")

assistant_name = "RILEN"

intro = "RILEN online. Hello " + name + ". How can I help?"
print(intro)
speak(intro)

while True:
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
        print("Contacting AEGIS...")
        result = aegis.security_check()
        print(result)
        speak(result)

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
        city = command.replace("weather in ", "")
        response = requests.get("https://wttr.in/" + city + "?format=3")
        message = response.text
        print(message)
        speak(message)

    elif command == "exit":
        message = "Goodbye, " + name + "!"
        print(message)
        speak(message)
        break

    else:
        print("Sorry, I don't understand that command.")
