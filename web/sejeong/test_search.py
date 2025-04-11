from tavily_tool import tavily_search_korean

query = "삼성전자 인재상과 추구하는 목표는 무엇인가요?"
result = tavily_search_korean(query)
print("🔍 최종 검색 결과 (한국어):", result)
