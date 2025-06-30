from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload-image/', views.upload_image_view, name='upload_image'),
    path('upload-vedio/',views.video_upload_view,name='upload_vedio'),
    path('', views.home_view, name='home'),
    path('contactme/',views.contact_page_view),
    path('services/',views.service_page_view),
    path('upload-video-result/', views.upload_video_result, name='upload_video_result'),

    # path('upload-video/', views.video_upload_view, name='video_upload_view'),
    # path('upload-video-result/', views.upload_video_result, name='upload_video_result')
]
