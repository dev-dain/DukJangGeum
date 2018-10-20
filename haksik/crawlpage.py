from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

if os.path.exists('weekMeal.txt') :
    os.remove('weekMeal.txt')

outFp = open('weekMeal.txt', 'w', encoding = 'utf-8')
html = urlopen('http://www.duksung.ac.kr/life/foodmenu/index.jsp?cafeId=CID01&weekFlag=1&startDate=20181015&endDate=20181019&cafeName=%C7%D0%BB%FD%BD%C4%B4%E7&categoryCnt=1&cafeFlag=')
source = html.read()
html.close()

soup = BeautifulSoup(source, 'lxml')
tableDiv = soup.find(id = 'contents')
tables = tableDiv.find('table')

newStr = tables.get_text()
newStr = newStr.strip('\n')
newStr = newStr.replace('\t', '')
newStr = newStr.replace('\n', '\t')
newStr = newStr.replace('\r', '\n')

oldList = newStr.split('\t')
newList = []
for i in range (len(oldList)) :
    if oldList[i]!='' :
        newList.append(oldList[i])

for line in newList :
    outFp.writelines(line+'\r\r')

outFp.close()
