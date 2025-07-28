import streamlit as st
import numpy as np
import random
from pydub.generators import Sine
from io import BytesIO
import base64
from pydub.generators import Sine, Sawtooth


# -----------------------------
# 튜토리얼 안내
# -----------------------------
st.title("🎵 AI 음악 생성기")
st.markdown("""
이 웹앱은 감정, 느낌, 또는 장르를 입력하면 AI가 해당 분위기를 표현하는 **30초~1분 길이의 음악**을 생성해줍니다.

**사용법:**
1. 아래 입력창에 당신의 감정, 느낌, 또는 원하는 장르를 입력하세요. (예: "행복한 느낌", "잔잔하고 고요한", "록 장르")
2. '음악 생성하기' 버튼을 누르세요.
3. AI가 생성한 음악을 웹에서 바로 듣거나 다운로드할 수 있습니다.

이 활동을 통해 **AI의 윤리적 영향, 데이터 편향성, 저작권 문제** 등에 대해 함께 생각해볼 수 있어요! 🎧
""")

# (코드 추가 요청 주석): 영상 바로 아래에 학생들의 개인적인 생각을 기록하는 부분을 포함하고, 제출하기 버튼을 클릭하면, data.txt에 append되도록 합니다.
# -----------------------------
# 사용자 입력 받기
# -----------------------------
user_input = st.text_area("1. 감정, 느낌 또는 장르를 입력해주세요:", placeholder="예: 다급함, 긴장, 고뇌, 고민, 걱정, 긴장, 무서운, 혼란, 신남, 당돌함 등")

# -----------------------------
# 감정/장르에 따라 파라미터 매핑
# -----------------------------
def get_music_params(feeling):
    feeling = feeling.lower()

    if "다급함" in feeling or "긴장" in feeling:
        return {
            "base_freq": 660,
            "beat": 0.2,
            "volume": -8,
            "wave_type": "sine",
            "freq_range": 80  # 변화 적당히
        }

    elif "고뇌" in feeling or "고민" in feeling or "걱정" in feeling:
        return {
            "base_freq": 200,
            "beat": 1.0,
            "volume": -20,
            "wave_type": "sine",
            "freq_range": 20  # 변화 거의 없음 → 안정적
        }

    elif "긴장" in feeling or "무서운" in feeling:
        return {
            "base_freq": 350,
            "beat": 0.15,
            "volume": -6,
            "wave_type": "sawtooth",
            "freq_range": 200  # 매우 넓은 변화 → 불안정
        }

    elif "혼란" in feeling:
        return {
            "base_freq": 330,
            "beat": 0.35,
            "volume": -10,
            "wave_type": "sine",
            "freq_range": 100  # 불규칙하지만 멜로딕
        }

    elif "신남" in feeling or "당돌함" in feeling:
        return {
            "base_freq": 500,
            "beat": 0.15,
            "volume": -5,
            "wave_type": "sawtooth",
            "freq_range": 50  # 약간의 역동성
        }

    else:
        return {
            "base_freq": 440,
            "beat": 0.5,
            "volume": -12,
            "wave_type": "sine",
            "freq_range": 60
        }


# -----------------------------
# 음악 생성 함수
# -----------------------------
def generate_music(params, duration=30, wave_type="sine"):
    from pydub import AudioSegment
    music = AudioSegment.silent(duration=0)
    
    for _ in range(int(duration / params["beat"])):
        freq = params["base_freq"] + random.choice([-50, 0, 50])
        
        if wave_type == "sawtooth":
            tone = Sawtooth(freq).to_audio_segment(duration=int(params["beat"] * 1000)).apply_gain(params["volume"])
        else:  # default is sine
            tone = Sine(freq).to_audio_segment(duration=int(params["beat"] * 1000)).apply_gain(params["volume"])
        
        music += tone
    
    return music


# -----------------------------
# 오디오 파일 다운로드 링크 생성
# -----------------------------
def get_audio_download_link(audio_segment, filename="generated_music.wav"):
    buf = BytesIO()
    audio_segment.export(buf, format="wav")
    byte_data = buf.getvalue()
    b64 = base64.b64encode(byte_data).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="{filename}">🎶 음악 다운로드</a>'
    return href

# -----------------------------
# 버튼 클릭 시 음악 생성
# -----------------------------
if st.button("🎼 음악 생성하기"):
    if user_input.strip() == "":
        st.warning("감정, 느낌 또는 장르를 입력해주세요!")
    else:
        with st.spinner("음악 생성 중..."):
            params = get_music_params(user_input)
            music = generate_music(params, duration=random.randint(30, 60))
            # 음악을 메모리에 export
            buf = BytesIO()
            music.export(buf, format="wav")
            st.audio(buf.getvalue(), format="audio/wav")
            st.markdown(get_audio_download_link(music), unsafe_allow_html=True)

# -----------------------------
# 샘플 데이터 설명
# -----------------------------
st.markdown("""
---
### 📁 샘플 데이터 구성 (시뮬레이션용) 설명
- `music_dataset.csv` : 음악 파일 경로 + 감정(예: happy, sad 등) + 장르 정보 포함
- 예시:
```
file_path,emotion,genre
data/happy1.wav,happy,pop
data/sad1.wav,sad,ballad
```
- Kaggle 등에서 `GTZAN`, `NSynth`, `EmoMusic Dataset` 등을 활용 가능

📌 실제 AI 학습을 위한 모델을 넣을 수도 있지만, 본 웹앱은 고등학생 수업용으로 음악을 직접 생성하는 시뮬레이션 기반입니다.
""")
