import io

import streamlit as st
from PIL import Image

import ncp_ocr


# 비밀번호 설정
PASSWORD = "thomas4506"

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

    if st.button("요청"):
        if len(uploaded_files) > 0:
            with st.status("OCR 요청 중...", expanded=True):
                result = ""
                for uploaded_file in uploaded_files:
                    image = Image.open(uploaded_file)
                    # 이미지를 BytesIO 객체로 변환
                    image_data = io.BytesIO()
                    image.save(image_data, format=image.format)

                    # OCR 요청
                    temp = ncp_ocr.request_ocr(image_data, image.format.lower())
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




