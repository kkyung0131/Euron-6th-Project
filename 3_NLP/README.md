### csv 파일 설명

[ cleaned_review_data.csv ]  
기존 전처리 파일에서 필요없는 변수를 제거 : 'clean_reviews', 'keyword2'   
데이터 정제 보완 : 한글과 공백 빼고 모두 제거

  
[ spell_data.csv ]  
clean_reviews에 대해 맞춤법 교정 수행 : [spell_reviews, keyword2] 

  
[ Back_Translation_data.csv ]  
데이터 번역 후 재번역을 통해서 불균형을 어느정도 해소한 데이터셋  
value_counts가 9 미만인 label(keyword2)은 제거함  
'bt_reviews', 'keyword2'

  
[ eda_data.csv ]  
Easy Data Augmentation(RS,RD)로 2차적으로 불균형 해소한 데이터셋  
해당 데이터로 이후 토큰화, 벡터화 및 모델 학습 진행  
'bt_reviews', 'keyword2'

※ train/test를 나누지 않고 데이터 증강을 진행하였습니다.  
따로 test dataset을 구축하거나, train/test로 나눈 후 다시 처음부터 데이터 증강을... (😭)

---

### ipynb 파일 설명

NLP-(1).ipynb : 음식점/카페/주점으로 나누어 각각 기본 자연어처리를 진행한 코드

NLP-(2).ipynb : Back Translation과 Easy Data Augmentation을 진행한 코드

NLP-(3).ipynb : eda_data를 가지고 여러 자연어처리 방법의 성능을 비교한 코드



