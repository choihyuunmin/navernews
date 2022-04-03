import sys
import requests
import json
import time
import logging
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib import parse
from typing import List

from database import Base
from database import engine
import models


Base.metadata.create_all(bind=engine)


class Logger:
    def __init__(self, pid:bool = False):
        self.logger = logging.getLogger("logger")
        self.filename = f"./log/APPLOG_{datetime.datetime.now():%Y/%m/%d/%H:%M}.log"
        self.pid = pid
        self.file_handler = None
    
    def setLogger(self):
        if self.file_handler:
            self.logger.removeHandler(self.file_handler)

        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s] : %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        self.file_handler = logging.FileHandler(self.filename, mode='a')
        self.file_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)


class Crawler:
    def __init__(self):
        self.headers = {
                        "authority": "apis.naver.com",
                        "method": "GET",
                        "scheme": "https",
                        "accept": "*/*",
                        "accept-encoding": "gzip, deflate, br",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
                    }
        self.log = Logger()
        self.logger = self.log.logger


    def get_news(self, keyword: str) -> List:
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
        
        self.logger.info(url_list)
        return url_list


    def scrap(self, url: str):
        """Go into Url and Get articles title and comment"""
        try:   
            title = requests.get(url, headers=self.headers)
            bs = BeautifulSoup(title.text, "lxml")
            title = bs.find("h3", attrs={"id":"articleTitle"}).text
            logging.debug(title)
            
            pre_url = url.split("oid=")[1].split("&")
            url_oid = pre_url[0]
            url_id = pre_url[1].split("aid=")[-1]

            link = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220313225543&_callback=jQuery1124029040860222038956_1646227945222&lang=ko&country=KR&objectId=news{url_oid}%2C{url_id}&categoryId=&pageSize=30000&indexSize=&groupId=&listType=OBJECT&pageType=more&page=&refresh=true&sort=FAVORITE&includeAllStatus=true&_={url_id}"
            self.headers["referer"] = f"https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid={url_oid}&aid={url_id}"
            res = requests.get(link, headers=self.headers)
            jquery = res.text[res.text.find("(")+1:-2]
        except:
            AttributeError("DOCUMENT FORMAT IS INCORRECT")

        return title, jquery


    def parsing(self, title: str, jquery: str):
        """parsing comment by title"""

        jquery = json.loads(jquery)
        commentList = jquery["result"]["commentList"]
        
        result = defaultdict(list)
        for comment in commentList:
            if comment["contents"]:
                result[title].append(comment["contents"])
        time.sleep(1)
        return result
            

    
    def main(self):
        url_list = self.get_news(sys.argv[1])

        print(url_list)
        for url in url_list:
            title, jquery = self.scrap(url)
            result = self.parsing(title, jquery)
            self.logger.info(result)
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please input keyword")

    crawler = Crawler()
    crawler.main()
    



