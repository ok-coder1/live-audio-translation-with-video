import speech_recognition
from translate import Translator

recognizer = speech_recognition.Recognizer()
microphone = speech_recognition.Microphone(device_index=0)
translator = Translator(to_lang="zh")


def main():
    # Recognize speech
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)
        speech = recognizer.recognize_groq(audio, language="en")
    print(f"You said: {speech}")

    # Translate speech
    translated_speech = translator.translate(speech)
    print(f"Translated to French: {translated_speech}")


if __name__ == "__main__":
    main()
