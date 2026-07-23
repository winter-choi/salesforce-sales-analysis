# Tableau Public 대시보드 만들기 가이드

`report1784771313929.csv` 로 Streamlit 대시보드와 동일한 분석을 Tableau로 재현하는 단계별 가이드.

## 1. 설치 및 연결

1. https://public.tableau.com/en-us/s/download 에서 Tableau Public 설치 (무료, 가입 필요)
2. 실행 후 **Connect > Text File** → `report1784771313929.csv` 선택
3. 인코딩은 UTF-8, 첫 행을 헤더로 인식하는지 확인

## 2. 필드 정리

| 원본 컬럼 | 역할 | 비고 |
|---|---|---|
| Amount | Measure (숫자) | 통화 형식으로 지정 |
| Stage | Dimension | Closed Won/Lost 포함 |
| LeadSource | Dimension | 결측치는 "Unknown"으로 그룹핑 |
| CloseDate | Dimension (날짜) | Data type을 Date로 변경 |
| AccountName, OpportunityName | Dimension | |

계산 필드 추가 (Analysis > Create Calculated Field):

- **Is Won**: `IF [Stage] = "Closed Won" THEN 1 ELSE 0 END`
- **Is Closed**: `IF [Stage] IN ("Closed Won", "Closed Lost") THEN 1 ELSE 0 END`
- **Win Rate**: `SUM([Is Won]) / SUM([Is Closed])` → 서식을 퍼센트로 지정

## 3. 시트(Worksheet) 만들기

Streamlit 버전과 동일한 구성으로 6개 시트를 만듭니다.

1. **Revenue by Stage** — Rows: Stage, Columns: SUM(Amount), 가로 막대
2. **Revenue by Lead Source** — Rows: LeadSource, Columns: SUM(Amount)
3. **Opportunity Count by Stage** — Rows: Stage, Columns: CNT(OpportunityName)
4. **Average Deal Size by Lead Source** — Rows: LeadSource, Columns: AVG(Amount)
5. **Revenue Heatmap (Stage x LeadSource)** — Rows: Stage, Columns: LeadSource, Color: SUM(Amount) → Marks type: Square/Heatmap
6. **Win Rate by Lead Source** — Rows: LeadSource, Columns: Win Rate (텍스트 테이블 또는 막대)

KPI 숫자 카드(Total Pipeline, Win Rate, Average Deal Size, Total Opportunities)는 각각 텍스트 전용 시트로 만들어 큰 폰트로 표시하면 Streamlit의 `st.metric` 카드와 비슷한 효과를 냅니다.

## 4. 대시보드 조립

1. New Dashboard, 크기는 Automatic 또는 1600x1000 고정
2. 상단에 KPI 카드 4개를 가로로 배치
3. 2x2 그리드로 4개 막대 차트 배치
4. 하단에 히트맵 + Win Rate 테이블 배치
5. **Filter**: LeadSource 시트에 필터 액션 추가 → Dashboard 우측에 필터 카드로 노출 (Streamlit 사이드바 필터와 동일한 역할)

## 5. 게시 (Publish)

1. Server > Tableau Public > Save to Tableau Public As...
2. 로그인 후 대시보드 제목을 `Salesforce Sales Strategy Dashboard`로 저장
3. 게시되면 공개 링크가 생성됨 → GitHub README에 링크 추가 권장

## 6. 인터뷰에서 언급할 포인트

- Streamlit(Python 코드형) vs Tableau(비주얼 BI 툴)로 동일한 분석을 두 가지 방식으로 구현했다는 점 → 기술 스택 유연성 어필
- Win Rate, Stage별 파이프라인, Lead Source ROI 같은 핵심 세일즈 지표를 스스로 정의하고 계산했다는 점 강조
