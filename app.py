import speech_recognition as sr
from gtts import gTTS
import os
from translate import Translator
import streamlit as st
import streamlit.components.v1 as components
import base64

def main():
    st.title("실시간 번역 챗봇")

    # 음성 파일 업로드 함수
    def get_audio():
        uploaded_file = st.file_uploader("음성 파일 업로드 (wav 형식)", type=["wav"])
        if uploaded_file is not None:
            audio_bytes = uploaded_file.read()
            st.audio(audio_bytes, format="audio/wav")
            return uploaded_file
        return None

    # 1. 음성 파일 업로드
    audio_file = get_audio()
    if audio_file is not None:
        user_input = recognize_audio(audio_file)
        if user_input:
            # 2. 한글에서 영어로 번역
            st.write(f"사용자: {user_input}")
            translator = Translator(from_lang="ko", to_lang="en")
            translation = translator.translate(user_input)
            st.write("번역된 영어: " + translation)
            speak2(translation)

    def recognize_audio(audio_file):
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            try:
                said = r.recognize_google(audio, language="ko-KR")
                st.write("당신이 말한 한국어는: " + said)
                return said
            except sr.UnknownValueError:
                st.write("음성을 인식할 수 없습니다. 다시 시도해 주세요.")
            except sr.RequestError as e:
                st.write("음성 인식 서비스 오류: {0}".format(e))
            except Exception as e:
                st.write("Exception: " + str(e))
                return None

    def speak2(text):
        tts = gTTS(text=text, lang='en')
        filename = 'voice.mp3'
        tts.save(filename)

        # 자동 재생을 위한 HTML 구성 요소 사용
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{base64_audio(filename)}" type="audio/mp3">
        </audio>
        """
        components.html(audio_html, height=100)
        
        # 파일 삭제 (선택사항)
        if st.button("음성 파일 삭제"):
            os.remove(filename)
            st.write("음성 파일이 삭제되었습니다.")

    def base64_audio(filename):
        with open(filename, "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read()).decode()
        return encoded_string

if __name__ == "__main__":
    main()
