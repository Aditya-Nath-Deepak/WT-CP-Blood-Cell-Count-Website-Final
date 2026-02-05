from django.shortcuts import render, redirect
import urllib.request
import random
from mainapp.models import *
from django.contrib import messages 
from django.core.mail import send_mail
import ssl
import urllib.parse
from django.conf import settings
from django.core.paginator import Paginator


# Create your views here.
def index(req):
    if req.method == "POST":
        name = req.POST.get("Name")
        email = req.POST.get("Email")
        subject = req.POST.get("Subject")
        message = req.POST.get("Message")
        if not name or not email or not subject or not message:
            messages.warning(req, "Enter all the fields to continue")
            return render(req, 'main/index.html')
        Contact_Us.objects.create(
            Full_Name=name, Email_Address=email, Subject=subject, Message=message
        )
        messages.success(req, "Your message has been submitted successfully.")
    return render(req,"main/index.html")

def about(request):
    return render(request,"main/about.html")

def contact(req):
    if req.method == "POST":
        name = req.POST.get("Name")
        email = req.POST.get("Email")
        subject = req.POST.get("Subject")
        message = req.POST.get("Message")
        if not name or not email or not subject or not message:
            messages.warning(req, "Enter all the fields to continue")
            return render(req, 'main/contact.html')
        Contact_Us.objects.create(
            Full_Name=name, Email_Address=email, Subject=subject, Message=message
        )
        messages.success(req, "Your message has been submitted successfully.")
    return render(req,"main/contact.html")

def login(req):
    if req.method == "POST":
        user_email = req.POST.get("email")
        user_password = req.POST.get("password")
        if not user_email or not user_password:
            messages.warning(req, "Enter all the fields to continue")
            return render(req, 'main/login.html')

        try:
            users_data = UserModel.objects.filter(user_email=user_email)
            if not users_data.exists():
                messages.error(req, "User does not exist")
                return redirect("login")

            for user_data in users_data:
                if user_data.user_password == user_password:
                    if (user_data.Otp_Status == "verified" and user_data.User_Status == "accepted"):
                        req.session["user_id"] = user_data.user_id
                        messages.success(req, "You are logged in..")
                        user_data.No_Of_Times_Login += 1
                        user_data.save()
                        return redirect("user_dashboard")
                    elif (user_data.Otp_Status == "verified" and user_data.User_Status == "pending"):
                        messages.info(req, "Your Status is pending")
                        return redirect("login")
                    elif (user_data.Otp_Status == "verified" and user_data.User_Status == "removed"):
                        messages.info(req, "Your Account has been suspended...!")
                        return redirect("login")
                    else:
                        messages.warning(req, "verifyOTP...!")
                        req.session["user_email"] = user_data.user_email
                        return redirect("otp")
                else:
                    messages.error(req, "Incorrect credentials...!")
                    return redirect("login")

            messages.error(req, "Incorrect credentials...!")
            return redirect("login")
        except Exception as e:
            print(e)
            messages.error(req, "An error occurred. Please try again later.")
            return redirect("login")
    return render(req,"main/login.html")

def signup(req):
    if req.method == "POST":
        fullname = req.POST.get("username")
        email = req.POST.get("email")
        password = req.POST.get("password")
        age = req.POST.get("age")
        address = req.POST.get("address")
        phone = req.POST.get("contact number")
        image = req.FILES.get("image")
        number = random.randint(1000, 9999)

        if not fullname or not email or not password or not age or not address or not phone or not image or not number:
            messages.warning(req, "Enter all the fields to continue")
            return render(req, 'main/signup.html')


        try:
            data = UserModel.objects.get(user_email=email)
            messages.warning(
                req, "Email was already registered, choose another email..!"
            )
            return redirect("signup")
        except:
            sendSMS(fullname,number,phone)
            UserModel.objects.create(
                user_name=fullname,
                user_email=email,
                user_contact=phone,
                user_age=age,
                user_password=password,
                user_address=address,
                user_image=image,
                Otp_Num=number,
                User_Status="accepted"
            )

            mail_message = (
                f"Registration Successfully\n Your 4 digit Pin is below\n {number}"
            )
            print(mail_message)
            send_mail("Verify your OTP", mail_message , settings.EMAIL_HOST_USER, [email])
            req.session["user_email"] = email
            messages.success(req, "Your account was created..")
            return redirect("otp")
    print(req.method)
    return render(req, "main/signup.html")

def otp(req):
    user_email = req.session.get("user_email")
    if user_email:
        try:
            user_o = UserModel.objects.get(user_email=user_email)
        except UserModel.DoesNotExist:
            messages.error(req, "User not found.")
            return redirect("login")

        if req.method == "POST":
            otp1 = req.POST.get("otp1", "")
            otp2 = req.POST.get("otp2", "")
            otp3 = req.POST.get("otp3", "")
            otp4 = req.POST.get("otp4", "")

            if otp1 and otp2 and otp3 and otp4:
                user_otp = otp1 + otp2 + otp3 + otp4
                if user_otp.isdigit():
                    u_otp = int(user_otp)
                    if u_otp == user_o.Otp_Num:
                        user_o.Otp_Status = "verified"
                        user_o.save()
                        messages.success(
                            req, "OTP verification was successful. You can now login."
                        )
                        return redirect("login")
                    else:
                        messages.error(
                            req, "Invalid OTP. Please enter the correct OTP."
                        )
                else:
                    messages.error(
                        req, "Invalid OTP format. Please enter numbers only."
                    )
            else:
                messages.error(req, "Please enter all OTP digits.")

    else:
        messages.error(req, "Session expired. Please retry the OTP verification.")

    return render(req, "main/otp.html")
    

def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode(
        {
            "username": "Aditya Nath Deepak",
            "apikey": "56dbbdc9cea86b276f6c",
            "mobile": mobile,
            "message": f"Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you",
            "senderid": "Aditya Nath Deepak",
        }
    )
    data = data.encode("utf-8")
    # Disable SSL certificate verification
    context = ssl._create_unverified_context()
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data, context=context)
    return f.read()