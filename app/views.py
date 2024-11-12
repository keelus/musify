from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index_page(request):
    return HttpResponse(b"Hi");
