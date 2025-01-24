import streamlit as st
import os
import base64
import time

# 初期値の設定
if "left_count" not in st.session_state:
    st.session_state.left_count = 0
if "right_count" not in st.session_state:
    st.session_state.right_count = 0
if "last_left" not in st.session_state:
    st.session_state.last_left = 0
if "last_right" not in st.session_state:
    st.session_state.last_right = 0
if "left_mistakes" not in st.session_state:
    st.session_state.left_mistakes = 0  # 左ランプのカウント
if "right_mistakes" not in st.session_state:
    st.session_state.right_mistakes = 0  # 右ランプのカウント

# カスタムCSSを追加
st.markdown(
    """
    <style>
    /* 左側のスタイル */
    .left-text {
        color: #007acc; /* 青系 */
        font-weight: bold;
    }
    .left-button .stButton>button {
        background-color: #cceeff !important; /* 青系 */
        color: #007acc !important;
        border: 2px solid #007acc !important;
        border-radius: 5px !important;
    }

    /* 右側のスタイル */
    .right-text {
        color: #cc0000; /* 赤系 */
        font-weight: bold;
    }
    .right-button .stButton>button {
        background-color: #ffcccc !important; /* 赤系 */
        color: #cc0000 !important;
        border: 2px solid #cc0000 !important;
        border-radius: 5px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# カウントアップ関数
def add_to_count_and_reset_mistakes(side, value):
    if side == "left":
        st.session_state.left_count += value
        st.session_state.last_left = value
        if st.session_state.left_count>50:
            st.session_state.left_count = 25
        st.session_state.left_mistakes = 0  # ミスのランプをリセット
    elif side == "right":
        st.session_state.right_count += value
        st.session_state.last_right = value
        if st.session_state.right_count>50:
            st.session_state.right_count = 25
        st.session_state.right_mistakes = 0  # ミスのランプをリセット
    st.rerun()

# ランプ表示のHTML作成
def render_lamps(mistake_count):
    lamps = []
    for i in range(3):
        color = "green" if i < mistake_count else "gray"
        lamps.append(
            f"<div style='width: 30px; height: 30px; background-color: {color}; margin: 0 5px; border-radius: 50%; display: inline-block;'></div>"
        )
    return "".join(lamps)

# 音声再生用関数
def get_audio_html(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            b64_audio = base64.b64encode(audio_bytes).decode()
            audio_html = f"""
            <audio autoplay>
                <source src="data:audio/wav;base64,{b64_audio}" type="audio/wav">
            </audio>
            """
            return audio_html
    else:
        st.error(f"音声ファイル '{file_path}' が見つかりません！")
        return ""

def play_local_sound(file_path):
    audio_html = get_audio_html(file_path)
    if audio_html:
        st.markdown(audio_html, unsafe_allow_html=True)

# メイン画面
st.title("Molkky得点アプリ")

# 左右全体のレイアウト
col1, col2 = st.columns(2)

# 左側
with col1:
    st.markdown('<p class="left-text">左サイド</p>', unsafe_allow_html=True)
    st.markdown(f"<h1 class='left-text'>得点: {st.session_state.left_count}</h1>", unsafe_allow_html=True)
    st.write("加算する値を選択:")
    with st.container():
        left_buttons_row1 = st.columns(6)
        for i, btn in enumerate(left_buttons_row1):
            with btn:
                if st.button(f"{i + 1}", key=f"left_{i + 1}"):
                    add_to_count_and_reset_mistakes("left", i + 1)
        left_buttons_row2 = st.columns(6)
        for i, btn in enumerate(left_buttons_row2):
            with btn:
                if st.button(f"{i + 7}", key=f"left_{i + 7}"):
                    add_to_count_and_reset_mistakes("left", i + 7)
    if st.button("キャンセル (左)", key="cancel_left"):
        st.session_state.left_count -= st.session_state.last_left
        st.session_state.last_left = 0
        st.rerun()
    st.write("ミス表示:")
    st.markdown(render_lamps(st.session_state.left_mistakes), unsafe_allow_html=True)
    if st.button("左ミス追加"):
        if st.session_state.left_mistakes < 3:
            st.session_state.left_mistakes += 1
            st.session_state.play_sound = True
            st.rerun()
    if st.button("左ミスリセット"):
        st.session_state.left_mistakes = 0
        st.rerun()

# 右側
with col2:
    st.markdown('<p class="right-text">右サイド</p>', unsafe_allow_html=True)
    st.markdown(f"<h1 class='right-text'>得点: {st.session_state.right_count}</h1>", unsafe_allow_html=True)
    st.write("加算する値を選択:")
    with st.container():
        right_buttons_row1 = st.columns(6)
        for i, btn in enumerate(right_buttons_row1):
            with btn:
                if st.button(f"{i + 1}", key=f"right_{i + 1}"):
                    add_to_count_and_reset_mistakes("right", i + 1)
        right_buttons_row2 = st.columns(6)
        for i, btn in enumerate(right_buttons_row2):
            with btn:
                if st.button(f"{i + 7}", key=f"right_{i + 7}"):
                    add_to_count_and_reset_mistakes("right", i + 7)
    if st.button("キャンセル (右)", key="cancel_right"):
        st.session_state.right_count -= st.session_state.last_right
        st.session_state.last_right = 0
        st.rerun()
    st.write("ミス表示:")
    st.markdown(render_lamps(st.session_state.right_mistakes), unsafe_allow_html=True)
    if st.button("右ミス追加"):
        if st.session_state.right_mistakes < 3:
            st.session_state.right_mistakes += 1
            st.session_state.play_sound = True
            st.rerun()
    if st.button("右ミスリセット"):
        st.session_state.right_mistakes = 0
        st.rerun()

# 音声を自動再生
if st.session_state.get("play_sound", False):
    st.session_state.play_sound = False
    play_local_sound("miss_announce.mp3")
