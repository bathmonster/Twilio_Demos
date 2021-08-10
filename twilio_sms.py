import warnings
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import os
import playsound
from twilio.rest import Client


import account_info

warnings.filterwarnings("ignore")

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def talk(audio):
    engine.say(audio)
    engine.runAndWait()

def rec_audio():
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recog.listen(source)

    data = " "

    try:
        data = recog.recognize_google(audio)
        print("you said: " + data)

    except sr.UnknownValueError:
        print("Computer was not able to understand you")

    except sr.RequestError as ex:
        print("Request error from Google Speech Recognition" + ex)

    return data

def response(text):
    print(text)

    tts = gTTS(text=text, lang="en")

    audio = "Audio.mp3"
    tts.save(audio)

    playsound.playsound(audio)

    os.remove(audio)

def call(text):
    action_call = "computer"

    text = text.lower()

    if action_call in text:
        return True

    return False

while True:

    try:

        # Record the audio
        text = rec_audio()
        speak = ""  # Empty speak string

        # Checking for the wake word/phrase
        if call(text):

            # Check for greetings by the user
            speak = speak + say_hello(text)

           # Check to see if the user said 'send message'
        elif "send message" in text:
                # account_sid = ""  # Enter your Twilio SID here
                # auth_token = ""  # Enter your Twilio Token here
                client = Client(account_info.twilio_account_sid, account_info.twilio_auth_token)

                # talk("to what number")
                # account_info.target_number = str(rec_audio()) # trying to get the target.number as a var
                #print(" Sending message to " + account_info.target_number)  # to confirm that number was obtained
                talk("What should i send")
                message = client.messages.create(
                    body=rec_audio(),
                    from_=account_info.twilio_number,
                    to=account_info.target_number,
                    status_callback='https://a30e2e06a0af.ngrok.io/twilio'

                )
                print("SMS was sent with the following information" + message.body + "To " + account_info.target_number)
                speak = speak + "Message sent successfully"


            # # Check to see if the user said 'don't listen' or 'stop listening' or 'do not listen'
            # elif "don't listen" in text or "stop listening" in text or "do not listen" in text:
            #     talk("for how many seconds do you want me to sleep")
            #     a = int(rec_audio())
            #     time.sleep(a)
            #     speak = speak + str(a) + " seconds completed. Now you can ask me anything"

            # Check to see if the user said 'exit' or 'quit'

        if "exit" in text or "quit" in text or "stop" in text:
                exit()

        # Computer response
        response(speak)

    except:
       talk(speak)