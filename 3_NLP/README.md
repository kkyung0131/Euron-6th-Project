### NLP_test.ipynb

- 새롭게 크롤링한 데이터 중 400개를 랜덤하게 뽑아,
  데이터 전처리 + 데이터 정제 + 맞춤법 교정을 진행한 코드
- 최종 test dataset : review_test.csv (400,2)

### NLP_train.ipynb

- 기존 데이터 전처리 + 데이터 정제 + 맞춤법 교정
- Back Translation(번역 후 재번역)과 Easy Data Augmentation을 진행하여 불균형 해소한 코드
- 최종 train dataset : review_train.csv (2026,2)
  (이 파일에서 train/valid 나누어 성능 검증하시면 됩니다.)
