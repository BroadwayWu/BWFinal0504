from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('create/', views.create,name='create'),
    path('update/', views.update,name='update'),
    path('', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('storymap/', views.storymap,name='storymap'),
    path('checkname/<str:name>',views.checkname,name='checkname'),
    path('survey/', views.survey,name='survey'),
    path('userpattern/', views.userpattern,name='userpattern'),
    # path('voice/', views.voice,name='voice'),
    # path('voiceUnknown/', views.voiceUnknown,name='voiceUnknown'),
    # path('voiceError/', views.voiceError,name='voiceError'),
    # path('voiceContinue/', views.voiceContinue,name='voiceContinue'),
    # path('voiceContinue_con/', views.voiceContinue_con,name='voiceContinue_con'),
    path('pic_saver/',views.pic_saver,name='pic_saver'),
    path('graphmodel/', views.graphmodel,name='graphmodel'),
    path('road_direction/', views.road_direction,name='road_direction'),
    path('voicestart/', views.voicestart,name='voicestart'),
    path('voiceend/', views.voiceend,name='voiceend'),
    path('voicemode/', views.voicemode,name='voicemode')
    # path('voicecon/', views.voicecon,name='voicecon')
    # path('voicestand/', views.voicestand,name='voicestand')
]
