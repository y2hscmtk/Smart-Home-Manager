# AI Speaker의 역할을 하는 부분

import time
import os  # 프로그램 종료 방지용
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound


def listen(recognizer, audio):  # 음성 인식 (듣기 )
    try:
        text = recognizer.recognize_google(audio, language='ko')
        print("[User] " + text)
        answer(text)
    except sr.UnknownValueError:
        speak("잘 듣지 못했어요")
        print("인식 실패")  # 음성 인식이 실패한 경우
    except sr.RequestError as e:  # 네트워크 등의 이유로 연결이 제대로 안됐을경우 API Key 오류, 네트워크 단절 등
        speak("네트워크 상태를 확인해주세요")
        print("요청 실패 : {0}".format(e))  # 에러형식 출력
    pass


def answer(input_text):  # 어떤 대답을 할것인지 정의
    answer_text = ''  # 컴퓨터가 대답할 말 key값이 들어갔다면 출력되도록
    if '안녕' in input_text:
        answer_text = "안녕하세요? 반갑습니다."
    elif '날씨' in input_text:
        answer_text = "오늘 서울 기온은 20도입니다. 맑은 하늘이 예상됩니다."
    elif '환율' in input_text:
        answer_text = "원 달러 환율은 1400원입니다."
    elif '고마워' in input_text:
        answer_text = "별 말씀을요."
    elif '종료' in input_text:
        answer_text = "다음에 또 만나요."
        stop_listening(wait_for_stop=False)  # 더이상 듣지 않음
    elif '자비스' in input_text:
        answer_text = "부르셨나요?"
    else:
        answer_text = "잘 이해하지 못했어요."
    speak(answer_text)


def speak(text):  # 소리내어 읽기 (TTS)
    print('[인공지능] ' + text)  # 인공지응이 하는말 텍스트 출력
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='ko')  # 한글로 저장
    tts.save(file_name)  # file_name으로 해당 mp3파일 저장
    playsound(file_name)  # 저장한 mp3파일을 읽어줌
    if os.path.exists(file_name):  # file_name 파일이 존재한다면
        os.remove(file_name)  # 실행 이후 mp3 파일 제거


r = sr.Recognizer()
m = sr.Microphone()

speak('무엇을 도와드릴까요?')

# 계속 귀를 열어둠 m(마이크)를 통해 듣다가 내가 정의한 listen함수 호출
stop_listening = r.listen_in_background(m, listen)  # listen 함수 호출

# 프로그램 종료 방지
while True:
    time.sleep(0.1)
