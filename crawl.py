import requests
import json
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import urlopen
from typing import List



def get_news(keyword: str) -> List:
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
    headers = {
                    "authority": "apis.naver.com",
                    "method": "GET",
                    "scheme": "https",
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "referer": "https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid=014&aid=0004796402",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
                }
    
    req = requests.get(url_list, headers=headers)
    print(req.text)
    
    
    # except:
    #     page = urlopen(url_list)
    #     page_encode = page.read().decode('cp949')
    #     print(page_encode)  
  
def main():
    scrap_and_parse()
    
    
    
if __name__ == '__main__':
    main()





# url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220217154255&_callback=jQuery1124029040860222038956_1646227945222&lang=ko&country=KR&objectId=news014,0004796402&categoryId=&pageSize=19192&indexSize=&groupId=&listType=OBJECT&pageType=more&page=1&refresh=true&sort=FAVORITE&includeAllStatus=true&_={s14}'
# # url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220217154255&_callback=jQuery112406935308254980357_1646572243606&lang=ko&country=KR&objectId=news014,0004796402&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=1&refresh=true&sort=FAVORITE&includeAllStatus=true&_=1646572243609'

# headers = {
#     "authority": "apis.naver.com",
#     "method": "GET",
#     "scheme": "https",
#     "accept": "*/*",
#     "accept-encoding": "gzip, deflate, br",
#     "referer": "https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid=014&aid=0004796402",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
# }


# res = requests.get(url, headers=headers)
# print(res)
# print(res.text)

# jquery = res.text[res.text.find("(")+1:-2]
# jquery = json.loads(jquery)
# commentList = jquery["result"]["commentList"]
# print(commentList)


# print(len(commentList))
# for comment in commentList:
#     print(comment['contents'])