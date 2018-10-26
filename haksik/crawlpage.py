'''
이 모듈은 식단 웹페이지의 정보를 BeautifulSoup로 가져와
필요한 정보인 텍스트만 가져오는 필터링 작업을 거쳐
txt 파일에 저장합니다.

사용 변수 목록
out_fp (_io.TextIOWrapper)
html (http.client.HTTPResponse)
source (bytes)
soup (bs4.BeautifulSoup)
contents_table (bs4.element.Tag)
target_table (bs4.element.Tag)
temp_str (str)
temp_list (list)
origin_list (list)
i (int)
line (str)

'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import os


if os.path.exists('weekMeal.txt') :
    os.remove('weekMeal.txt')

out_fp = open('weekMeal.txt', 'w', encoding='utf-8')
html = urlopen('http://www.duksung.ac.kr/life/foodmenu/index.jsp')
source = html.read()
html.close()

soup = BeautifulSoup(source, 'lxml')
contents_table = soup.find(id='contents')
target_table = contents_table.find('table')

temp_str = target_table.get_text()
temp_str = temp_str.strip('\n')
temp_str = temp_str.replace('\t', '')
temp_str = temp_str.replace('\n', '\t')
temp_str = temp_str.replace('\r', '\n')

temp_list = temp_str.split('\t')
origin_list = []

for i in range (len(temp_list)) :
    if temp_list[i] :
        origin_list.append(temp_list[i])

for line in origin_list :
    out_fp.writelines(line+'\r\r')

out_fp.close()
