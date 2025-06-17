# pc_builder/views.py
from django.core.cache import cache
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')