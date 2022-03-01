import requests
import json
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import urlopen






def get_news(keyword: str) -> list:
    '''
    Get news list enclose the keyword
    
    param: keyword 
    return: list
    '''
    keyword = parse.quote(keyword)
    url_list = []
    for i in range(1, 101, 10):
        url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&start={i}'
        req = requests.get(url)
        bs = BeautifulSoup(req.text, "lxml")

        links = bs.find_all("a", {"class":"info"})

        for link in links:
            if link.get_text() == '네이버뉴스':
                url_list.append(link["href"])
                
    return url_list

  
def scrap_and_parse():
    url_list = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=101&oid=001&aid=0013007145'
    try:
        req = requests.get(url_list)
        print(req.text)
    
    except:
        page = urlopen(url_list)
        page_encode = page.read().decode('cp949')
        print(page_encode)  
  
def main():
    scrap_and_parse()
    
    
    
if __name__ == '__main__':
    main()