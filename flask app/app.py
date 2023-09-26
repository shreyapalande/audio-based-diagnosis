from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import numpy as np
import os
import pickle
import speech_recognition as sr

app = Flask(__name__)

# Load the model from the pickle file
def load_model(modelfile):
	loaded_model = pickle.load(open(modelfile, 'rb'))
	return loaded_model

def get_key(val,my_dict):
	for key,value in my_dict.items():
		if val == value:
			return key

model = load_model('../model.pkl')
vec_model = load_model('../vectorizer.pkl')

prediction_labels = {'Emotional pain': 0, 'Hair falling out':1, 'Head hurts':2, 'Infected wound':3, 'Foot achne':4,
'Shoulder pain':5, 'Injury from sports':6, 'Skin issue':7, 'Stomach ache':8, 'Knee pain':9, 'Joint pain':10, 'Hard to breath':11,
'Head ache':12, 'Body feels weak':13, 'Feeling dizzy':14, 'Back pain':15, 'Open wound':16, 'Internal pain':17, 'Blurry vision':18,
'Acne':19, 'Neck pain':21, 'Cough':22, 'Ear achne':23, 'Feeling cold':24}

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/predict", methods = ["POST"])
def predict():

    input_text = [str(a) for a in request.form.values()]
    print((input_text[0]))
    vec_text =  vec_model.transform([input_text[0]]).toarray()
    pred = model.predict(vec_text)
    final_result = get_key(pred,prediction_labels)
    print(final_result)

    return render_template("index.html", prediction_text = "The predicted prompt is {}".format(final_result))

@app.route("/audio_predict", methods = ["POST"])
def audio_predict():

    if "file" not in request.files:
        return redirect(request.url)
    
    file = request.files["file"]
    print(type(file))
    if file: 
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile(file)
        with audioFile as source:
            data = recognizer.record(source)
        transcript = recognizer.recognize_google(data, key=None)
        # print(type(transcript))

        vec_text =  vec_model.transform([transcript]).toarray()
        pred = model.predict(vec_text)
        final_result = get_key(pred,prediction_labels)
        # print(final_result)

    return render_template("index.html", transcribed_text = transcript, prediction = "The predicted prompt is {}".format(final_result))

@app.route("/upload_audio", methods = ["POST"])
def upload_audio():
    print("hello audio")
    if 'audioFile' in request.files:
        print(request.files['audioFile'])
        audio_file = request.files['audioFile']

        # Process the audio file
        if audio_file:
            # Access the filename
            filename = audio_file.filename

            # Create the 'uploads' directory if it doesn't exist
            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            # Save the uploaded file to a specific directory
            upload_path = f'uploads/{filename}'
            audio_file.save(upload_path)

            # use speech recognition library to transcribe the audio
            transcript = transcribe_audio(upload_path)

            # try:
            #     # Add file validation here
            #     allowed_formats = ('.wav', '.aiff', '.aif', '.flac')
            #     if audio_file.filename.lower().endswith(allowed_formats):
            #         print('in')
            #         print("audio : ", audio_file.filename)
            #         recognizer = sr.Recognizer()
            #         audioFile = sr.AudioFile(audio_file)
            #         with audioFile as source:
            #             data = recognizer.record(source)
            #         transcript = recognizer.recognize_google(data, key=None)
            #         print("transcript : ", transcript)
            #         return jsonify({'transcript': transcript})
            #     else:
            #         return jsonify({'error': 'Invalid audio format. Supported formats: WAV, AIFF, AIFF-C, FLAC'})
            # except sr.UnknownValueError:
            #     print('err1')
            #     return jsonify({'error': 'Speech Recognition could not understand audio'})
            # except sr.RequestError:
            #     print('err2')
            #     return jsonify({'error': 'Could not request results; check your network connection'})
            # except Exception as e:
            #     print('err3 ', e )
            #     return jsonify({'error': str(e)})

            # vec_text =  vec_model.transform([transcript]).toarray()
            # pred = model.predict(vec_text)
            # final_result = get_key(pred,prediction_labels)
            # print(final_result)
        
        return jsonify({'response': "transcript"})
    
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path, format="wav") as source:
        audio_data = recognizer.record(source)

    # Transcribe the audio
    transcript = recognizer.recognize_google(audio_data, key=None)
    print("trans : ",transcript)

    return transcript
 


if __name__ == "__main__":
    app.run(debug=True, threaded=True)