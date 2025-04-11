import requests
from bs4 import BeautifulSoup
import time
import random
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/135.0.0.0 Safari/537.36'
}

# 1. 자소서 리스트 페이지 순회하면서 id 수집
ids = []
for page in range(1, 7):  # 총 6페이지 (114건 기준)
    list_url = f"https://www.jobkorea.co.kr/starter/PassAssay/PassAssayList?schTxt=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&Page={page}"
    res = requests.get(list_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    links = soup.select('.listDefault a.name')
    for link in links:
        href = link['href']
        id_ = href.split('/')[-1]  # URL에서 id 추출
        ids.append(id_)
    
    time.sleep(random.uniform(1, 2))  # 딜레이

# 2. 상세 페이지 크롤링
base_detail_url = "https://www.jobkorea.co.kr/starter/PassAssay/View/{}"
result = []

for id_ in ids:
    url = base_detail_url.format(id_)
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    company = soup.select_one('.titBx h3')
    general_review = soup.select_one('.tx')

    if not company or not general_review:
        continue  # 데이터 없으면 건너뜀

    reviews = []

    questions = soup.select('.qnaList .q')
    answers = soup.select('.qnaList .a')
    comments = soup.select('.qnaList .commentTxt')

    for q, a, c in zip(questions, answers, comments):
        reviews.append({
            "question": q.get_text(strip=True),
            "answer": a.get_text(strip=True),
            "comment": c.get_text(strip=True)
        })

    result.append({
        "company": company.get_text(strip=True),
        "general_review": general_review.get_text(strip=True),
        "reviews": reviews
    })

    time.sleep(random.uniform(1, 2))  # 서버 부담 줄이기

# 3. json 파일로 저장
with open('samsung_full_reviews.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("크롤링 완료! samsung_full_reviews.json 파일 생성됨")