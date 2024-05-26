import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import speech_recognition as sr
from gtts import gTTS
import os
from translate import Translator
import base64
import numpy as np

class SpeechRecognizer(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_data = []

    def recv(self, frame):
        audio = frame.to_ndarray().flatten()
        self.audio_data.append(audio)
        return frame

    def get_text(self):
        if not self.audio_data:
            return None
        audio_data = np.concatenate(self.audio_data, axis=0).astype(np.int16)
        audio_data = sr.AudioData(audio_data.tobytes(), frame_rate=16000, sample_width=2)
        try:
            text = self.recognizer.recognize_google(audio_data, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            return f"음성 인식 서비스 오류: {e}"
        except Exception as e:
            return f"Exception: {e}"

def main():
    st.title("실시간 번역 챗봇")

    # WebRTC 설정
    ctx = webrtc_streamer(
        key="speech-recognizer",
        mode=WebRtcMode.SENDONLY,
        audio_processor_factory=SpeechRecognizer,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    # 음성 입력 및 번역 처리
    if st.button("음성 인식 시작"):
        if ctx.audio_processor:
            text = ctx.audio_processor.get_text()
            if text:
                st.write("당신이 말한 한국어는: " + text)
                # 한글에서 영어로 번역
                translator = Translator(from_lang="ko", to_lang="en")
                translation = translator.translate(text)
                st.write("번역된 영어: " + translation)
                speak2(translation)

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
        st.markdown(audio_html, unsafe_allow_html=True)

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
