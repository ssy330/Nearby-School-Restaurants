# 필요한 라이브러리 임포트
import gradio as gr
import requests
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# Google Places API 키 설정
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# 식당을 찾는 함수 정의
def find_restaurants(menu_name, location='37.27014, 127.1261', radius=5000):
    # Google Places API의 URL 설정
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    # API 요청에 필요한 파라미터 설정
    params = {
        'key': API_KEY,
        'location': location,  # 검색할 위치 (위도, 경도) -> 37.27014, 127.1261
        'radius': radius,  # 검색 반경 (미터 단위) -> 5km
        'keyword': menu_name,  # 검색할 키워드 (메뉴 이름)
        'type': 'restaurant',  # 장소 유형 (식당)
        'language': 'ko'  # 응답 언어 (한국어)
    }
    
    # API 요청 보내기
    response = requests.get(url, params=params)
    # 응답에서 결과 가져오기
    results = response.json().get('results', [])
    
    # 식당 목록 저장할 리스트 초기화
    restaurants = []
    # 최대 10개의 결과 처리
    for result in results[:10]: 
        name = result.get('name')  # 식당 이름 가져오기
        address = result.get('vicinity')  # 식당 주소 가져오기
        restaurants.append(f"{name} - {address}")  # 식당 이름과 주소를 리스트에 추가
    
    # 검색 결과가 없을 때 메시지 반환
    if not restaurants:
        return "근처에 해당 메뉴를 제공하는 식당을 찾을 수 없습니다."
    
    # 결과를 문자열로 반환
    return "\n".join(restaurants)

# 사용자 입력을 처리하는 함수 정의
def chatbot_response(user_input):
    # 사용자가 입력한 메뉴 이름을 이용해 식당 검색
    return find_restaurants(user_input)

# Gradio 인터페이스 설정
iface = gr.Interface(
    fn=chatbot_response,  # 사용자 입력을 처리할 함수
    inputs="text",  # 입력 유형 (텍스트)
    outputs="text",  # 출력 유형 (텍스트)
    title="강남대 근처 식당 찾기",  # 인터페이스 제목
    description="메뉴 이름을 입력하면 강남대 근처의 해당 메뉴를 제공하는 식당을 찾습니다."  # 인터페이스 설명
)

# 인터페이스 실행
iface.launch()
