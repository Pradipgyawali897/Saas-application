from django.shortcuts import render,HttpResponse

def home_section_view(request,*args, **kwargs):
    return HttpResponse("<h1>hello<h1>")