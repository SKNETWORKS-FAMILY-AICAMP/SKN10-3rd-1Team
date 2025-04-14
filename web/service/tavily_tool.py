import requests
from openai import OpenAI
from langchain.tools import Tool

# 🔍 Tavily 검색
def tavily_search(query: str, tavily_key) -> str:
    url = "https://api.tavily.com/search"
    headers = {
        "Authorization": f"Bearer {tavily_key}",
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
def translate_to_korean(text: str, openai_key) -> str:
    try:
        # ✅ OpenAI 초기화
        client = OpenAI(api_key=openai_key)

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
def tavily_search_korean(query: str, tavily_key, openai_key) -> str:
    english_result = tavily_search(query, tavily_key=tavily_key)
    korean_result = translate_to_korean(english_result, openai_key=openai_key)
    return korean_result

