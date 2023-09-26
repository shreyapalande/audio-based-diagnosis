import speech_recognition as sr
# Initialize recognizer class                                       
r = sr.Recognizer()
# audio object                                                         
audio = sr.AudioFile("a3.wav")
#read audio object and transcribe
with audio as source:
    audio = r.record(source)                  
    result = r.recognize_google(audio)
    
print(result)