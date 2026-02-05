from django.db import models


# Create your models here.
class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(help_text="user_name", max_length=50)
    user_age = models.IntegerField(null=True)
    user_email = models.EmailField(help_text="user_email")
    user_password = models.EmailField(help_text="user_password", max_length=50)
    user_address = models.TextField(help_text="user_address", max_length=100)
    user_subject = models.TextField(
        help_text="user_subject", max_length=100, default="ok"
    )
    user_contact = models.CharField(help_text="user_contact", max_length=15, null=True)
    user_image = models.ImageField(upload_to="profilepic/", null=True)
    Date_Time = models.DateTimeField(auto_now=True, null=True)
    User_Status = models.TextField(default="pending", max_length=50, null=True)
    Otp_Num = models.IntegerField(null=True)
    Otp_Status = models.TextField(default="pending", max_length=60, null=True)
    Last_Login_Time = models.TimeField(null=True)
    Last_Login_Date = models.DateField(auto_now_add=True, null=True)
    No_Of_Times_Login = models.IntegerField(default=0, null=True)
    Message = models.TextField(max_length=250, null=True)

    # New field to track the number of predictions
    prediction_count = models.IntegerField(default=0, null=True)
    

    class Meta:
        db_table = "user_details"



class Contact_Us(models.Model):
    Full_Name = models.CharField(help_text="Full_name", max_length=50)
    Email_Address = models.EmailField(help_text="Email")
    Subject = models.CharField(help_text="Subject", max_length=50)
    Message = models.CharField(help_text="Message", max_length=50)

    class Meta:
        db_table = "Contact_Us"
    
        


class Predict_details(models.Model):
    predict_id = models.AutoField(primary_key=True)
    Field_1 = models.CharField(max_length=60, null=True)
    Field_2 = models.CharField(max_length=60, null=True)
    Field_3 = models.CharField(max_length=60, null=True)
    Field_4 = models.CharField(max_length=60, null=True)
    Field_5 = models.CharField(max_length=60, null=True)
    Field_6 = models.CharField(max_length=60, null=True)
    Field_7 = models.CharField(max_length=60, null=True)
    Field_8 = models.CharField(max_length=60, null=True)

    class Meta:
        db_table = "predict_detail"

