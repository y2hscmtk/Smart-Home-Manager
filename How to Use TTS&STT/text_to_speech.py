# TTS (Text To Speech) 글자를 읽어줌
# STT (Speech To Text) 말하면 글자로 변환

# 가상환경 생성
# 터미널 - + - Command Prompt
# python -m venv myenv
# .\myenv\Scripts\activate
# pip install gTTS => 구글에서 제공하는 TTS 서비스
# pip install playsound==1.2.2 구버전으로 설치(문제 방지)

from playsound import playsound
from winsound import PlaySound
from gtts import gTTS
# 컴퓨터 음성으로 바꾸기 위해 텍스트를 정의
# 텍스트를 생성한후 gTTS를 이용하여 텍스트를 음성으로 변환

file_name = 'sample.mp3'  # 저장할 파일 이름

# 영어 문장
# text = 'Imagine that you have just arrived at a hotel after a tiring 7-hour overnight flight'  # 변환할 문자열
# tts_en = gTTS(text=text, lang='en')  # 문자 = 변수, 언어 = 영어
# tts_en.save(file_name)  # file_name으로 해당 mp3파일 저장


# 한글 문장
# text = "파이썬을 배우면 이런 것도 할 수 있어요"
# tts_ko = gTTS(text=text, lang='ko')  # 한글로 저장
# tts_ko.save(file_name)  # file_name으로 해당 mp3파일 저장
# playsound(file_name)  # 저장한 mp3파일을 읽어줌

# 긴 문장 (파일에서 불러와서 처리)
with open('sample.txt', 'r', encoding='utf-8') as f:
    text = f.read()

tts_ko = gTTS(text=text, lang='ko')  # 한글로 저장
tts_ko.save(file_name)  # file_name으로 해당 mp3파일 저장
playsound(file_name)  # 저장한 mp3파일을 읽어줌
