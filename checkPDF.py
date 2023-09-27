import PyPDF2
import sys

isDouble = 0


def is_double_column_page(page):
    global isDouble  # 声明isDouble为全局变量
    text = page.extract_text()
    lines = text.split('\n')

    # 判断页面文本是否分为两列
    if len(lines) > 100:
        isDouble += 1  # 增加isDouble计数
    else:
        isDouble -= 1  # 减少isDouble计数


def check_pdf_for_double_column(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                is_double_column_page(page)
    except Exception as e:
        print(f"Error: {str(e)}")


pdf_path = 'C:/Users/ACER/Desktop/output/paper_11.pdf'
sys.stdout.reconfigure(encoding='utf-8')
check_pdf_for_double_column(pdf_path)
if isDouble < 0:
    print("不是")
else:
    print("是")
