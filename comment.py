from collections import defaultdict
import requests
import json
import time
from bs4 import BeautifulSoup
from urllib import parse
from typing import List



def get_news(keyword: str) -> List:
    """Get news list enclose the keyword
    
    param: str = keyword 
    return: List
    """
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
    
    # print(url_list)
    return url_list

def scrap_and_parse(url_list):
    """url 이동 후 댓글 스크랩 후 파싱

    Args:
        url_list (List): 기사 리스트
    """
    for url in url_list:
        url_id = url.split("aid=")[-1]
        # print(url_id)
        link = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220313225543&_callback=jQuery1124029040860222038956_1646227945222&lang=ko&country=KR&objectId=news014,0004796402&categoryId=&pageSize=30000&indexSize=&groupId=&listType=OBJECT&pageType=more&page=&refresh=true&sort=FAVORITE&includeAllStatus=true&_={url_id}"

        headers = {
            "authority": "apis.naver.com",
            "method": "GET",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "referer": f"https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid=014&aid={url_id}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        }

        res = requests.get(link, headers=headers)
        jquery = res.text[res.text.find("(")+1:-2]
        jquery = json.loads(jquery)
        
        commentList = jquery["result"]["commentList"]
        
        result = defaultdict(list)

        for comment in commentList:
            if comment["contents"]:
                result[link].append(comment["contents"])

        print(result)
        time.sleep(1)
        

  
def main():
    url_list = get_news("국토부")
    scrap_and_parse(url_list)

    
if __name__ == '__main__':
    main()




