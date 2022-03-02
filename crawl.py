import requests
import json
from bs4 import BeautifulSoup
from urllib import parse
from urllib.request import urlopen



# def get_news(keyword: str) -> list:
#     '''
#     Get news list enclose the keyword
    
#     param: keyword 
#     return: list
#     '''
#     keyword = parse.quote(keyword)
#     url_list = []
#     for i in range(1, 101, 10):
#         url = f'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&start={i}'
#         req = requests.get(url)
#         bs = BeautifulSoup(req.text, "lxml")

#         links = bs.find_all("a", {"class":"info"})

#         for link in links:
#             if link.get_text() == '네이버뉴스':
#                 url_list.append(link["href"])
                
#     return url_list

# def scrap_and_parse():
#     url_list = 'https://news.naver.com/main/read.naver?mode=LSD&mid=sec&sid1=101&oid=001&aid=0013007145'
#     try:
#         req = requests.get(url_list)
#         print(req.text)
    
#     except:
#         page = urlopen(url_list)
#         page_encode = page.read().decode('cp949')
#         print(page_encode)  
  
# def main():
#     scrap_and_parse()
    
    
    
# if __name__ == '__main__':
#     main()





url = 'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220217154255&_callback=jQuery1124029040860222038956_1646227945222&lang=ko&country=KR&objectId=news014,0004796402&categoryId=&pageSize=1000&indexSize=1000&groupId=&listType=OBJECT&pageType=more&page=100&refresh=false&sort=FAVORITE&current=751091199246336480&prev=751085926435783273&moreParam.direction=next&moreParam.prev=100000n00001805pfhqn7rx5rd&moreParam.next=100000000000005pfjlxif6n6o&includeAllStatus=true&_=1646230184194'


headers = {
    "authority": "apis.naver.com",
    "method": "GET",
    "path": "/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_economy&pool=cbox5&_cv=20220217154255&_callback=jQuery112407773896026507126_1646230184190&lang=ko&country=KR&objectId=news014,0004796402&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=2&refresh=false&sort=FAVORITE&current=751091199246336480&prev=751085926435783273&moreParam.direction=next&moreParam.prev=100000n00001805pfhqn7rx5rd&moreParam.next=100000000000005pfjlxif6n6o&includeAllStatus=true&_=1646230184194",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "cookie": "NNB=L4FZEAQVAHXGC; NaverSuggestUse=use&unuse; ASID=1ba743350000017e9addf5940000004e; _fbp=fb.1.1644037955483.1338212178; _gcl_au=1.1.959263144.1644037956; nid_inf=1970498853; NID_AUT=yCov+g6kGqFd6e2Vc9+v9GjTf/XQYMVGAMdpAFwq5fmWLZ9iHaPg7EipvG0+7cm+; NID_JKL=P1i2KtVU0SQBuO56Za2au8afXKkoRYvWUIcyJ4FBa2E=; _ga=GA1.2.187920163.1643646512; _ga_7VKFYR6RV1=GS1.1.1645071592.1.1.1645071768.60; nx_ssl=2; BMR=s=1646037524550&r=https://n.news.naver.com/article/214/0001181200?cds=news_media_pc&r2=https://news.naver.com/; NID_SES=AAABnJ8C1p3AILNI+AzeqQ/TegeK08CfK4aFiGl83P3us6DNhgsEpqbcGeqDnHZWEj+Kssxuf/f5XEZHYxqiSxeaDsbQ0eiH9h45d4pkBIZ0ZCSlwSqaFmkYrY+KjM/6Ao3m/vLLvDzGnX/D/5YK8NMeABe+t0R74F0bgI5Bqjc6LZBTQA2OmyWsRdj5fjW5HTXymLTiyf0zq3IMc+RIsdSpCNUEM/QcqJ3zyHd4IdFUGnti97m1k6JR100ANfItTk7VJo94Iwd0WBzHFfp8/TpM9LWe3SWNKEzv7ikS9qXFEGGH5Mj+xeIGhmgXifxetdD8U2W+vIi8+Gy2D/qQ8RkxergJ3xwKYMBV5nfQFL2h6GYHWuiHm3zuK7zEx4rBSm5wWgacXpl3mCzHcgFH0sF6sqZ/iqHRtZMuG6vG2qbYXlOPT182FJCsr9eUrbZH4t6NppSaa8eVRpCdJioNUxLpprG9xJnkSOJuJhqw5qQbQvX/3uQtRNWt9kKibuzbXF6fEnspTkA/oA1utxT7zz1UJOBc47T2uxCsPfYOeTku1GS6; _naver_usersession_=VxyH3Niq4pxYo386UeRQNg==; page_uid=hm9I7dprvmZssfnrkKKssssssGl-003544",
    "referer": "https://news.naver.com/main/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=101&oid=014&aid=0004796402",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
}


res = requests.get(url, headers=headers)
print(res)
print(res.text)

jquery = res.text[res.text.find("(")+1:-2]
jquery = json.loads(jquery)
commentList = jquery["result"]["commentList"]
print(commentList)


print(len(commentList))
for comment in commentList:
    print(comment['contents'])