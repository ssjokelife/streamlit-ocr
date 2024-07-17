import os
from google.cloud import vision


# 서비스 계정 키 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'files/python-spreadsheet-419221-aa484c1a1b0d.json'


def detect_text_in_image(image_content):
    """Detects text in the provided image content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    # 텍스트 감지
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    return texts[0].description if texts else ""

# # 예시 이미지 파일 경로
# image_path = 'rotated_image.png'
#
# # 이미지에서 텍스트 추출
# detected_text = detect_text_in_image(image_path)
# print(detected_text)
