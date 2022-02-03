from django.db.models import query
from django.db.models.query import QuerySet
import requests
from bs4 import BeautifulSoup
import threading
import sys
sys.path.append('C:\\Users\\USER\\work\\subbeacon')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','subbeacon.settings')

import django
django.setup()
from restapi_beacon.models import User, arrival, destination, subway
def reset():
    queryset = subway.objects.all()
    queryset.delete()

def apidata():
    global open_url, res, soup, data
    open_url = 'http://swopenapi.seoul.go.kr/api/subway/6c434e5075626f6f33375576625070/xml/realtimePosition/0/40/7%ED%98%B8%EC%84%A0'
    res = requests.get(open_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find_all('row')
    

def updatedata():
    print("==================================재호출=======================================")
    apidata()
    global firststationno
    global firsttrainno
    firststationno = []
    firsttrainno = []
    updatetrainno = []
    updatestatnnm = []
    queryset = subway.objects.all()
    is_exist = queryset.exists()
    if(is_exist == False):
        for row in data:
            firststationno = row.find("statnnm").text
            firsttrainno = row.find("trainno").text
            subway(
                subwaynum = firsttrainno,
                subwaysta = firststationno
            ).save()
    
    subnumdata = (list(subway.objects.values_list('subwaynum',flat = True)))
    substadata = (list(subway.objects.values_list('subwaysta',flat = True)))
    subnumdata = sorted(subnumdata)
    substadata = sorted(substadata)
    print(subnumdata, substadata)
    apidata()
    for i in soup.find_all("trainno"):       
        updatetrainno.append(i.text)
    updatetrainno = list(map(int, updatetrainno))
    updatetrainno = sorted(updatetrainno)
    print(updatetrainno)
    for i in soup.find_all("statnnm"):       
        updatestatnnm.append(i.text)
    updatestatnnm = sorted(updatestatnnm)
   
    for i in range(0, len(subnumdata)):
        if(subnumdata[i] == updatetrainno[i]):
            if(substadata[i] != updatestatnnm[i]):
                subway_list = subway.objects.filter(subwaysta = substadata[i])
                subway_list.update(subwaysta = updatestatnnm[i])
                print(True)
        else:
            reset()
            updatedata()

    
   
    threading.Timer(180, updatedata).start()


reset()
updatedata()