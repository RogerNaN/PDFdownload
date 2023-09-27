import PyPDF2
import sys

isDouble = 0


def is_double_column_page(page):
    global isDouble
    text = page.extract_text()
    lines = text.split('\n')

    # 判斷是否為雙欄式文章
    if len(lines) > 100:
        isDouble += 1
    else:
        isDouble -= 1


def check_pdf_for_double_column(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                is_double_column_page(page)
    except Exception as e:
        print(f"Error: {str(e)}")


pdf_path = r'C:\Users\ACER\Desktop\setPDF\pdf_files\paper_2.pdf'
sys.stdout.reconfigure(encoding='utf-8')
check_pdf_for_double_column(pdf_path)
if isDouble < 0:
    print("(X)不是雙欄式文章")
else:
    print("(O)是雙欄式文章")
