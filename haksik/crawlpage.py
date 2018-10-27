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
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import sys
import shutil


def find_table(source):
    """
    id가 'contents'인 <div>를 찾고 <table>을 찾아 반환한다.
    bytes 타입 매개변수를 받아 bs4.element.Tag 타입 변수를 return한다.
    
    """
    soup = BeautifulSoup(source, 'lxml')
    contents_div = soup.find(id='contents')
    target_table = contents_div.find('table')
    return target_table

def parse_table(target_table):
    """
    <table>에서 escape sequence를 최소한으로 줄인다.
    bs4.element.Tag 타입 매개변수를 받아 str 타입 변수를 return한다.

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
    str 타입 매개변수를 받아 list 타입 변수를 return한다.
    
    """
    temp_list = temp_str.split('\t')
    origin_list = []
    for i in range (len(temp_list)):
        if temp_list[i]:
            origin_list.append(temp_list[i]+'\r\r')
    return origin_list

def go_crawl():
    """
    페이지 주소의 html 파일을 read하고 이 모듈의 함수들을 실행한다.
    함수들을 실행하는 데 필요한 매개변수 등은 해당 함수 docstring에 기재했다.
    함수들의 호출이 모두 끝나면 파일을 닫고 종료한다.
    
    """
    if os.path.exists('weekMeal.txt'):
        shutil.copy('weekMeal.txt', 'weekMeal_copy.txt')
        os.remove('weekMeal.txt')
    url = 'http://www.duksung.ac.kr/life/foodmenu/index.jsp?' \
            'cafeId=CID01&weekFlag=1&startDate=20181029&endDate=20181102&' \
            'cafeName=%C7%D0%BB%FD%BD%C4%B4%E7&categoryCnt=1&cafeFlag='
    out_fp = open('weekMeal.txt', 'w', encoding='utf-8') 
    try:
        html = urlopen(url)
        source = html.read()
        html.close()
    except:
        out_fp.close()
        shutil.copy('weekMeal_copy.txt', 'weekMeal.txt')
        sys.exit()
    target_table = find_table(source)
    temp_str = parse_table(target_table)
    origin_list = get_clean_list(temp_str)
    for line in origin_list:
        out_fp.writelines(line)
    out_fp.close()


if __name__ == '__main__':
    go_crawl()
