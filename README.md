# audio-based-diagnosis
Project to provide accurate medical diagnoses based on patient description.

The dataset contains patient symptoms which are classified into 24 classes. This data is cleaned, preprocessed and undergoes various NLP techniques to provide diagnosis. Three types of vectorizers namely CountVectorizer, TF-IDF vectorizer and Hashing Vectorizer is used and the reuslts are compared. The model uses a pipeline which consists of various Machine Learning algorithms such as Naive Bayes, SVM, KNN, Random Forest and much more. All these algorithms have similiar accuracy score. The Bagging Classifier, having the highest score, is used for building the final model used for prediction.

Speech_recognition library is used for conversion of audio files into text.

![image](https://github.com/shreyapalande/audio-based-diagnosis/assets/84615801/0617628c-ae5a-4303-b376-88115e6b2ee8)

![image](https://github.com/shreyapalande/audio-based-diagnosis/assets/84615801/4275338a-1672-4225-8cfd-c9442c3ab16f)

