import json
import time
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://map.naver.com/v5/search'
driver = webdriver.Chrome()  # 드라이버 경로
driver.get(url)
key_word = '이대 맛집'  # 검색어

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경


# 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)

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

# css를 찾을때 까지 10초 대기
time_wait(10, 'div.input_box > input.input_search')

# (1) 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(1)

# (2) frame 변경
switch_frame('searchIframe')
page_down(80)
sleep(5)

# 가게 리스트
#parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.UEzoS')
# 페이지 리스트
next_btn = driver.find_elements(By.CSS_SELECTOR, '.zRM9F> a')

# dictionary 생성
parking_dict = {'가게데이터': []}
# 시작시간
start = time.time()
print('[크롤링 시작...]')

# 크롤링 (페이지 리스트 만큼)
for btn in range(len(next_btn))[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
    
    gage_list = driver.find_elements(By.CSS_SELECTOR, 'li.UEzoS')
    names = driver.find_elements(By.CSS_SELECTOR, '.place_bluelink')  # (3) 가게명
    types = driver.find_elements(By.CSS_SELECTOR, '.KCMnt')  # (4) 가게 유형

    temp_index = 1 # 현 페이지 내 가게 인덱스 변수
    for data in range(len(gage_list)):  # 가게 리스트 만큼
        print(data)

        sleep(1)
        try:
            
            # (3) 가게이름 가져오기
            title = names[data].text
            print(title)

            # (4) 유형
            category = types[data].text
            print(category)
            
            # 상세페이지로 이동
            button_tmp = '#_pcmap_list_scroll_container > ul > li:nth-child('+ str(temp_index) +') > div.CHC5F > a > div > div > span.place_bluelink.TYaxT'
            driver.find_element(By.CSS_SELECTOR, button_tmp).click()

            # 로딩 기다리기
            sleep(1)

            # 상세페이지로 프레임 전환
            switch_frame('entryIframe')

            # 별점
            try: 
                score = driver.find_element(By.CSS_SELECTOR, '.LXIwF').text
                score_num = float(re.findall("\d+.\d+",score)[0]) # 데이터에서 별점만 추출
                print(score_num)
            except:
                score_num = ""
                print("별점 없음")

            # 가게 설명글
            try: 
                descript = driver.find_element(By.CSS_SELECTOR, 'div.XtBbS').text.strip("'\"")
                descript = descript.replace("\n", " ") # 중간에 있는 엔터 없애기
                print(descript)
            except:
                descript = ""
                print("가게설명 없음")

            
            # 스크롤
            page_down(10)
            sleep(5)

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
            
            # 리뷰 탭으로 이동
            driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div.place_fixed_maintab.place_stuck.place_tab_shadow > div > div > div > div > a:nth-child(5) > span').click()

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

            # dict에 데이터 집어넣기
            dict_temp = {
                'name': title,
                'rating' : score_num,
                'type': category,
                
            }

            parking_dict['가게데이터'].append(dict_temp)
            print(f'{title} ...완료')

            sleep(1)

        except Exception as e:
            print(e)
            print('ERROR!' * 3)

            # dict에 데이터 집어넣기
            dict_temp = {
                'name': title,
                'rating' : score_num,
                'type': category,
                
            }

            parking_dict['가게데이터'].append(dict_temp)
            print(f'{title} ...완료')

            sleep(1)
    
        switch_frame('searchIframe')
        temp_index = temp_index + 1 # 가게 인덱스 +1

    # 다음 페이지 버튼 누를 수 없으면 종료
    if not next_btn[-1].is_enabled():
        break

    if names[-1]:  # 마지막 주차장일 경우 다음버튼 클릭
        next_btn[-1].click()
        sleep(2)
    else:
        print('페이지 인식 못함')
        break

print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을 닫는다.

fields = ['name', 'parking_type', 'road_address', 'jibun_address']

# json 파일로 저장
with open('./store_data.json', 'w', encoding='utf-8') as f:
    json.dump(parking_dict, f, indent=4, ensure_ascii=False)
