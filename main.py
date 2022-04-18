import sys
import requests
import json
import time
import logging

from datetime import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib import parse
from typing import List

from database import session, Base, engine
from models import Articles, Comments


Base.metadata.create_all(bind=engine)

class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.stream_handler = logging.StreamHandler()
        self.file_handler = logging.FileHandler(filename=f"./log/naver_{datetime.now():%Y%m%d%H%M}.log", encoding='utf-8')

    def set_logger(self):
        self.stream_handler.setLevel(logging.INFO)
        self.file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt="[%(asctime)s][%(levelname)s] %(message)s")

        self.stream_handler.setFormatter(formatter)
        self.file_handler.setFormatter(formatter)
        
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)

        return self.logger



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
        self.logger = Logger()
        self.logger = self.logger.set_logger()

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
        
        return url_list


    def scrap(self, url: str):
        """Go into Url and Get articles title and comment"""
        title = None
        jquery = None
        reg_date = None
        try:   
            title = requests.get(url, headers=self.headers)
            bs = BeautifulSoup(title.text, "lxml")
            title = bs.find("h3", attrs={"id":"articleTitle"})
            if title:
                title = title.text
                reg_date = bs.find("span", attrs={"class":"t11"}).text
                pre_url = url.split("oid=")[1].split("&")
                url_oid = pre_url[0]
                url_id = pre_url[1].split("aid=")[-1]

                link = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220313225543&_callback=jQuery1124029040860222038956_1646227945222&lang=ko&country=KR&objectId=news{url_oid}%2C{url_id}&categoryId=&pageSize=30000&indexSize=&groupId=&listType=OBJECT&pageType=more&page=&refresh=true&sort=FAVORITE&includeAllStatus=true&_={url_id}"
                self.headers["referer"] = f"https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid={url_oid}&aid={url_id}"
                res = requests.get(link, headers=self.headers)
                jquery = res.text[res.text.find("(")+1:-2]
                if "오전" in reg_date:
                    reg_date = reg_date.replace("오전", "AM")
                else:
                    reg_date = reg_date.replace("오후", "PM")
                reg_date = datetime.strptime(reg_date, '%Y.%m.%d. %p %I:%M')
                
                self.logger.info(url)
                self.logger.info(title)
                self.logger.info(reg_date)

        except AttributeError as e:
            self.logger.error(e, "DOCUMENT FORMAT IS INCORRET")
            pass

        except:
            pass

        return title, jquery, reg_date 


    def parsing(self, title: str, jquery: str, reg_date: str, url: str):
        """parsing comment by title"""
    
        jquery = json.loads(jquery)
        commentList = jquery["result"]["commentList"]

        result = defaultdict(list)
        result["title"] = title
        result["url"] = url
        result["reg_date"] = reg_date
        result["comments"] = []
        
        for comment in commentList:
            if comment["contents"]:
                result["comments"].append(comment["contents"])
        self.logger.info(result)
                
        time.sleep(1)
        return result


    def main(self):
        url_list = self.get_news(sys.argv[1])

        for url in url_list:
            title, jquery, reg_date = self.scrap(url)
            add_article = Articles(title=title, url=url, reg_date=reg_date)
            session.add(add_article)
            if jquery:
                result = self.parsing(title, jquery, reg_date, url)
        return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please input keyword")

    crawler = Crawler()
    crawler.main()
    session.commit()