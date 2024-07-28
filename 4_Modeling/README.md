### KoBERT 
- SKTBrain에서 개발한 KoBERT 모델 사용
- Hugging Face에서 모델 다운로드
- 기존 csv 파일을 tsv 파일로 변환 후 모델에 적용 (review_train.tsv, review_test.tsv)
- 결과 : 과적합 문제는 여전하고, 낮은 성능을 보임
  
  ||accuracy|f1|
  |---|---|---|
  |valid|0.8350|0.7931|  
  |test|0.26|0.2618|  
