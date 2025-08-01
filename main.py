import streamlit as st
import numpy as np
import random
from pathlib import Path
from pydub.generators import Sine, Sawtooth
from pydub import AudioSegment
from io import BytesIO
import base64
from datetime import datetime

# -----------------------------
# 사이드바 섹션 선택
# -----------------------------
st.sidebar.title("🎧 AI 음악 체험")
page = st.sidebar.radio("이동할 섹션을 선택하세요:", ["🎵 AI 음악 생성기", "🧠 AI 음악 판별하기"])

# -----------------------------
# 사이드바 안내 문구 (페이지별 다르게 표시)
# -----------------------------
if page == "🎵 AI 음악 생성기":
    st.sidebar.markdown("""
    이 웹앱은 감정, 느낌, 또는 장르를 입력하면 AI가 해당 분위기를 표현하는 **30초~1분 길이의 음악**을 생성해줍니다.

    **사용법:**
    1. 아래 입력창에 당신의 감정, 느낌을 입력하세요. (예: 다급함, 긴장, 고뇌, 고민, 걱정, 긴장, 무서운, 혼란, 신남, 당돌함)
    2. '음악 생성하기' 버튼을 누르세요.
    3. AI가 생성한 음악을 웹에서 바로 듣거나 다운로드할 수 있습니다.

    이 활동을 통해 **AI의 윤리적 영향, 데이터 편향성, 저작권 문제** 등에 대해 함께 생각해볼 수 있어요! 🎧
    """)

elif page == "🧠 AI 음악 판별하기":
    st.sidebar.markdown("""
    이 섹션에서는 미리 준비된 음악을 듣고 그것이 **AI가 생성한 음악인지 아닌지**를 판별해보는 활동을 합니다.

    **사용법:**
    1. 음악을 들어보세요.
    2. AI가 생성했는지 여부를 선택하세요.
    3. 음악을 듣고 느낀 감정을 입력하세요.
    4. '제출하기' 버튼을 누르면 결과가 기록됩니다.

    이 활동을 통해 **AI 창작물 판별의 어려움**, **감정 분석**, 그리고 **AI 윤리 및 저작권 문제**에 대해 고민해볼 수 있습니다. 🎼
    """)

# -----------------------------
# 함수: 감정 기반 음악 파라미터 설정
# -----------------------------
def get_music_params(feeling):
    feeling = feeling.lower()
    if "다급함" in feeling or "긴장" in feeling:
        return {"base_freq": 660, "beat": 0.2, "volume": -8, "wave_type": "sine", "freq_range": 80}
    elif "고뇌" in feeling or "고민" in feeling or "걱정" in feeling:
        return {"base_freq": 200, "beat": 1.0, "volume": -20, "wave_type": "sine", "freq_range": 20}
    elif "무서운" in feeling:
        return {"base_freq": 350, "beat": 0.15, "volume": -6, "wave_type": "sawtooth", "freq_range": 200}
    elif "혼란" in feeling:
        return {"base_freq": 330, "beat": 0.35, "volume": -10, "wave_type": "sine", "freq_range": 100}
    elif "신남" in feeling or "당돌함" in feeling:
        return {"base_freq": 500, "beat": 0.15, "volume": -5, "wave_type": "sawtooth", "freq_range": 50}
    else:
        return {"base_freq": 440, "beat": 0.5, "volume": -12, "wave_type": "sine", "freq_range": 60}

# -----------------------------
# 함수: 음악 생성
# -----------------------------
def generate_music(params, duration=30):
    music = AudioSegment.silent(duration=0)
    for _ in range(int(duration / params["beat"])):
        freq = params["base_freq"] + random.choice([-50, 0, 50])
        if params["wave_type"] == "sawtooth":
            tone = Sawtooth(freq).to_audio_segment(duration=int(params["beat"] * 1000)).apply_gain(params["volume"])
        else:
            tone = Sine(freq).to_audio_segment(duration=int(params["beat"] * 1000)).apply_gain(params["volume"])
        music += tone
    return music

# -----------------------------
# 함수: 다운로드 링크 생성
# -----------------------------
def get_audio_download_link(audio_segment, filename="generated_music.wav"):
    buf = BytesIO()
    audio_segment.export(buf, format="wav")
    byte_data = buf.getvalue()
    b64 = base64.b64encode(byte_data).decode()
    return f'<a href="data:audio/wav;base64,{b64}" download="{filename}">🎶 음악 다운로드</a>'

# -----------------------------
# [탭 1] AI 음악 생성기
# -----------------------------
if page == "🎵 AI 음악 생성기":
    st.title("🎵 AI 음악 생성기")
    st.markdown("""
    ### 저작권이란?
                
    소설이나 시, 음악, 미술 등과 같은 저작물을 창작한 사람이 자신의 창작물을 복제, 공연, 전시, 방송, 또는 전송하는 등 
    법이 정하고 있는 일정한 방식으로 스스로 이용하거나, 다른 사람들이 그러한 방식으로 이용하는 것을 허락할 수 있는 권리
                
    ### 저작인접권이란?
                
    저작물을 해석하거나 전달하는 사람에게 부여되는 권리
    ex) 음반제작자, 방송사업자
                
    ### 음악을 생성해보아요 !
    """)
    user_input = st.text_area("1. 감정, 느낌을 입력해주세요:", placeholder="예: 다급함, 긴장, 고뇌, 고민 등")

    if st.button("🎼 음악 생성하기"):
        if user_input.strip() == "":
            st.warning("감정을 입력해주세요.")
        else:
            with st.spinner("음악 생성 중..."):
                params = get_music_params(user_input)
                music = generate_music(params, duration=random.randint(30, 60))
                buf = BytesIO()
                music.export(buf, format="wav")
                st.audio(buf.getvalue(), format="audio/wav")

                download_link = get_audio_download_link(music)
                st.markdown(f"""
                <div style='text-align: center;'>
                    <a href="{download_link.split('"')[1]}" download="generated_music.wav">
                        <button style='background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px;cursor:pointer;'>🎶 생성된 음악 다운로드</button>
                    </a>
                </div>""", unsafe_allow_html=True)

            st.markdown("""
            ---
            ### ⚖️ 생성형 음악과 저작권

            AI로 생성된 음악이라 하더라도 **창작물로 간주될 수 있으며**,  
            다른 사람의 창작물(샘플, 악보, 특정 스타일)을 **모방하거나 변형했을 경우 저작권 문제가 발생할 수 있습니다.**

            > 이 웹앱에서 생성된 음악은 수업/체험 목적에 한해 자유롭게 사용 가능하지만,  
            > 상업적 활용 시에는 생성한 콘텐츠에 대한 **저작권·소유권 문제**를 반드시 고려해야 합니다.

            ---
            ### ⚠️ 데이터 편향성에 대한 이해

            - AI는 사람이 만든 데이터를 학습해 동작합니다.  
            따라서 **학습에 사용된 데이터가 한쪽으로 치우쳐 있다면**, 결과도 그 방향으로 쏠릴 수 있습니다.
            - 예: 긍정적인 문장 위주로 학습되었다면, 중립적인 문장도 긍정으로 오인할 수 있습니다.
            - 이는 AI의 오류가 아닌, **학습 데이터의 편향성(Bias)** 때문입니다.
            - 우리가 AI를 사용할 때는 **AI가 완벽하지 않으며, 데이터에 따라 달라질 수 있음**을 인지해야 합니다.

            ---

            """)

# -----------------------------
# [탭 2] AI 음악 판별하기
# -----------------------------


elif page == "🧠 AI 음악 판별하기":
    st.title("🧠 AI 음악 판별 퀴즈")

    music_folder = Path("music_samples")
    music_files = list(music_folder.glob("*.wav")) + list(music_folder.glob("*.mp3"))

    if not music_files:
        st.warning("음악 파일이 없습니다. `music_samples/` 폴더에 `.wav` 또는 `.mp3` 파일을 추가하세요.")
    else:
        # 🎯 세션 상태에 선택된 파일이 없다면 무작위 선택해서 저장
        if "selected_file" not in st.session_state:
            st.session_state.selected_file = random.choice(music_files)

        selected_file = st.session_state.selected_file

        st.subheader("1. 아래 음악을 듣고 AI 생성 여부를 추측해보세요!")
        with open(selected_file, "rb") as audio_file:
            file_ext = selected_file.suffix.lower()
            file_format = "audio/wav" if file_ext == ".wav" else "audio/mp3"
            st.audio(audio_file.read(), format=file_format)

        is_ai = st.radio("이 음악은 AI가 생성한 음악인가요?", ["AI 생성", "AI 아님"])
        emotion = st.text_input("2. 이 음악을 들었을 때 어떤 감정이 느껴졌나요?")
        submit = st.button("제출하기")

        if submit:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_data = f"[{now}] 파일: {selected_file.name}, AI판별: {is_ai}, 감정: {emotion}\n"

            with open("log.txt", "a", encoding="utf-8") as f:
                f.write(log_data)

            st.success("제출되었습니다! 다음 음악으로 넘어갑니다 😊")

            # 🎯 다음 제출을 위해 세션 상태 초기화 → 다음 랜덤 음악으로 변경
            del st.session_state.selected_file
    # -----------------------------
    # 저장된 감상 결과 출력 (댓글창 스타일)
    # -----------------------------
    if Path("log.txt").exists():
        st.markdown("---")
        st.markdown("### 💬 이전 사용자 의견 보기")

        with open("log.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines.reverse()  # 최신 항목이 위로

        for line in lines:
            try:
                if not line.strip():
                    continue  # 빈 줄 건너뜀

                date_part = line.split("]")[0][1:]
                file_name = line.split("파일:")[1].split(",")[0].strip()
                ai_judgment = line.split("AI판별:")[1].split(",")[0].strip()
                emotion = line.split("감정:")[1].strip()

                st.markdown(f"""
                <div style='
                    background-color: #f0f2f6;
                    border-radius: 8px;
                    padding: 10px 15px;
                    margin-bottom: 10px;
                    border-left: 4px solid #4CAF50;
                '>
                    <span style='color: gray; font-size: 13px;'>{date_part}</span><br>
                    <strong>{file_name}</strong> |
                    <em>{ai_judgment}</em><br>
                    <span style='color: #333;'>{emotion}</span>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                # 에러가 나는 줄은 무시하고 넘어감
                print(f"⚠️ 잘못된 로그 형식: {line.strip()} - {e}")
                continue

