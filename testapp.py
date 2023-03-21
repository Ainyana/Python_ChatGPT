from flask import Flask, redirect, url_for, render_template
import pyaudio
import wave
import openai
import speech_recognition as s
import gtts  
from playsound import playsound  
import time
import json
from json import JSONEncoder
import jsonpickle

class Thing(object):
    def __init__(self, name):
        self.name = name

app = Flask(__name__)

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 10
filename = "output.wav"

def json_serializer(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8')

    return obj
     


@app.route("/")
def page1():
    return "Hello"

@app.route("/members")
def members():
    return {"members":["Member1","Member2"]}
query = []
frames = []  # Initialize array to store frames


@app.route("/recording")
def recording():
    print("Recording for 10 seconds")
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    # frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')
    
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    # # Define OpenAI API key 
    # openai.api_key = "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"

    # # Set up the model and prompt
    model_engine = "text-davinci-003"
    print("model")
    print(model_engine)
    # prompt = "Once upon a time, in a land far, far away, there was a princess who..."
    sr = s.Recognizer()
    # print("Speak something")
    query = []
    with s.WavFile('output.wav') as m:
        audio = sr.listen(m)
        query = sr.recognize_google(audio)
        print('query now')
        print(query)

    # # Generate a response
    # completion = openai.Completion.create(
    #     engine=model_engine,
    #     prompt=query,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )
    # print("Open AI Response")
    # response = completion.choices[0].text
    # print(response)

    return (query)

@app.route("/chatgpt")
def chatgpt():
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Define OpenAI API key 
    openai.api_key = "Key"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    # prompt = "Once upon a time, in a land far, far away, there was a princess who..."
    sr = s.Recognizer()
    # print("Speak something")

    query = []
    with s.WavFile('output.wav') as m:
        audio = sr.listen(m)
        query = sr.recognize_google(audio)
        print(query)

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=query,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print("Open AI Response")
    response = completion.choices[0].text
    print(response)
    
    print("Question to ChatGPT")
    playsound("output.wav")  

    print("Chat GPT Answer")
    t1 = gtts.gTTS(response,lang='hi')
    t1.save("welcome.mp3")   
    playsound("welcome.mp3")  




    return (completion.choices[0].text)

 

if __name__ == "__main__":
    app.run(debug=True)