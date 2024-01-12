import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def to_xlsx(merged_df, nx, ny):
    # CSV 파일 읽기
    df = merged_df['P']

    # 재구성을 위한 총 요소 수 계산
    total_elements = nx * ny

    # 데이터가 xy보다 길면 데이터프레임과 인덱스 배열을 잘라냄
    df = df.iloc[:total_elements]

    # 원하는 형태로 데이터프레임 재구성
    reshaped_df = pd.DataFrame(df.values.reshape(ny, nx))

    # 데이터프레임의 행 순서를 뒤집음 (상하반전)
    reshaped_df = reshaped_df.iloc[::-1]

    # Get the script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Open a file dialog to choose file path and name
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                            filetypes=[('XLSX files', '*.xlsx')],
                                            title='Save map file as',
                                            initialfile='output_map',
                                            initialdir=script_directory)

    # Pandas Excel 작성기 생성 (XlsxWriter 엔진 사용)
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # 데이터프레임을 Excel 파일에 쓰기
    reshaped_df.to_excel(writer, index=False, header=False)

    # XlsxWriter 워크북과 워크시트 객체에 접근
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # 1이 있는 셀에 대한 형식 정의
    green_format = workbook.add_format({'bg_color': '#C6EFCE'})

    # 데이터를 순회하며 1이 있는 셀에 형식 적용
    # 바이너리 데이터 대신 인덱스 번호로 셀 채우기
    for i, value in enumerate(df):
        row, col = divmod(i, nx)
        row = ny - 1 - row  # 상하반전을 위한 행 인덱스 조정
        if value == 1:
            worksheet.write(row, col, i + 1, green_format)
        else:
            worksheet.write(row, col, i + 1)

    # 정사각형 셀을 만들기 위해 열 너비와 행 높이 설정
    for i in range(nx):
        worksheet.set_column(i, i, 3)  # 열 너비 설정
        worksheet.set_row(i, 20)       # 행 높이 설정

    # Pandas Excel 작성기를 닫고 Excel 파일 저장
    writer._save()