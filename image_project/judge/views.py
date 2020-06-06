from django.shortcuts import render
from .models import ImageModel
from django.urls import reverse_lazy
from fjango.views.generic import CreateView

class create(CreateView):
    template_name = "create.html"
    model = ImageModel
    fields = '__all__'
    success_url = reverse_lazy()##判定ページへ飛ばす
