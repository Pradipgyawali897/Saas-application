# app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SaasUser
from django.contrib.auth import authenticate


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = authenticate(request,username=username,password=password)
            if user:
                request.session["saas_user_id"] = user.id  # manual session
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid credentials")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, "login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login")
