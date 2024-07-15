import io

import streamlit as st
from PIL import Image

import ncp_ocr

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
