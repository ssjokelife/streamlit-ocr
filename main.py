import streamlit as st
from PIL import Image

import gcp_vision


# 비밀번호 설정
PASSWORD = "thomas4506"

# 'Buy Me a Coffee' 버튼 HTML 및 CSS 코드
buy_me_a_coffee_button = """
<div style="position: fixed; bottom: 70px; right: 10px;">
    <a href="https://www.buymeacoffee.com/ssjokelife" target="_blank">
        <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=ssjokelife&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff" />
    </a>
</div>
"""

# 'Buy Me a Coffee' 버튼 표시
st.markdown(buy_me_a_coffee_button, unsafe_allow_html=True)


def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 보안상 비밀번호를 메모리에서 삭제
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 비밀번호 입력 창
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # 비밀번호가 틀린 경우
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Password is incorrect")
        return False
    else:
        return True

if check_password():
    # 여러 파일 업로드를 허용
    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    # 언어 선택 박스
    language_option = st.selectbox("언어를 선택하세요:", ["한글", "희랍어", "영어"])

    # 선택한 언어에 따라 language_hints 설정
    language_hints = {
        "한글": "ko",
        "희랍어": "el",
        "영어": "en"
    }

    selected_language = language_hints.get(language_option, "en")  # 기본값은 영어

    if st.button("요청"):
        if len(uploaded_files) > 0:
            with st.status("OCR 요청 중...", expanded=True):
                result = ""
                for uploaded_file in uploaded_files:
                    image_content = uploaded_file.read()
                    temp = gcp_vision.detect_text_in_image(image_content, selected_language)
                    result += temp + "\n"
                    result += "=" * 80 + "\n"

            st.text_area("결과", value=result)
        else:
            st.warning('이미지를 첨부해야 합니다.', icon="⚠️")

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # 파일을 열기
            img = Image.open(uploaded_file)

            # 이미지 표시
            st.image(img, caption=uploaded_file.name)
else:
    st.write("Please enter the password to access this app.")




