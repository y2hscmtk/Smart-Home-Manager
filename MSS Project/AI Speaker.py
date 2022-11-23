# TTS와 STT를 활용한 인공지능과 대화하기
import sys
import io
import time
import os  # 프로그램 종료 방지용
import threading
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import paho.mqtt.client as mqtt

isCall = False  # 호출어가 명령된 상태인지 확인
wai = True  # mqtt 수신 명령을 말하는동안 스피커가 말하는 소리를 음성으로 인식하지 않도록
power = True  # 스피커의 전원에 해당
guest = True  # 손님 방문에 대한 정보를 알렸는지 여부를 저장
answer_text = '입력이 되지 않았습니다'
r = sr.Recognizer()
# = sr.Microphone()  # 마이크에 해당

broker_address = "192.168.216.87"  # input("브로커 IP>>")


# 스피커에서는 온습도정보, 손님방문정보를 구독함
def onConnect(client, userdata, flag, rc):
    if (rc == 0):
        print(" 연결되었습니다")
        client.subscribe("temperature", qos=0)  # 온도 정보
        client.subscribe("humidity", qos=0)  # 습도 정보
        client.subscribe("guest", qos=0)  # 손님 방문 유무
    pass  # 이것은 더미다 . 보통 함수 onConnect 의 끝임을 표시 함


def onMessage(client, userdata, msg):
    global guest
    command = str(msg.payload.decode("utf-8"))  # 소수점 제거
    # 이미지 데이터가 바이트 배열로 도착, 이것은 보내는쪽에서 바이트배열로 보내야함을 의미함
    if (msg.topic == "temperature"):
        speak("현재 온도는 " + command + "도 이며")
    if (msg.topic == "humidity"):
        speak("현재 습도는 " + command + "입니다.")
    if (msg.topic == "guest"):
        if guest:  # 방문정보를 아직 알린적 없다면
            speak("손님이 방문하였습니다. 모바일 리모컨에서 확인하세요")
            guest = False  # 알렸다고 표시 => 중복 알림 방지
            start_time = threading.Timer(60, reset_guest)  # 1분 후 알림정보 리셋
            start_time.start()
    pass


def listen(recognizer, audio):  # 음성 인식 (듣기 )
    global wait
    try:
        text = recognizer.recognize_google(audio, language='ko')
        print("[User] " + text)

        # mqtt 수신 명령에 대한 처리
        if '날씨' in text:
            client.publish("command", "temperature", qos=0)  # 온도 정보 요구
            client.publish("command", "humidity", qos=0)  # 습도 정보 요구
            wait = False  # 날씨 정보에 관해 스피커가 말하는것을 음성명령으로 인식하지 않도록
        else:  # mqtt 송수신 명령 이외의 명령의 경우 => 불 켜줘, 등~
            answer(text)
    except sr.UnknownValueError:
        print("인식 실패")  # 음성 인식이 실패한 경우
        speak("잘 듣지 못했어요")
    except sr.RequestError as e:  # 네트워크 등의 이유로 연결이 제대로 안됐을경우 API Key 오류, 네트워크 단절 등
        print("요청 실패 : {0}".format(e))  # 에러형식 출력
    pass


def answer(input_text):  # 어떤 대답을 할것인지 정의
    global isCall, power, wait
    global answer_text  # 컴퓨터가 대답할 말 key값이 들어갔다면 출력되도록

    if '안녕' in input_text:
        answer_text = "안녕하세요? 반갑습니다."
    elif '불' in input_text:
        if '켜' in input_text:
            answer_text = "불을 켭니다"
            client.publish("command", "ledOn")  # 조명도에 따라 다른 세기로 불 키기
        elif '꺼' in input_text:
            answer_text = "불을 끕니다"
            client.publish("command", "ledOff")
    elif '감시' in input_text:
        if '켜' in input_text:
            answer_text = "CCTV를 킵니다. 모바일 리모컨에서 확인하세요"
            client.publish("command", "cctvOn")
        elif '꺼' in input_text:
            answer_text = "CCTV를 끕니다."
            client.publish("command", "cctvOff")
    elif '고마워' in input_text:
        answer_text = "별 말씀을요."
    elif '종료' in input_text:
        answer_text = "다음에 또 만나요."
        isCall = False
        power = False
        # stop_listening(wait_for_stop=False)  # 더이상 듣지 않음
    elif '거북' in input_text:
        answer_text = "부르셨나요?"
    else:
        answer_text = "잘 이해하지 못했어요."
    speak(answer_text)


def speak(text):  # 소리내어 읽기 (TTS)
    global wait
    wait = False  # 스피커가 말하는 동안은 명령 수신x
    print('[인공지능] ' + text)  # 인공지능이 하는말 텍스트 출력
    if "손님" in text:
        file_name = 'voice2.mp3'  # 음성파일 중복 삭제로 인한 오류를 해결하기 위함
    else:
        file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='ko')  # 한글로 저장
    tts.save(file_name)  # file_name으로 해당 mp3파일 저장
    playsound(file_name)  # 저장한 mp3파일을 읽어줌
    if os.path.exists(file_name):  # file_name 파일이 존재한다면
        os.remove(file_name)  # 실행 이후 mp3 파일 제거
        wait = True


# 음성 명령 권한을 회수하는 메소드
def reset_mode():
    global isCall
    isCall = False


# 손님 방문 알림에 대한 정보를 리셋
def reset_guest():
    global guest
    guest = True


# MQTT 제어
client = mqtt.Client()      # mqtt 클라이언트 객체 생성
client.on_connect = onConnect   # 연결요청시 Callback 함수
client.on_message = onMessage   # 이미지가 도착하였을때 Callback 함수
client.connect(broker_address, 1883)   # 브로커에 연결을 요청함
client.loop_start()  # 인공지능 스피커가 동작해야하므로 비동기식으로 별도의 스레드로 진행

# 스피커가 동작하는 공간
while power:
    with sr.Microphone() as source:  # 마이크에서 들리는 음성(source)을 listen을 통해 들음
        print('Listening')  # 잠깐의 대기 시간이 있으므로 확인용으로 텍스트 출력
        callName = r.listen(source)  # 마이크로부터 호출어 듣기
        text = ""  # 예외처리문 밖에서도 이용하기 위해
        # 호출어에 대한 예외처리
        try:
            # 구글 API 로 인식 (하루 50회만 허용)
            # 영어는 language = 'en-US
            text = r. recognize_google(callName, language='ko')  # 한국어 음성으로 변환
            print(text)  # 정상 작동 확인용
        except sr.UnknownValueError:
            print("인식 실패")  # 음성 인식이 실패한 경우
        except sr.RequestError as e:  # 네트워크 등의 이유로 연결이 제대로 안됐을경우 API Key 오류, 네트워크 단절 등
            print("요청 실패 : {0}".format(e))  # 에러형식 출력
            # 사용자에게 오류사실을 알림
            speak("네트워크 오류가 발생했습니다. 지속적인 오류가 발생할 경우 관리자에게 문의하세요")

        if "거북" in text:  # 음성이 키워드일때 명령을 할수있게 변경
            isCall = True
            wait = True
            speak("안녕하세요!")

            # 아무 명령을 하지 않더라도, 20초가 지나면 명령 권한 회수
            start_time = threading.Timer(50, reset_mode)  # 20초후 reset
            start_time.start()
        else:
            continue

    # 명령 권한이 있는 상태에서는 계속 명령을 받을 수 있음
    while isCall:
        while wait:
            with sr.Microphone() as source:
                command = r.listen(source)  # 마이크로부터 음성 듣기
                listen(r, command)

client.disconnect()
client.loop_stop()
