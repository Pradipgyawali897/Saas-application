from django.core.mail import send_mail, BadHeaderError
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import smtplib

def send_otp_email(otp_obj):
    try:
        purpose = otp_obj.purpose
        otp = otp_obj.code
        user_email = otp_obj.user.email
        subject = "Your OTP Code" if purpose == "login" else "Verify Your Email"
        message = (
            f"Your one-time password is {otp}. It expires in 5 minutes."
            if purpose == "login"
            else f"Your email verification code is {otp}. It expires in 5 minutes."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email="your_email@example.com",
            recipient_list=[user_email],
            fail_silently=False,
        )
    except BadHeaderError:
        raise Exception("Invalid header found while sending email.")
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP error occurred: {str(e)}")
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")

def send_otp(user, purpose='login'):
    try:
        OTP = apps.get_model("constum_auth", "OTP")
        OTP.objects.filter(user=user, purpose=purpose).delete()
        otp_obj = OTP.objects.create(user=user, purpose=purpose)
        send_otp_email(otp_obj)
        return otp_obj
    except Exception as e:
        raise Exception(f"Failed to send OTP for {purpose}: {str(e)}")

def validate_otp(user, otp_got, purpose='login'):
    try:
        OTP = apps.get_model("constum_auth", "OTP")
        otp = OTP.objects.filter(user=user, purpose=purpose).order_by('-created_at').first()
        if not otp:
            raise Exception(f"No valid OTP request found for {purpose}.")
        if timezone.now() <= otp.expiry_time:
            if otp_got == otp.code:
                otp.delete()
                return True
            return False
        else:
            otp.delete()
            raise Exception("OTP has expired.")
    except Exception as e:
        raise