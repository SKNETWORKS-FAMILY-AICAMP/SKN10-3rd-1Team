import requests
from openai import OpenAI
from langchain.tools import Tool

# ✅ API 키 설정
TAVILY_API_KEY = "key"
OPENAI_API_KEY = "key"

# ✅ OpenAI 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

# 🔍 Tavily 검색
def tavily_search(query: str) -> str:
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": True
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result.get("answer", "검색 결과가 없습니다.")
    else:
        return f"Tavily 검색 오류: {response.status_code} - {response.text}"

# 🌐 영어 → 한글 번역 (GPT 사용)
def translate_to_korean(text: str) -> str:
    try:
        messages = [
            {"role": "system", "content": "You are a translator that translates English to Korean."},
            {"role": "user", "content": f"Translate this to Korean:\n{text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"번역 오류: {str(e)}"

# 🧠 전체 통합
def tavily_search_korean(query: str) -> str:
    english_result = tavily_search(query)
    korean_result = translate_to_korean(english_result)
    return korean_result

# ✅ LangChain Tool 객체 생성
tavily_tool = Tool(
    name="TavilySearchKorean",
    func=tavily_search_korean,
    description=(
        "실시간 웹 검색 결과를 한글로 요약해주는 도구입니다. "
        "삼성전자 채용, 뉴스, 트렌드 관련 질문에 사용하세요."
    )
)
