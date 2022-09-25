from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('password', views.password, name='password'),
    path('faq', views.faq, name='faq'),
    path('check', views.check, name='check')
]