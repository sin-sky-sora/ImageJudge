from django.urls import path
from .views import create, judgefunc
from . import views


urlpatterns = [
    path("",create.as_view(),name="create"),
    path("judge/",judgefunc,name="judge"),
]
