from django.urls import path
from .views import judgefunc, inputfunc
from . import views


urlpatterns = [
    path("",inputfunc,name="create"),
    path("judge/",judgefunc,name="judge"),
]
