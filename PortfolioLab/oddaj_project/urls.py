"""oddaj_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from oddaj_app.views import LandingPage, AddDonation, Login, Register, LogoutView, UserProfileView, \
    FilterInstitutionsInFormView, UserUpdateView

urlpatterns = [
    path('', LandingPage.as_view(), name='landing_page'),
    path('admin', admin.site.urls),
    path('add_donation', AddDonation.as_view(), name='add_donation'),
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('user_profile', UserProfileView.as_view(), name='user_profile'),
    path('filter_institutions', FilterInstitutionsInFormView.as_view(), name='json_filter'),
    path("user_update", UserUpdateView.as_view(), name='user_update'),

]
