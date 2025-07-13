from django.shortcuts import render,HttpResponse
def home_section_view(request,*args, **kwargs):
    return render(request,'snippets/home.html')