from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    url('', views.boards, name='index'),
    url('tests', views.boards, name='test'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)