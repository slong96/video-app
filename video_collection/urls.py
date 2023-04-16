from django.urls import path
from . import views

# empty path string means home page
urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video'),
    path('video_list', views.video_list, name='video_list'),
    # video/1 # video/2 and so on, video_pk is primary key from Video model
    path('video/<int:video_pk>', views.video_detail, name='video_detail')
]