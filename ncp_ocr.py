import os

# from dotenv import load_dotenv
import base64
import streamlit as st
import requests
import json

# load_dotenv()
# OCR API 엔드포인트 URL
ocr_url = "https://a4si57wev1.apigw.ntruss.com/custom/v1/30946/9f18bfacfd98fb975e7844826ba6c78ac5c30dc64cf0d702f815472661cc83c1/general"
# api_key = os.getenv("API_KEY")
api_key = st.secrets["API_KEY"]


def parse_ocr_response(response):
    if not response or 'images' not in response or not response['images']:
        return "No valid OCR response received."

    # 이미지 정보 추출
    image_info = response['images'][0]
    result_text = []

    # OCR 결과 상태 확인
    if image_info['inferResult'] != 'SUCCESS':
        return f"OCR inference failed: {image_info.get('message', 'No message available')}"

    # 필드 정보 추출
    fields = image_info.get('fields', [])
    for field in fields:
        text = field.get('inferText', '')
        line_break = field.get('lineBreak', False)
        result_text.append(text)
        if line_break:
            result_text.append("\n")

    # 결과를 하나의 문자열로 반환
    return " ".join(result_text).replace(" \n ", "\n")


def request_ocr(image_data, image_format):
    # 이미지 데이터를 Base64로 인코딩
    image_base64 = base64.b64encode(image_data.getvalue()).decode('utf-8')

    # 요청 헤더 설정
    headers = {
        "X-OCR-SECRET": api_key,
        "Content-Type": "application/json"
    }

    # 요청 데이터 설정
    data = {
        "images": [
            {
                "format": image_format,
                "name": "sample",
                "data": image_base64
            }
        ],
        "requestId": "unique-request-id",
        "version": "V2",
        "timestamp": 0
    }

    # API 호출
    response = requests.post(ocr_url, headers=headers, data=json.dumps(data))
    result = ""
    # 응답 확인
    if response.status_code == 200:
        result = response.json()
        # print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    return parse_ocr_response(result)
