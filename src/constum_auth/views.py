from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import SaasUser, OTP
from .validate.otp import send_otp, validate_otp

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("Email") 
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            request.session["saas_user_id"] = user.id
            request.session["email"] = user.email
            request.session["purpose"] = "login"
            send_otp(user, purpose="login")
            return redirect("verify_otp")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "constum_auth/login.html")

def logout_view(request):
    request.session.flush()
    return redirect("login") 

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "constum_auth/signup.html")

        if SaasUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "constum_auth/signup.html")

        if SaasUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "constum_auth/signup.html")

        user = SaasUser(email=email, username=username)
        user.set_password(password)  
        user.is_active = False  
        user.save()
        request.session["email"] = email
        request.session["purpose"] = "email_verification"
        send_otp(user, purpose="email_verification")
        messages.success(request, "Account created! Please verify your email with the OTP sent.")
        return redirect("verify_otp")

    return render(request, "constum_auth/signup.html")

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = SaasUser.objects.get(email=email)
            send_otp(user, purpose="login")
            request.session["email"] = email
            request.session["purpose"] = "login"
            request.session["forgot_password"] = True  
            messages.success(request, "OTP sent to your email")
            return redirect("verify_otp")
        except SaasUser.DoesNotExist:
            messages.error(request, "Email not found")
    return render(request, "constum_auth/forgot_password.html")

def verify_otp_view(request):
    email = request.session.get("email")
    purpose = request.session.get("purpose")
    if not email or not purpose:
        messages.error(request, "Session expired or invalid. Please try again.")
        return redirect("login")

    if request.method == "POST":
        otp = request.POST.get("otp")
        try:
            otp = int(otp) 
            user = SaasUser.objects.get(email=email)
            if validate_otp(user, otp, purpose):
                if purpose == "email_verification":
                    user.is_active = True
                    user.save()
                    messages.success(request, "Email verified! You can now log in.")
                    return redirect("login")
                elif purpose == "login":
                    request.session["saas_user_id"] = user.id
                    if request.session.get("forgot_password"):
                        return redirect("reset_password")
                    return redirect("dashboard")
            else:
                messages.error(request, "Invalid OTP")
        except ValueError:
            messages.error(request, "OTP must be a number")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
        except Exception as e:
            messages.error(request, str(e)) 
    return render(request, "constum_auth/otp_verification.html", {"email": email, "purpose": purpose})

def reset_password_view(request):
    email = request.session.get("email")
    if not email or not request.session.get("forgot_password"):
        messages.error(request, "Session expired or invalid. Please try again.")
        return redirect("login")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "constum_auth/reset_password.html", {"email": email})

        try:
            user = SaasUser.objects.get(email=email)
            user.set_password(password) 
            user.save()
            messages.success(request, "Password reset successfully! Please log in.")
            request.session.flush()  
            return redirect("login")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, "constum_auth/reset_password.html", {"email": email})

def regenerate_otp_view(request):
    email = request.session.get("email")
    purpose = request.session.get("purpose")

    if not email or not purpose:
        messages.error(request, "Session expired or invalid. Please try again.")
        return redirect("login")

    if request.method == "POST":
        try:
            user = SaasUser.objects.get(email=email)
            send_otp(user, purpose=purpose)
            messages.success(request, "A new OTP has been sent to your email.")
            return redirect("verify_otp")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
            return redirect("login")

    return render(request, "constum_auth/regenerate_otp.html", {"email": email, "purpose": purpose})