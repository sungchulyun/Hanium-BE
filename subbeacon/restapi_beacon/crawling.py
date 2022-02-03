#from django.shortcuts import render

# Create your views here.


from django.db.models import query
from rest_framework import viewsets
from django.views import View
from restapi_beacon.models import  User, naviroot, ocrimg, subway, arrival, destination, subwayim, userstatus
from restapi_beacon.serializers import ocrimgSerializer, UserSerializer, subwaySerializer, arrivalSerializer, destinationSerializer, subwayimSerializer, userstatusSerializer, navirootSerializer
import json
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup
import threading


def arrreset():
    queryset = arrival.objects.all()
    queryset.delete()

def destreset():
    queryset = destination.objects.all()
    queryset.delete()

def subreset():
    queryset = subway.objects.all()
    queryset.delete()

def subdata():                          #실시간 열차 위치 api 호출
    global open_url, res, soup, data
    open_url = 'http://swopenapi.seoul.go.kr/api/subway/6c434e5075626f6f33375576625070/xml/realtimePosition/0/55/7%ED%98%B8%EC%84%A0'
    res = requests.get(open_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find_all('row')



def positiondata():                        #3분마다 api 재호출해 db update
    print("==================================재호출=======================================")
    subdata()
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
    subdata()
    for i in soup.find_all("trainno"):       
        updatetrainno.append(i.text)
    updatetrainno = list(map(int, updatetrainno))
    updatetrainno = sorted(updatetrainno)
    for i in soup.find_all("statnnm"):       
        updatestatnnm.append(i.text)
    updatestatnnm = sorted(updatestatnnm)
    try:
        '''for i in range(0, len(subnumdata)):
                if(subnumdata[i] == updatetrainno[i]):
                    if(substadata[i] != updatestatnnm[i]):
                        subway_list = subway.objects.filter(subwaysta = substadata[i])
                        subway_list.update(subwaysta = updatestatnnm[i])'''
        subreset()
        subdata()
        for row in data:
                firststationno = row.find("statnnm").text
                firsttrainno = row.find("trainno").text
                subway(
                        subwaynum = firsttrainno,
                        subwaysta = firststationno
                        ).save()
    except:
                    subreset()
                    subdata()
                    for row in data:
                        firststationno = row.find("statnnm").text
                        firsttrainno = row.find("trainno").text
                        subway(
                            subwaynum = firsttrainno,
                            subwaysta = firststationno
                        ).save()
    threading.Timer(100, positiondata).start()

                                     
   

def arrsave():                                  #도착예정정보 db저장
   
    global open_url, res, soup, data
    startdestination = []
    startdestination = (list(destination.objects.values_list('startdet',flat = True)))
    open_url = 'http://swopenapi.seoul.go.kr/api/subway/50467a7974626f6f37364f47474253/xml/realtimeStationArrival/0/5/' + startdestination[0] 
    res = requests.get(open_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find_all('row')
    queryset = arrival.objects.all()
    is_exist = queryset.exists()
    if(is_exist == False):
        for row in data:
             staname = row.find("statnnm").text
             subdir = row.find("trainlinenm").text
             subarrtime = row.find("barvldt").text
             subtrainno = row.find("btrainno").text
             subwaycode = row.find("updnline").text
             arrival(
                station = staname,
                trainline = subdir,
                arrivetime =  subarrtime,
                trainnum = subtrainno,
                waycode = subwaycode
            ).save()
    else:
        queryset.delete()
        for row in data:
             staname = row.find("statnnm").text
             subdir = row.find("trainlinenm").text
             subarrtime = row.find("barvldt").text
             subtrainno = row.find("btrainno").text
             subwaycode = row.find("updnline").text
             arrival(
                station = staname,
                trainline = subdir,
                arrivetime =  subarrtime,
                trainnum = subtrainno,
                waycode = subwaycode
            ).save()
   

def rootdata():                                 #destination에서 출발지와 도착지를 파라미터로 api 호출
    global open_url, res, soup, data
    startsta = (list(destination.objects.values_list('startdet',flat = True)))
    startsta = list(subwayim.objects.values_list('subid',flat = True).filter(substa = startsta[0]))
    finalsta = (list(destination.objects.values_list('enddet',flat = True)))
    finalsta = list(subwayim.objects.values_list('subid',flat = True).filter(substa = finalsta[0]))
    open_url = 'https://api.odsay.com/v1/api/subwayPath?lang=0&CID=1000&SID=' + str(startsta[0]) + '&EID=' + str(finalsta[0]) + '&Sopt=1&apiKey=DutLvusKsPNGmWGOTGtoWHgW%2BFNs6GW%2BH4mKfIUdmAE&output=xml'
    res = requests.get(open_url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find_all('driveinfo')
    trainline = []
    waydir= []
    waycode = []
    startsta = []
    exchasta = []
   
    for i in soup.find_all("wayname"):       
       waydir.append(i.text)
    for i in soup.find_all("waycode"):       
       waycode.append(i.text)
    for i in soup.find_all("startname"):       
       startsta.append(i.text)
    queryset = naviroot.objects.all()
    is_exist = queryset.exists()
    if(is_exist == False):
            naviroot(
                startline = waydir[0],
                startwname = startsta[0],
                startwcode = waycode[0],
                exchaline = waydir[1],
                exchawname = startsta[1],
                exchawcode = waycode[1]
                ).save()
    else:
        queryset.delete()
        naviroot(
                startline = waydir[0],
                startwname = startsta[0],
                startwcode = waycode[0],
                exchaline = waydir[1],
                exchawname = startsta[1],
                exchawcode = waycode[1]
                ).save()

    setstartsta = (list(naviroot.objects.values_list('startwname',flat = True)))
    if(setstartsta[0] != startsta[0]):
        queryset.delete()
        rootdata()
    
   

def userposition():
    rootdata()
    traindir = (list(naviroot.objects.values_list('startwcode',flat = True)))
    for i in range(0, len(traindir)):
        if(traindir[i] == 1):
               traindir[i] = "상행"
        else:
                traindir[i] = "하행"
    usertra = list(arrival.objects.values_list('trainnum',flat = True).filter(waycode = traindir[0]))
    if not usertra:
        positiondata()
    userstation = list(subway.objects.values_list('subwaysta',flat = True).filter(subwaynum = usertra[0]))
    if not userstation:
        positiondata()
    queryset = userstatus.objects.all()
    is_exist = queryset.exists()
    if(is_exist == False):
            for n in userstation:
             userstatus(
                    usersta = userstation[0],
                    usertrain = usertra[0]
                 ).save()
    else:
            user_list = userstatus.objects.filter(usertrain = usertra[0])
            userstation = list(subway.objects.values_list('subwaysta',flat = True).filter(subwaynum = usertra[0]))
            user_list.update(usersta = userstation[0])
             
    
    threading.Timer(60, userposition).start()

