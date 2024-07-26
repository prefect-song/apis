from django.urls import path
from manageSystem import views

urlpatterns = [

    path('get_video', views.get_video),
    path('capture_img', views.capture_img),
]