# 가상화폐 시세 추이 프로젝트
이 프로젝트는 가상화폐의 실시간 시세를 추적하고 시세 추이를 시각화하는 웹 애플리케이션입니다. Bithumb API를 사용하여 가상화폐 시세 데이터를 수집하고, 전처리 후 Redis에 적재한 뒤, Streamlit과 Altair를 활용하여 데이터를 시각화하였습니다.


### 프로젝트 구성 요소

- main.py: Streamlit을 사용하여 웹 애플리케이션을 구축하는 메인 스크립트입니다.
- DataHandler.py: 데이터 핸들링을 위한 함수들이 포함된 모듈입니다.

### Python 및 주요 라이브러리 버전
Python 3.9.13
pandas 1.5.0
redis 4.5.5
streamlit 1.23.1
altair 5.0.1


### 실행 방법
1. 저장소를 클론합니다

```
git clone https://github.com/your-repo.git
```

2. 라이브러리 및 Python main.py 스크립트를 실행합니다

```
python -m streamlit run main.py
```

3. 웹 브라우저에서 http://localhost:8501로 접속하여 가상화폐 시세 추이를 확인합니다.


### Layout

![image](https://github.com/ScrewlessKingjo/Redis_Project/assets/92324214/7d4d2ee2-04d6-4c37-b738-164a1f0be0cc)

- 웹 애플리케이션은 가상화폐 시세 추이를 실시간으로 업데이트하여 보여줍니다.
- 각 가상화폐의 현재가 정보에 대한 테이블을 볼 수 있습니다.
- 최근 호가 정보를 바탕으로, 가상화폐 별 평균 매도가(빨간색) 평균 매수가(파란색)을 Line Chart로 확인할 수 있습니다.
- 차트와 테이블은 5초 간격으로 업데이트됩니다.
