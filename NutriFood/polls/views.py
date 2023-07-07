from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hey tu es sur l'index de l'application search du projet NutriFood.")