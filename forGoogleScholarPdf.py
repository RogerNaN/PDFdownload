import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import os

# 创建用于保存PDF和文本文件的文件夹
pdf_folder = 'pdf_files'
text_folder = 'text_files'

os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(text_folder, exist_ok=True)

# 获取PDF文件的链接


def get_pdf_links():
    #url = 'https://scholar.google.com.tw/scholar?hl=zh-TW&as_sdt=0,5&q=%22solar+system%22&scisbd=1'
    url = 'https://www.odyssee-mure.eu/publications/national-reports/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        pdf_links = []
        for link in links:
            href = link.get('href')
            if href and href.endswith('.pdf'):
                if not href.startswith('http'):
                    href = 'https://www.odyssee-mure.eu' + href
                pdf_links.append(href)

        return pdf_links
    else:
        print('无法访问该网页。')
        return []

# 下载并处理PDF文件


def process_pdf(url_file, output_filename):
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html, application/xhtml+xml, application/xmlq = 0.9, image/webp, image/apng, */*q = 0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    req = requests.get(url_file, headers=send_headers)

    if req.headers.get('content-type') == 'application/pdf':
        bytes_io = io.BytesIO(req.content)

        output_pdf_path = os.path.join(pdf_folder, output_filename)
        with open(output_pdf_path, 'wb') as pdf_file:
            pdf_file.write(bytes_io.getvalue())

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


if __name__ == '__main__':
    pdf_links = get_pdf_links()

    if pdf_links:
        for i, link in enumerate(pdf_links):
            filename = f'paper_{i+1}.pdf'
            process_pdf(link, filename)
