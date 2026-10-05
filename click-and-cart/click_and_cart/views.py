from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
def index1(request):
    return redirect("/shop/")