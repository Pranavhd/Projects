import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, Comment
import re
import os

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get("https://en.wikibooks.org/wiki/Java_Programming/Object_Lifecycle")

page_html = driver.page_source
soup = BeautifulSoup(page_html,'html.parser')

data = soup.find("div", class_="mw-parser-output")

print(os.getcwd())

fileName= os.getcwd() + "\\" + soup.find('h1', {'class': 'firstHeading'}).text + ".txt"
fileContent = ""
file = open(fileName, 'w+')

for i in data:
    #print(i,type(i),str(i)[0:3])
    #print("--------------------")

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
    if tr>10:
        break
    tr += 1
    if "\n" != i and "\n\n" != i and "\n\n\n" != i and "\n\n\n\n" != i and "<br>" != i and not isinstance(i, Comment):
        if i.has_attr('class') and i['class'][0] in ["wikitable", "noprint", "metadata", "topicon", "notice", "notice-todo"]:
            pass
        else:
            #print(i.text)
            pass
'''

