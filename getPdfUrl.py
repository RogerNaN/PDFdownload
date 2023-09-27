import requests
from bs4 import BeautifulSoup

# 指定Google學術搜索的網址
url = 'https://scholar.google.com.tw/scholar?hl=zh-TW&as_sdt=0,5&q=%22solar+system%22'

# 發送GET請求以獲取網頁內容
response = requests.get(url)

# 確認請求成功
if response.status_code == 200:
    # 使用Beautiful Soup解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 解析HTML頁面後，尋找所有的<a>元素
    links = soup.find_all('a', href=True)

    # 遍歷每個<a>元素，提取PDF檔的連結
    pdf_links = []
    for link in links:
        href = link.get('href')
        if href and 'pdf' in href:
            pdf_links.append(href)

    # 打印PDF檔的連結
    for pdf_link in pdf_links:
        print(pdf_link)
else:
    print('無法訪問該網頁。')
