from quart import Quart, request, websocket, render_template, redirect
import speech_recognition
from translate import Translator
import asyncio
from pydub import AudioSegment

app = Quart(__name__)
recognizer = speech_recognition.Recognizer()


translator = None
translated_speech = None
og_language = translated_language = None


@app.route("/recognize_speech", methods=["POST"])
async def recognize_speech():
    global translator, og_language, translated_language
    form = await request.form
    og_language = form.get("og_language")
    translated_language = form.get("translated_language")
    translator = Translator(to_lang=translated_language)

    return redirect("/")


async def translate():
    global translated_speech

    f = AudioSegment.from_file("audio_recording.webm", format="webm")
    f.export("output.wav", format="wav")

    source = speech_recognition.AudioData.from_file("output.wav")
    # audio = recognizer.listen(source)
    speech = recognizer.recognize_groq(source, language=og_language)
    translated_speech = translator.translate(speech)

    # source.close()
    return translated_speech


# @app.websocket("/ws")
async def wsx():
    global translator, og_language, translated_language
    # try:
    with open("audio_that_record.webm", "wb") as f:
        while True:
            data = await websocket.receive()
            if isinstance(data, bytes):
                print(f"we got these many bytes: {len(data)}")
                f.write(data)
                await websocket.send(b"HELLO")
                #await translate()
            else:
                print(f"no bytes why: {data}")

    # except asyncio.CancelledError:
    #     print("bye")
    # except Exception as e:
    #     print(f"error moment: {e}")


@app.websocket("/ws")
async def ws():
    global translator, og_language, translated_language

    while True:
        data = await websocket.receive()
        if isinstance(data, bytes):
            print(f"Received complete recording: {len(data)} bytes")
            with open("audio_recording.webm", "wb") as f:
                f.write(data)
            await websocket.send(await translate())


@app.get("/")
async def index():
    return await render_template('index.html', translated_speech="")


if __name__ == "__main__":
    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5000"]
    config.certfile = "cert.pem"
    config.keyfile = "key.pem"

    asyncio.run(hypercorn.asyncio.serve(app, config))
