import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser

def getInfo(url):
    header={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
        }

    r = requests.get(url=url, headers=header)
    soup = BeautifulSoup(r.text, 'lxml')
    # get info
    info = {}
    info['title'] = soup.h1.span.text
    infos = soup.find(id='info').find_all('span',attrs={'class':'pl'})
    
    for i in infos:
        if i.text.strip() == '作者':
            info['作者'] = i.next_sibling.next_sibling.text
        elif i.text == '出版社:':
            info['出版社'] = i.next_sibling.next_sibling.text
        else:
            info[i.text.strip().strip(':')] = i.next_sibling.text.strip()

    info['score'] = soup.find(class_='rating_num').text.strip()
    info['cover'] = soup.find(class_='nbg')['href'].strip()

    return info

def createRecord(info,token,database_id, url):

    body = {
        "parent": { "type": "database_id", "database_id":  database_id},
        "properties": {
            "书名": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": info.get("title",' ')}}]
            },
            "豆瓣链接": {
                "url": url
            },
            "ISBN": {
                "type": "rich_text", 
                "rich_text": [{"type": "text", "text": {"content": info.get("ISBN",'')}}]
            },
            "页数": {
                "number": int(info.get("页数",0))
            },
            "出版社": {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": info.get("出版社",' ')}}]
            },
            "评分": {
                "number": float(info["score"])
            },
            "作者": {
                "type": "rich_text",
                "rich_text": [{"type": "text", "text": {"content": info.get('作者','')}}]
            },
            "标签": {
                "type": "multi_select",
                "multi_select": [{"name": info.get('tag')}]
            },
            "封面": {
                "files": [
                    {
                        "type": "external",
                        "name": info['cover'],
                        "external": {"url": info['cover']}
                    }
                ]
            },
            "状态": {
                "type": "select",
                "select": {
                    "name": info.get('status'),
                }
            },
        },
    }

    re = requests.request(
        "POST",
        "https://api.notion.com/v1/pages",
        json= body,
        headers={"Authorization": "Bearer " + token, "Notion-Version": "2022-02-22"},

    )
    if re.status_code == 200:
        print("Success!")
    else:
        print(re.text)

if __name__ == "__main__":

    token = 'secret_vWQy6ZyL5ao8V1P9FsvHEXhu4Wi8LziQFHNVFXEDrFY'
    database_id = "156f7826cf084cc7bc7ba066279a74b6" 
    argparser = ArgumentParser(description='Notion-doubanBook')
    argparser.add_argument("--url", "-u", help="豆瓣读书链接")
    argparser.add_argument("--tag", "-t", help="自定义标签，默认为空")
    argparser.add_argument("--status", "-s", help="阅读状态（未读，在读，读完），默认为未读")
    arg = argparser.parse_args()
    if arg.url is None :
        print("请输入豆瓣读书链接")
        print("E.g. doubanBook.py -u 'https://book.douban.com/subject/10491608/'")
    else:
        info=getInfo(arg.url)
        info['tag'] = arg.tag if arg.tag is not None else ' '
        info['status'] = arg.status if arg.status is not None else '未读'
        createRecord(info=info,token=token,database_id=database_id,url=arg.url)