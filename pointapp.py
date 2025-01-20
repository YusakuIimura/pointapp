import streamlit as st

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

# カウントアップ関数
def add_to_count_immediate(side, value):
    if side == "left":
        st.session_state.left_count += value
        st.session_state.last_left = value
    elif side == "right":
        st.session_state.right_count += value
        st.session_state.last_right = value
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


# メイン画面
st.title("Molkky得点アプリ")
st.write("左右のカウントとランプ表示")

# 左右カウント表示
col1, col2 = st.columns(2)
with col1:
    st.subheader("左カウント")
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.left_count}</h1>", unsafe_allow_html=True)
    st.write("加算する値を選択:")
    # ボタンを2行に分けて表示
    left_buttons_row1 = st.columns(6)
    for i, btn in enumerate(left_buttons_row1):
        if btn.button(f"{i + 1}", key=f"left_{i + 1}"):
            add_to_count_immediate("left", i + 1)
    left_buttons_row2 = st.columns(6)
    for i, btn in enumerate(left_buttons_row2):
        if btn.button(f"{i + 7}", key=f"left_{i + 7}"):
            add_to_count_immediate("left", i + 7)
    if st.button("キャンセル (左)", key="cancel_left"):
        st.session_state.left_count -= st.session_state.last_left
        st.session_state.last_left = 0
        st.rerun()

with col2:
    st.subheader("右カウント")
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.right_count}</h1>", unsafe_allow_html=True)
    st.write("加算する値を選択:")
    # ボタンを2行に分けて表示
    right_buttons_row1 = st.columns(6)
    for i, btn in enumerate(right_buttons_row1):
        if btn.button(f"{i + 1}", key=f"right_{i + 1}"):
            add_to_count_immediate("right", i + 1)
    right_buttons_row2 = st.columns(6)
    for i, btn in enumerate(right_buttons_row2):
        if btn.button(f"{i + 7}", key=f"right_{i + 7}"):
            add_to_count_immediate("right", i + 7)
    if st.button("キャンセル (右)", key="cancel_right"):
        st.session_state.right_count -= st.session_state.last_right
        st.session_state.last_right = 0
        st.rerun()

# ミス表示のUI
st.subheader("ミス表示")
col1, col2 = st.columns(2)

# 左ミス表示
with col1:
    st.write("左ミス")
    st.markdown(render_lamps(st.session_state.left_mistakes), unsafe_allow_html=True)
    if st.button("左ミス追加"):
        if st.session_state.left_mistakes < 3:
            st.session_state.left_mistakes += 1
            st.rerun()

    if st.button("左ミスリセット"):
        st.session_state.left_mistakes = 0
        st.rerun()


# 右ミス表示
with col2:
    st.write("右ミス")
    st.markdown(render_lamps(st.session_state.right_mistakes), unsafe_allow_html=True)
    if st.button("右ミス追加"):
        if st.session_state.right_mistakes < 3:
            st.session_state.right_mistakes += 1
            st.rerun()

    if st.button("右ミスリセット"):
        st.session_state.right_mistakes = 0
        st.rerun()
