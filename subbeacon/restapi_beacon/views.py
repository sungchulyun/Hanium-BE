#from django.shortcuts import render

# Create your views here.


from django.db.models import query
from rest_framework import viewsets
from django.views import View
from . import models
from restapi_beacon.models import  User, naviroot, ocrimg, subway, arrival, destination, subwayim, userstatus
from restapi_beacon.serializers import ocrimgSerializer, UserSerializer, subwaySerializer, arrivalSerializer, destinationSerializer, subwayimSerializer, userstatusSerializer, navirootSerializer
import json
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup
import threading
from django.shortcuts import render
import cv2
import sys
import time
from django.conf import settings
import os
from .crawling import positiondata, arrreset, destreset, subreset, subdata, arrsave, rootdata, userposition
import re

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class subwayViewSet(viewsets.ModelViewSet):
    queryset = subway.objects.all()
    serializer_class = subwaySerializer

class arrivalViewSet(viewsets.ModelViewSet):
    queryset = arrival.objects.all()
    serializer_class = arrivalSerializer

class destinationViewSet(viewsets.ModelViewSet):
    queryset = destination.objects.all()
    serializer_class = destinationSerializer

class subwayimViewSet(viewsets.ModelViewSet):
    queryset = subwayim.objects.all()
    serializer_class = subwayimSerializer

class userstatusViewSet(viewsets.ModelViewSet):
    queryset = userstatus.objects.all()
    serializer_class = userstatusSerializer

class navirootViewSet(viewsets.ModelViewSet):
    queryset = naviroot.objects.all()
    serializer_class = navirootSerializer

class ocrimgViewSet(viewsets.ModelViewSet):
    queryset = ocrimg.objects.all()
    serializer_class = ocrimgSerializer

class IndexView(View):
    def get(self, request):
        if request.method == 'GET':
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        if request.method == 'POST':
            body = json.loads(request.body.decode('utf-8'))
            print(body)
           
        return HttpResponse(status=200)

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40

image_path = "C:/Users/USER/work/subbeacon/media/2021/09/25.sign.jfif"
appkey = "20cdcbccac4bb4ff047f7a1fab7f859e"
img_list = "abc"

def hangul(st):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') # 한글과 띄어쓰기를 제외한 모든 글자
    # hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')  # 위와 동일
    result = []
    result = hangul.sub('', st) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
    return result

'''def home():
    word = "한글"
    if word.encode().isalpha():
        print("It is an alphabet")
    else:
        print("It is not an alphabet")
    word = "abc"
    if word.encode().isalpha():
        print("It is an alphabet")
    else:
        print("It is not an alphabet")
    global image_path
    image = ocrimg.objects.all()
    key = ocrimg.objects.latest('image')
    i = 20
    print(key.id)
    while(i< key.id): 
        img_list = ocrimg.objects.get(pk = i)
        image_path = img_list.image.url
        image_path = "/home/ubuntu/21_pf044/subbeacon" + str(image_path)   
        i = i+1
    print(image_path)'''

def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})

def getkey():
    queryset = ocrimg.objects.all()
    key = ocrimg.objects.latest('image')
    return key.id
def ocrexecute():
    global appkey, image_path, img_list
    image = ocrimg.objects.all()
    key = ocrimg.objects.last()
    print(key.id)
    i = 93
    while(i <= key.id): 
        #try:
            img_list = ocrimg.objects.get(pk = i)
            image_path = img_list.image.url
            image_path = "/home/ubuntu/21_pf044/subbeacon" + str(image_path)   
            resize_impath = kakao_ocr_resize(image_path)
            if resize_impath is not None:
                image_path = resize_impath
                print("원본 대신 리사이즈된 이미지를 사용합니다.")
            ocroutput = []
            ocrkor = []
            output = kakao_ocr(image_path, appkey).json()
            output = json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False)
            output = json.loads(output)
            for a in range(0, len(output['result'])):
                    ocroutput.extend(output['result'][a]['recognition_words'])
                    print(ocroutput[a])                 #이미지 하나로 텍스트 추출
            for a in range(0,len(ocroutput)):       #ocroutput배열 길이만큼 for 돌려
                    ocrkor += hangul(ocroutput[a])
                    ocrkor = ''.join(ocrkor)
            print(ocrkor)
            queryset = ocrimg.objects.all()
            ocr_list = ocrimg.objects.values_list('title',flat = True).filter(pk = i)
            print(ocr_list)
            ocr_list.update(title = ocrkor)
            i += 1
        #except: 
         #   print("재실행")
          #  break
              
    threading.Timer(3, ocrexecute).start()

ocrexecute()