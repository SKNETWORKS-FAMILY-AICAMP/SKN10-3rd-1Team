from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# 크롬 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 창 안 띄우기 (테스트 끝나면 주석처리 가능)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

ids = []

# 자소서 리스트 페이지 순회
for page in range(1, 7):
    url = f"https://www.jobkorea.co.kr/starter/PassAssay/PassAssayList?schTxt=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&Page={page}"
    driver.get(url)

    # 스크롤 여러번 내려서 데이터 로딩 유도
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # 요소 로딩 대기 (최대 10초)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.listDefault a.name'))
        )
    except:
        print(f"{page} 페이지 로딩 실패")
        continue

    links = driver.find_elements(By.CSS_SELECTOR, 'div.tplList div.tplTit a')
    print(f"{page}페이지 수집 링크 수 : {len(links)}")

    for link in links:
        href = link.get_attribute('href')
        id_ = href.split('/')[-1]
        ids.append(id_)

    time.sleep(1)

print(f"총 수집한 자소서 ID 수 : {len(ids)}")

result = []

# 상세 페이지 크롤링
for id_ in ids:
    detail_url = f"https://www.jobkorea.co.kr/starter/PassAssay/View/{id_}"
    driver.get(detail_url)

    time.sleep(2)

    try:
        company = driver.find_element(By.CSS_SELECTOR, '.titBx h3').text
        general_review = driver.find_element(By.CSS_SELECTOR, '.tx').text
    except:
        print(f"데이터 없음 - {id_}")
        continue

    questions = driver.find_elements(By.CSS_SELECTOR, '.qnaList .q')
    answers = driver.find_elements(By.CSS_SELECTOR, '.qnaList .a')
    comments = driver.find_elements(By.CSS_SELECTOR, '.qnaList .commentTxt')

    reviews = []

    for q, a, c in zip(questions, answers, comments):
        reviews.append({
            "question": q.text.strip(),
            "answer": a.text.strip(),
            "comment": c.text.strip()
        })

    result.append({
        "company": company.strip(),
        "general_review": general_review.strip(),
        "reviews": reviews
    })

# json 저장
with open('samsung_full_reviews.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("크롤링 완료! samsung_full_reviews.json 생성 완료")

driver.quit()

