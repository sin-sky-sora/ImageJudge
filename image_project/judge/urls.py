from django.urls import path
from .views import judgefunc, inputfunc, judgerfunc, mypagefunc
from . import views


urlpatterns = [
    path("",inputfunc,name="create"),
    path("judge/",judgefunc,name="judge"),
    path("judge/<int:pk>/",judgerfunc,name="judger"),
    path("mypage/",mypagefunc,name="mypage"),
]
