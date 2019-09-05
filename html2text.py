import requests
import pandas as pd
from bs4 import BeautifulSoup

def convert(url):
    html=requests.get(url).text
    soup=BeautifulSoup(html,"html.parser")
    #print(soup.prettify)

    for script in soup(["script", "style"]):
        script.decompose()
    #print(soup)

    text=soup.get_text()
    #print(text)

    lines= [line.strip() for line in text.splitlines()]

    #lines=[]
    #for line in text.splitlines():
    #  lines.append(line.strip)
    #print(lines)

    text="\n".join(line for line in lines if line)
    print(text)
    f = open("scraping.txt", "a", encoding="utf-8")
    f.writelines(text)