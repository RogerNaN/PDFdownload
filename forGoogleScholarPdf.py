import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import os
import PyPDF2
import sys
from requests.exceptions import ConnectionError

isDouble = 0


# 獲得PDF url
def get_pdf_links():
    #url = 'https://scholar.google.com.tw/scholar?hl=zh-TW&as_sdt=0,5&q=%22solar+system%22&scisbd=1'
    url = 'https://www.odyssee-mure.eu/publications/national-reports/'
    # url = 'https://scholar.google.com.tw/scholar?hl=zh-TW&as_sdt=0%2C5&q=%22solar+system%22&oq='  # solary system
    #url = 'https://scholar.google.com.tw/scholar?hl=zh-TW&as_sdt=0%2C5&q=%22machine+learning%22&btnG='
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        pdf_links = []
        for link in links:
            href = link.get('href')
            # if href and href.endswith('.pdf'):
            if href and 'pdf' in href:
                if not href.startswith('http'):
                    href = 'https://www.odyssee-mure.eu' + href  # 可依據網站修改
                pdf_links.append(href)
        print('success get PDF URL!')
        # print(pdf_links)
        return pdf_links
    else:
        print('unable to access this website!')
        return []


# 下載PDF並提取內容
def process_pdf(url_file, output_filename):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html, application/xhtml+xml, application/xmlq = 0.9, image/webp, image/apng, */*q = 0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    try:
        req = requests.get(url_file, headers=send_headers)

        if req.headers.get('content-type') == 'application/pdf':
            bytes_io = io.BytesIO(req.content)
            output_pdf_path = os.path.join(pdf_folder, output_filename)
            with open(output_pdf_path, 'wb') as pdf_file:
                pdf_file.write(bytes_io.getvalue())
            #pdf_path = output_filename
            sys.stdout.reconfigure(encoding='utf-8')

            full_pdf_path = os.path.join(pdf_folder, output_filename)
            check_pdf_for_double_column(full_pdf_path)
            if isDouble < 0:
                print(output_filename+"不是雙欄式文章")
            else:
                print(output_filename+"是雙欄式文章")

            pdf = pdfplumber.open(output_pdf_path)
            page_texts = []

            for page in pdf.pages:
                text = page.extract_text()
                page_texts.append(text)

            full_text = "\n".join(page_texts)
            output_text_path = os.path.join(
                text_folder, f'extracted_full_text_{output_filename}.txt')

            with open(output_text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(full_text)

            print(
                f"Full text for '{output_filename}' has been saved to '{output_text_path}'")
        else:
            print(f"The link '{url_file}' does not lead to a valid PDF.")
    except ConnectionError as e:
        print(f"Error: {str(e)} (Connection Error)")


# 計算換行數
def is_double_column_page(page):
    global isDouble
    text = page.extract_text()
    lines = text.split('\n')

    # 判斷是否為雙欄式文章
    if len(lines) > 100:
        isDouble += 1
    else:
        isDouble -= 1


# 判斷是否為雙欄式文章
def check_pdf_for_double_column(pdf_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                is_double_column_page(page)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    working_directory = os.getcwd()

    pdf_folder = os.path.join(working_directory, 'pdf_files')
    text_folder = os.path.join(working_directory, 'text_files')

    os.makedirs(pdf_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)

    pdf_links = get_pdf_links()

    if pdf_links:
        for i, link in enumerate(pdf_links):
            filename = f'paper_{i+1}.pdf'
            process_pdf(link, filename)
