import requests
from bs4 import BeautifulSoup

def get_datas():

    client = requests.session()
    r = client.get("https://www.citytalk.tw/cata")
    phpsessid = client.cookies['PHPSESSID']

    soup = BeautifulSoup(r.text, 'lxml')
    csrf_token = soup.find('meta', attrs={'name':'csrf-token'})['content']

    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "PHPSESSID=" + phpsessid,
        "Host": "www.citytalk.tw",
        "Origin": "https://www.citytalk.tw",
        "Referer": "https://www.citytalk.tw/cata/",
        "X-CSRF-Token": csrf_token
    }

    data = {
        "type": "eventSearch_GET",
        "data[keyword]": "",
        "data[time]": "weekend",
        "data[time_range]": "",
        "data[time_new]": "",
        "data[time_expired]": "",
        "data[verify]": "t",
        "data[c_id]": "",
        "data[city]": "",
        "data[old]": "hide",
        "data[sort]": "hot",
        "data[ticket]": "all",
        "data[prize]": "hide",
        "data[free]": "all",
        "data[limit]": "10",
        "data[offset]": "1",
        "data[return]": "t",
        "data[random]": "f",
        "data[randomlimit]": "10",
        "data[v_id]": "0",
        "data[ep_id]": "0",
        "data[geo_lat]": "",
        "data[geo_lng]": "",
        "data[distance]": "1000",
        "data[date_modify]": "",
        "data[e_ids]": ""
    }

    ex_data = requests.post("http://www.citytalk.tw/post/v3/cata/index", headers=header, data=data)

    datas = ex_data.json()['data']

    content = []
    for i, data in enumerate(datas):
        id = data['e_id']
        title = data['title']
        img = data['img']
        text = '日期：' + data['e_start'] + '-' + data['e_end']
        content.append({'title':title,
                        'url': 'https://www.citytalk.tw/event/' + id + '-'+ title.replace(' ', ''), 
                        'img':'https://www.citytalk.tw' + img,
                        'text': text
                       })   

    return content