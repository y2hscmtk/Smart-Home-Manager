# pip install SpeechRecognition
# pip install PyAudio

from email.mime import audio
import speech_recognition as sr

r = sr.Recognizer()  # Recognizer 객체를 r로 사용
with sr.Microphone() as source:  # 마이크에서 들리는 음성(source)을 listen을 통해 들음
    print('듣고 있어요')  # 잠깐의 대기 시간이 있으므로 확인용으로 텍스트 출력
    audio = r.listen(source)  # 마이크로부터 음성 듣기
# 녹음된 데이터를 구글에 전송 => 구글 서버에서 작업 => 텍스트를 보게됨 => network가 연결되어있어야함

# 예외처리문
try:
    # 구글 API 로 인식 (하루 50회만 허용)
    # 영어는 language = 'en-US
    text = r. recognize_google(audio, language='ko')  # 영어 음성으로 변환
    print(text)
except sr.UnknownValueError:
    print("인식 실패")  # 음성 인식이 실패한 경우
except sr.RequestError as e:  # 네트워크 등의 이유로 연결이 제대로 안됐을경우 API Key 오류, 네트워크 단절 등
    print("요청 실패 : {0}".format(e))  # 에러형식 출력

# 말을 하면 마이크 모듈을 이용하여 source에 음성을 저장하고 audio에 저장
# 인터넷이 잘 연결 되어있다면, 혹은 다른 오류가 없다면 문자로 변환해줌
