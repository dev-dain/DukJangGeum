"""
웹페이지의 소스코드를 읽어 파싱 후 텍스트 파일에 저장한다.

사용 변수 목록
url (str)
out_fp (_io.TextIOWrapper)
html (http.client.HTTPResponse)
source (bytes)
soup (bs4.BeautifulSoup)
contents_div (bs4.element.Tag)
target_table (bs4.element.Tag)
temp_str (str)
temp_list (list)
origin_list (list)
i (int)
line (str)

"""
# Import
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import sys


# Function
def find_table(source):
    """
    id가 'contents'인 <div>를 찾고 <table>을 찾아 반환한다.
    prm type: bytes, return type: bs4.element.Tag

    """
    soup = BeautifulSoup(source, 'lxml')
    contents_div = soup.find(id='contents')
    target_table = contents_div.find('table')
    return target_table

def parse_table(target_table):
    """
    <table>에서 escape sequence를 최소한으로 줄인다.
    prm type: bs4.element.Tag, return type: str

    """
    temp_str = target_table.get_text()
    temp_str = temp_str.strip('\n')
    temp_str = temp_str.replace('\t', '')
    temp_str = temp_str.replace('\n', '\t')
    temp_str = temp_str.replace('\r', '\n')
    return temp_str

def get_clean_list(temp_str):
    """
    temp_str을 리스트에 넣고, 비어있지 않은 것을 최종 리스트에 append한다.
    prm type: str, return type: list
    
    """
    temp_list = temp_str.split('\t')
    # temp_list에서 빈 element를 제외한 나머지를 리스트에 넣어 return
    return [tmp+'\r\r' for tmp in temp_list if tmp]

def go_crawl():
    """
    페이지 주소의 html 파일을 read하고 이 모듈의 함수들을 실행한다.
    함수들을 실행하는 데 필요한 매개변수 등은 해당 함수 docstring에 기재했다.
    함수들의 호출이 모두 끝나면 파일을 닫고 종료한다.
    
    """
    if os.path.exists('weekMeal.txt'):
        os.remove('weekMeal.txt')
    
    url = 'http://www.duksung.ac.kr/life/foodmenu/index.jsp?'
    out_fp = open('weekMeal.txt', 'w', encoding='utf-8') 
    
    try:
        html = urlopen(url)
        source = html.read()
        html.close()
    except:
        out_fp.close()
        sys.exit()
    
    target_table = find_table(source)
    temp_str = parse_table(target_table)
    origin_list = get_clean_list(temp_str)
    
    for line in origin_list:
        out_fp.writelines(line)
    out_fp.close()

# Main
if __name__ == '__main__':
    go_crawl()
