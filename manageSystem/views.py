import os
import time
from datetime import date
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse

from apis.settings import STATICFILES_DIRS
from manageSystem import DBMS
import json
import jwt
import base64
from django.http import FileResponse
import cv2
from manageSystem import tools

video = 'http://192.168.3.41:4747/video'

camera = cv2.VideoCapture(video)


def get_video(request):
    # 视频流相机对象
    videoStream = tools.gen_display(camera)
    # 使用流传输传输视频流
    return StreamingHttpResponse(videoStream, content_type='multipart/x-mixed-replace; boundary=frame')


def capture_img(request):
    current_img = tools.get_current_img()
    if not current_img:
        return HttpResponse('')
    return HttpResponse(current_img)
