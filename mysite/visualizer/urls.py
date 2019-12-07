from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.boards, name='index'),
    url('tests', views.boards, name='test'),
]