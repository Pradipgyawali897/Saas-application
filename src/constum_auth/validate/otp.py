from django.core.mail import send_mail
from constum_auth.models import OTP
from django.core.mail import send_mail, BadHeaderError
import smtplib
from django.utils import timezone


def send_otp_email(user_email,otp):
    send_mail(
        subject="Your OTP Code",
        message=f"Your one-time password is {otp}. It expires in 5 minutes.",
        from_email="your_email@example.com",
        recipient_list=[user_email],
        fail_silently=False,
    )

def send_otp(request):
    user=request.user
    OTP.objects.create(user=user)
    try:
        otp=OTP.objects.get(user=user).code
        try:
            email=request.user.email
            send_otp_email(user_email=email,otp=otp)
        except BadHeaderError:
            print("Invalid header found.")
            raise
        except smtplib.SMTPException as e:
            print("SMTP error:", e)
            raise
        except Exception as e:
            print("General email send failure:", e)
            raise
    except:
     print("error")


def validate_otp(request):
    if request.method=="POST":
        user=request.user
        otp=OTP.objects.get(user=user)
        otp_got=request.POST.get("opt")
        expiry_time=otp.expiry_time
        created_at=otp.created_at
        if expiry_time>=timezone.now():
            if otp_got==otp:
                return True
    return False
    




