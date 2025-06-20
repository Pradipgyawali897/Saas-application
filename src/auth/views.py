from django.shortcuts import render
from django.contrib.auth import login,authenticate,logout
def login_view(request):
    if request.method=="POST":
        password=request.POST.get('password')
        username=request.POST.get('username')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request)
            return redirect('home')
    return render(request,'auth/login.html')


