import speech_recognition as sr
from gtts import gTTS
import os
import playsound
from translate import Translator
import streamlit as st

def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def speak2(text):
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename, block=False)
    os.remove(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("한국어를 말하세요.")
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="ko-KR")
            st.write("당신이 말한 한국어는: ", said)
        except Exception as e:
            st.write("Exception: " + str(e))

    return said

#######################################################################################################################

st.title("실시간 한국어 -> 영어 번역 서비스")
# speak("안녕하세요, 2초 후에 한국어로 말을 하면, 영어로 번역됩니다.")

# 1. 음성입력
if st.button("음성 입력"):
    text = get_audio()
    if text:
        # 2. 한글에서 영어로 번역
        translator = Translator(from_lang="ko", to_lang="en")
        translation = translator.translate(text)
        st.write("번역된 영어: ", translation)

        # 3. 음성 출력
        speak2(translation)
