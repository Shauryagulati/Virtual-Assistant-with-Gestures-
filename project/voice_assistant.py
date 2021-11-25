import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

sa_model = load_model("saved_models/sentiment_analysis/model.h5")

df = pd.read_csv("Tweets.csv")

tweet_df = df[['text', 'airline_sentiment']]
tweet_df = tweet_df[tweet_df['airline_sentiment'] != 'neutral']
sentiment_label = tweet_df.airline_sentiment.factorize()

tweet = tweet_df.text.values
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(tweet)


def predict_sentiment_sa(text):
    tw = tokenizer.texts_to_sequences([text])
    tw = pad_sequences(tw,maxlen=200)
    prediction_sa = int(sa_model.predict(tw).round().item())
    print("Predicted label: ", sentiment_label[1][prediction_sa])
    return sentiment_label[1][prediction_sa]


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    time2 = int(datetime.datetime.now().hour)
    if 0 <= time2 < 12:
        speak("Good Morning!")
    elif 12 <= time2 < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("Hi, i am your assistant. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    mic = sr.Microphone()#device_index=2)
    with mic as source:
        print("I'm listening to what you're saying...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query1 = r.recognize_google(audio, language='en-in')
        print(f"You said: {query1}\n")
    except Exception as e:
        print("Would you mind repeating that")
        speak("Would you mind repeating that")
        return "None"
    return query1


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia ...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=1)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'check' in query:
            test_sentence1 = takeCommand().lower()
            res = predict_sentiment_sa(test_sentence1)
            if(res == 'positive'):
                speak("Let me surprise you with something fun, say surprise me")
                print("Let me surprise you with something fun, say surprise me")
            else:
                speak("try painting on web canvas")
                print("try painting on web canvas")


        elif 'youtube' in query:
            webbrowser.open("youtube.com")
            speak("OPENING. ENJOY YOUR FAVOURITE VIDEOS")
            print("OPENING. ENJOY YOUR FAVOURITE VIDEOS")

        elif 'google' in query:
            webbrowser.open("google.com")
            speak("OPENING. EXPLORE AND SEARCH FOR ANYTHING. THE SKY IS THE LIMIT")
            print("OPENING. EXPLORE AND SEARCH FOR ANYTHING. THE SKY IS THE LIMIT")

        elif 'amazon' in query:
            webbrowser.open("amazon.in")
            speak("OPENING. SHOP FOR ANYTHING you like")
            print("OPENING. SHOP FOR ANYTHING you like")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            print(f"The current time is {strTime}")
            speak(f"The current time is {strTime}")

        elif 'thank you' in query:
            speak("My pleasure")
            print("My pleasure")

        elif 'surprise' in query:
            speak("OPENING NOW")
            webbrowser.open("https://www.youtube.com/results?search_query=kapil+sharma+show")

        elif 'fun' in query:
            speak("Opening")
            webbrowser.open("https://www.youtube.com/results?search_query=comedy+video+movie")

        elif 'bye' in query:
            speak(" Bye. See you soon")
            print(" Bye. See you soon")
            quit()