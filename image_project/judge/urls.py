from django.urls import path
from .views import create
from . import views


urlpatterns = [
    path("",create.as_view(),name="create"),
]
