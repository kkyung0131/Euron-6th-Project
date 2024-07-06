from audioop import add
from selenium import webdriver
from selenium.webdriver.common.by import By
import string
import time
import pandas as pd
import re

url_list = []
data_id = []
datas = []

def infinite_loop(driver):
    # 최초 페이지 스크롤 설정
    # 스크롤 시키지 않았을 때의 전체 높이
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # 윈도우 창을 0에서 위에서 설정한 전체 높이로 이동
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1.0)
        # 스크롤 다운한 만큼의 높이를 신규 높이로 설정 
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        # 직전 페이지 높이와 신규 페이지 높이 비교
        if new_page_height == last_page_height:
            time.sleep(1.0)
            # 신규 페이지 높이가 이전과 동일하면, while문 break
            if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                break
        else:
            last_page_height = new_page_height

def naverMapCrawling(search):

    driver = webdriver.Chrome()

    # 모바일 네이버 지도
    driver.get(f"https://m.map.naver.com/search2/search.naver?query={search}") 
    driver.implicitly_wait(3) # 로딩이 끝날 때 까지 10초까지는 기다림

    infinite_loop(driver)

    items = driver.find_elements(By.CSS_SELECTOR, '._item ')

    for item in items:
        title = item.get_attribute('data-title')
        id = int(item.get_attribute('data-id'))
        
        for character in string.punctuation:
            title = title.replace(character, '')

        datas.append({
            "id" : id,
            "title" : title
            })

        data_id.append(id)
        

    print(datas)

    for id in data_id:
        # 홈 탭으로 이동
        driver.get(f'https://m.place.naver.com/place/{id}/home')
        time.sleep(1)

        # 별점
        try: 
            score = driver.find_element(By.CSS_SELECTOR, '.LXIwF').text
            score_num = float(re.findall("\d+.\d+",score)[0]) # 데이터에서 별점만 추출
            print(score_num)
        except:
            score_num = ""
            print("별점 없음")

        for data in datas:
            if data["id"] == id:
                data["score_val"] = score_num
                break
     
        # 음식 카테고리
        try: 
            category = driver.find_element(By.CSS_SELECTOR, 'span.lnJFt').text
            print(category)
        except:
            category = ""
            print("카테고리 없음")

        for data in datas:
            if data["id"] == id:
                data["category"] = category
                break
        
        # 가게 설명글
        try: 
            descript = driver.find_element(By.CSS_SELECTOR, 'div.XtBbS').text.strip("'\"")
            descript = descript.replace("\n", " ") # 중간에 있는 엔터 없애기
            print(descript)
        except:
            descript = ""
            print("가게설명 없음")

        for data in datas:
            if data["id"] == id:
                data["descript"] = descript
                break
        
        # 리뷰 탭으로 이동
        driver.get(f'https://m.place.naver.com/place/{id}/review/visitor')
        time.sleep(1)

        # 대표 키워드 (3개)
        try: 
            keyword1 = driver.find_elements(By.CSS_SELECTOR, 'span.t3JSf')[0].text.strip("'\"")
            keyword2 = driver.find_elements(By.CSS_SELECTOR, 'span.t3JSf')[1].text.strip("'\"")
            keyword3 = driver.find_elements(By.CSS_SELECTOR, 'span.t3JSf')[2].text.strip("'\"")

            print(keyword1)
            print(keyword2)
            print(keyword3)
        except:
            keyword1 = ""
            keyword2 = ""
            keyword3 = ""
            print("키워드 없음")

        for data in datas:
            if data["id"] == id:
                data["keyword1"] = keyword1
                data["keyword2"] = keyword2
                data["keyword3"] = keyword3
                break
        
        # 긴 리뷰 펼치기
        try:
            extension_btn = driver.find_elements(By.CSS_SELECTOR, 'span.rvCSr')
            for btn in extension_btn:
                btn.click()
        except:
            print("긴 리뷰 없음")

        # 리뷰(5개)
        try:             
            reviews = ""
            for i in range(5):
                try:
                    review = driver.find_elements(By.CSS_SELECTOR, 'span.zPfVt')[i].text
                    if(i == 0):
                        reviews = f'{review}' # 리뷰를 reviews에 누적
                    else:
                        reviews = f'{reviews} / {review}' # 각 리뷰는 /로 구분
                except IndexError:
                    print("리뷰가 충분하지 않음") # 리뷰가 5개 이하인 가게
                    break
            reviews = reviews.replace("\n", " ") # 리뷰 중간 엔터 제외
            print(reviews)
        except Exception as e:
            reviews = ""
            print("리뷰 없음")

        for data in datas:
            if data["id"] == id:
                data["reviews"] = reviews
                
                break
    
    # csv 파일 내보내기
    df = pd.DataFrame(datas, columns=["id", "title", "score_val", "category", "descript", "reviews", "keyword1", "keyword2", "keyword3"])
    df.to_csv("result1.csv", index=False) # 내보낼 파일 이름 설정

# 함수 실행
search = "동탄 맛집" # 여기에 검색어 입력
naverMapCrawling(search)
