import sys
import requests
import json
import time
import logging
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib import parse
from typing import List



logging.basicConfig(
    format='[%(asctime)s][%(levelname)s] : %(message)s',
    datefmt='%Y-%m-%d %I:%M:%S',
    level=logging.DEBUG
)

headers = {
    "authority": "apis.naver.com",
    "method": "GET",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}

def get_news(keyword: str) -> List:
    """Get news list enclose the keyword """

    keyword = parse.quote(keyword)
    url_list = []
    for i in range(1, 101, 10):
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&start={i}"
        req = requests.get(url)
        bs = BeautifulSoup(req.text, "lxml")

        links = bs.find_all("a", {"class":"info"})

        for link in links:
            if link.get_text() == "네이버뉴스":
                url_list.append(link["href"])
    
    logging.info(url_list)
    return url_list


def scrap(url: str):
    """Go into Url and Get articles title and comment"""

    global headers
    try:   
        title = requests.get(url, headers=headers)
        bs = BeautifulSoup(title.text, "lxml")
        title = bs.find("h3", attrs={"id":"articleTitle"}).text
        logging.debug(title)
        
        pre_url = url.split("oid=")[1].split("&")
        url_oid = pre_url[0]
        url_id = pre_url[1].split("aid=")[-1]

        link = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220313225543&_callback=jQuery1124029040860222038956_1646227945222&lang=ko&country=KR&objectId=news{url_oid}%2C{url_id}&categoryId=&pageSize=30000&indexSize=&groupId=&listType=OBJECT&pageType=more&page=&refresh=true&sort=FAVORITE&includeAllStatus=true&_={url_id}"
        headers["referer"] = f"https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid={url_oid}&aid={url_id}"
        res = requests.get(link, headers=headers)
        jquery = res.text[res.text.find("(")+1:-2]

    except:
        AttributeError("DOCUMENT FORMAT IS INCORRECT")

    return title, jquery


def parsing(title: str, jquery: str):
    """parsing comment by title"""

    jquery = json.loads(jquery)
    commentList = jquery["result"]["commentList"]
    
    result = defaultdict(list)
    for comment in commentList:
        if comment["contents"]:
            result[title].append(comment["contents"])
        logging.info(result)
    time.sleep(1)
    return result
        

  
def main():
    url_list = get_news(sys.argv[1])

    print(url_list)
    for url in url_list:
        title, jquery = scrap(url)
        result = parsing(title, jquery)
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please input keyword")

    main()
    



