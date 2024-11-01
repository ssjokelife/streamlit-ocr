import base64
import os
from google.cloud import vision


# 서비스 계정 키 파일 경로 설정
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'files/python-spreadsheet-419221-aa484c1a1b0d.json'


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def detect_text_in_image(image_content, language_hints="en"):
    """Detects text in the provided image content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    # 그리스어 힌트 추가
    image_context = vision.ImageContext(language_hints=[language_hints])

    # 텍스트 감지
    response = client.text_detection(image=image, image_context=image_context)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    return texts[0].description if texts else ""


def detect_tables_in_image(image_content):
    """Detects tables in the provided image content using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    # 문서 텍스트 감지 요청
    response = client.document_text_detection(image=image)
    annotation = response.full_text_annotation

    if response.error.message:
        raise Exception(f'{response.error.message}')

    # 페이지별로 텍스트 블록을 처리합니다.
    tables = []
    for page in annotation.pages:
        for block in page.blocks:
            block_text = []
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    block_text.append((word_text, word.bounding_box))

            # 블록의 텍스트와 위치 정보를 사용하여 테이블을 구성합니다.
            tables.append(block_text)

    return tables


def extract_table_from_blocks(blocks):
    """Extracts table from detected blocks based on positions."""
    import pandas as pd

    # 각 단어의 중앙 x 좌표를 기준으로 행, 열을 결정합니다.
    rows = {}
    for text, bounding_box in blocks:
        # 중간 y 좌표를 기준으로 행을 결정합니다.
        center_y = (bounding_box.vertices[0].y + bounding_box.vertices[2].y) / 2
        if center_y not in rows:
            rows[center_y] = []
        rows[center_y].append((text, bounding_box))

    # y 좌표 순서대로 정렬하여 테이블 행을 만듭니다.
    sorted_rows = sorted(rows.items(), key=lambda x: x[0])

    # 데이터프레임으로 변환
    table_data = []
    for _, row in sorted_rows:
        row_text = [text for text, _ in row]
        table_data.append(row_text)

    df = pd.DataFrame(table_data)
    return df


# # 예시 이미지 파일 경로
# image_path = 'DECO1.png'
#
# # 이미지에서 텍스트 추출
# blocks = detect_tables_in_image(encode_image_to_base64(image_path))
# for block in blocks:
#     df = extract_table_from_blocks(block)
#     print(df)
#     # print(detected_text)
