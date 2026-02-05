"""blood_cell_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path

from userapp import views as user_views
from mainapp import views as main_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Main
    path('admin/', admin.site.urls),
    path("", main_views.index, name="index"),
    path("index", main_views.index, name="index"),
    path("about", main_views.about, name="about"),
    path("contact", main_views.contact, name="contact"),
    path("login", main_views.login, name="login"),
    path("otp", main_views.otp, name="otp"),
    path("register", main_views.signup, name="signup"),
    
    # User
    path("user-dashboard", user_views.user_dashboard, name="user_dashboard"),
    path("detection", user_views.detection, name="detection"),
    path("detection-result", user_views.detection_result, name="detection_result"),
    path('user-logout', user_views.user_logout, name='user_logout'),
    path("profile", user_views.profile, name="profile"),

    # --- TOPPER FEATURES (Viva Additions) ---
    path('api/status/', user_views.api_info, name='api_info'),
    path('report/download/', user_views.download_report, name='download_report'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)