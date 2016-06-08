"""COTools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import revenueTracker.views as views

urlpatterns = [
	url(r'$', views.StudentHome.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^student_home/', views.StudentHome.as_view()),
    url(r'^edit_report/(?P<report_pk>[0-9]+)', views.EditReport.as_view()),
    url(r'^add_cash_gift/(?P<report_pk>[0-9]+)/(?P<student_pk>[0-9]+)',views.AddCashModal.as_view()),
    url(r'^add_check_gift/(?P<report_pk>[0-9]+)/(?P<student_pk>[0-9]+)',views.AddCheckModal.as_view()),
    url(r'^edit_cash_gift/(?P<report_pk>[0-9]+)/(?P<student_pk>[0-9]+)/(?P<cash_pk>[0-9]+)', views.AddCashModal.as_view()),
    url(r'^edit_check_gift/(?P<report_pk>[0-9]+)/(?P<student_pk>[0-9]+)/(?P<check_pk>[0-9]+)', views.AddCheckModal.as_view()),
]
