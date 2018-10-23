import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, Comment
import re
import os

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get("https://en.wikibooks.org/wiki/Java_Programming")
baseurl = 'https://en.wikibooks.org'

page_html = driver.page_source
soup = BeautifulSoup(page_html,'html.parser')

data = soup.find("div", class_="mw-parser-output")

print(os.getcwd())

links_of_interest = []

list_h3 = data.find_all('h3')
list_ul = data.find_all('ul')

for h3 in list_h3:
    if h3.find('a') is not None:
        links_of_interest.append(baseurl + h3.find('a')['href'])

for ul in list_ul:
    li_list = ul.find_all('li')
    for li in li_list:
        a_list = li.find_all('a')
        if len(a_list)==2 and a_list[-1]['href'] is not None:
            links_of_interest.append(baseurl + a_list[-1]['href'])

print("---------------------")
print(len(links_of_interest))
for link in links_of_interest:
    print(link)
'''
fileName= os.getcwd() + "\\" + soup.find('h1', {'class': 'firstHeading'}).text + ".txt"
fileContent = ""
file = open(fileName, 'w+')

for i in data:

    string_i = str(i)
    if string_i[0:2]=='<h' and i.find("span").text!='':
        file.close()
        fileName = os.getcwd() + "\\" + i.find("span").text +  ".txt"
        fileContent = ""
        file = open(fileName, 'w+')
    elif string_i[0:3]=='<p>':
        file.write(str(i.text) + " ")
    elif string_i[0:3]=='<ta' and i.has_attr('class') and i['class'][0] in ["wikitable", "noprint", "metadata", "topicon", "notice", "notice-todo"]:
        pass
    elif string_i[0:3]=='<ta':
        file.write(str(i.text) + " ")
    elif string_i[0:2]=='<d':
        file.write(str(i.text) + " ")

file.close()
'''
