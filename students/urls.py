
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mark/', views.mark_attendance, name='mark_attendance'),
    path('records/', views.view_attendance, name='view_attendance'),
    path('submit/', views.submit_attendance_request, name='submit_attendance'),
    path('review/', views.review_requests, name='review_requests'),
    path('submit/', views.submit_attendance_request, name='submit_attendance'),

]
