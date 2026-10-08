"""
URL configuration for internsrizz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from interns_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="homepage"),
    path('home-page/', home_page, name="homepage"),
    path('signup-view/', signup_view, name="signup_view"),
    path('login-view/', login_view, name="login_view"), 
    path('profile-setup/', profile_setup, name="profile_setup"),
    path("job-feed/", job_feed, name="job_feed"),
]
