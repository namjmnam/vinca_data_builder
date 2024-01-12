# Vinca Data Builder

## 개요
본 프로젝트는 오브젝트 파일(.obj)을 그리드화 및 인덱스 좌표화하는 프로젝트입니다.

## 설명
run.py: 메인 실행파일

obj_raycasting.py: .obj 확장자명에 raycasting 알고리즘으로 좌표 그리드 생성 후 .csv 파일로 저장

coord_to_index.py: 좌표 그리드 DataFrame을 입력받아 인덱스 좌표 .csv 파일로 저장

map_to_xlsx.py: 인덱스 좌표 DataFrame을 입력받아 최상단 한 면을 매핑하여 .xlsx 파일로 시각화

## 예시
### 예시 입력 파일
cone.obj

cone.mtl

### 예시 출력 파일
output_coord.csv

output_index_coord.csv

output_map.xlsx

## 사용법
1. run.py 실행
2. .obj 파일 선택
3. 좌표 범위 및 그리드 밀도 설정
4. 좌표 그리드 .csv 출력파일 저장
5. 인덱스 좌표 .csv 출력파일 저장
6. 매핑 .xlsx 출력파일 저장