from django.db.models import query
from django.db.models.query import QuerySet
import requests
from bs4 import BeautifulSoup
import threading

import django
django.setup()

def apidata():
    global open_url, res, soup, data
    open_url = 'http://swopenAPI.seoul.go.kr/api/subway/7a767a466f626f6f36335250756b45/xml/realtimeStationArrival/0/5/잠실나루'
    res = requests.get(open_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find_all('row')
    print(data)
apidata()
    