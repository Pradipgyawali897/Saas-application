from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SaasUser, OTP
from django.contrib.auth import authenticate
from django.utils import timezone
from constum_auth.validate.otp import send_otp

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = authenticate(request, username=username, password=password)
            if user:
                request.session["saas_user_id"] = user.id
                send_otp(user, purpose='login')
                request.session['email'] = user.email
                request.session['purpose'] = 'login'
                return redirect("verify_otp")
            else:
                messages.error(request, "Invalid credentials")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, "constum_auth/login.html")

def logout_view(request):
    request.session.flush()
    return redirect("constum_auth/login")

def signup_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "constum_auth/signup.html")
        
        if SaasUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "constum_auth/signup.html")
        
        if SaasUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, "constum_auth/signup.html")
        
        user = SaasUser(email=email, username=username, password_hash=password)
        user.save() 
        request.session['email'] = email
        request.session['purpose'] = 'email_verification'
        messages.success(request, "Account created! Please verify your email with the OTP sent.")
        return redirect("verify_otp")
    
    return render(request, "constum_auth/signup.html")

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        try:
            user = SaasUser.objects.get(email=email)
            send_otp(user, purpose='login')  
            request.session['email'] = email
            request.session['purpose'] = 'login'
            messages.success(request, "OTP sent to your email")
            return redirect("verify_otp")
        except SaasUser.DoesNotExist:
            messages.error(request, "Email not found")
    return render(request, "constum_auth/forgot_password.html")

def verify_otp_view(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        email = request.POST["email"]
        purpose = request.POST["purpose"]
        
        try:
            user = SaasUser.objects.get(email=email)
            otp_obj = OTP.objects.filter(user=user, purpose=purpose, code=otp).first()
            if otp_obj and otp_obj.expiry_time > timezone.now():
                if purpose == 'email_verification':
                    user.is_active = True
                    user.save()
                    messages.success(request, "Email verified! You can now log in.")
                    return redirect("login")
                elif purpose == 'login':
                    request.session["saas_user_id"] = user.id
                    if 'forgot_password' in request.session:
                        return redirect("reset_password")
                    return redirect("dashboard")
            else:
                messages.error(request, "Invalid or expired OTP")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, "constum_auth/otp_verification.html")

def reset_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "reset_password.html")
        
        try:
            user = SaasUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully! Please log in.")
            del request.session['forgot_password']
            return redirect("login")
        except SaasUser.DoesNotExist:
            messages.error(request, "User not found")
    return render(request, "constum_auth/reset_password.html")