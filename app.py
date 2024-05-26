import speech_recognition as sr
from gtts import gTTS
import os
from translate import Translator
import streamlit as st

def main():
    st.title("실시간 번역 챗봇")

    def speak2(text):
        tts = gTTS(text=text, lang='en')
        filename = 'voice.mp3'
        tts.save(filename)
        st.audio(filename, format="audio/mp3")
        os.remove(filename)

    # 음성 입력 함수
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("듣는 중... 5초 동안 한국어를 입력하세요.")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            said = ""
            try:
                said = r.recognize_google(audio, language="ko-KR")
                # st.write("당신이 말한 한국어는: ", said)
                return said
            except sr.UnknownValueError:
                st.write("음성을 인식할 수 없습니다. 다시 시도해 주세요.")
            except sr.RequestError as e:
                st.write("음성 인식 서비스 오류: {0}".format(e))
            except Exception as e:
                st.write("Exception: " + str(e))
    
    # 1. 음성입력
    if st.button("음성 입력"):
        user_input = get_audio()
        if user_input:
            # 2. 한글에서 영어로 번역
            st.write(f"사용자: {user_input}")
            translator = Translator(from_lang="ko", to_lang="en")
            translation = translator.translate(user_input)
            st.write("번역된 영어: ", translation)
            speak2(translation)

if __name__ == "__main__":
    main()
