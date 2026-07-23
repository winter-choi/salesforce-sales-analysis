# Salesforce Sales Strategy Analysis

Pandas/matplotlib를 활용한 Salesforce 오퍼튜니티 데이터 분석 및 시각화 연습 프로젝트.

## 내용

- `analysis.py` — CSV 데이터 로드, 결측치 처리, 파이프라인/리드소스/단계별 매출 분석, 승률 계산
- `report1784771313929.csv` — 원본 오퍼튜니티 데이터
- `sales_strategy_dashboard.png` — Executive Dashboard 출력물

## 주요 분석

- Total Pipeline / Average Deal Size
- Stage별 매출 및 기회 수
- Lead Source별 매출 및 승률
- Stage x Lead Source 매출 히트맵
- Executive Dashboard (KPI 카드 + 4분할 차트)

## 실행

```bash
pip install pandas matplotlib
python analysis.py
```
