### KoBERT.ipynb
- SKTBrain에서 개발한 KoBERT 모델 사용
- Hugging Face에서 모델 다운로드
- 기존 csv 파일을 tsv 파일로 변환 후 모델에 적용 (review_train.tsv, review_test.tsv)
- 결과 : 과적합 문제는 여전하고, 낮은 성능을 보임
  ||accuracy|f1|
  |---|---|---|
  |valid|0.8350|0.7931|  
  |test|0.26|0.2618|
---
### KoGPT2.ipynb
- Hugging Face에서 모델 다운로드
- KoBERT 보다는 나은 성능을 보임
  ||accuracy|f1|
  |---|---|---|
  |valid|0.8374|0.8337|
  |test|0.2975|0.2941|
---
### LSTM_tuning.ipynb
- 실험노트 7.1.2
- batch_size=32, epoch=10, learning_rate=0.001
- AdamW 옵티마이저 사용, weight_decay=1e-4
- nn.LSTM의 dropout=0.4, 가중치 초기화 적용
- 완전연결층 전 Tanh 활성화함수와 nn.Dropout(0.5) layer 추가
  ||accuray|loss|
  |---|---|---|
  |valid|0.9546|0.2338|
  |test|0.3775|1.7499|
---
### ML.ipynb
- 10개의 머신러닝 모델 베이스라인
- CatBoost와 Voting에서 성능이 좋음 : f1-score 0.35 이상
- Gaussian NaiveBayes 모델에서 과적합이 가장 심하게 나타남
![image](https://github.com/user-attachments/assets/09254833-651d-467a-9d3b-debc7b1e826b)
---
### ML_tuning.ipynb
- SVC, XGB를 중심으로 튜닝 진행한 결과
- SVC : 실험노트 1.3.0
  ||accuracy|f1|loss|
  |---|---|---|---|
  |valid|0.9384|0.9362|1.8106|
  |test|0.395|0.3823|2.3256|
- XGB : 실험노트 3.7.2
  ||accuracy|f1|loss|
  |---|---|---|---|
  |valid|0.8325|0.8248|1.9071|
  |test|0.3675|0.3637|2.3442|
---
