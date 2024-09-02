"""lti_inspector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from django.urls import re_path

from inspector import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.tool_config, name='tool_config'),
    re_path(r'^launch[/]{0,1}(?P<placement>[a-z_]*)$', views.lti_launch, name='lti_launch'),
    re_path(r'^return_assignment_selection$', views.return_assignment_selection, name='return_assignment_selection'),
    re_path(r'^return_homework_submission$', views.return_homework_submission, name='return_homework_submission'),
    re_path(r'^return_editor_button_selection$', views.return_editor_button_selection, name='return_editor_button_selection'),
    re_path(r'^view_assignment/(?P<assignment_id>[a-zA-Z0-9]+)$', views.view_assignment, name='view_assignment'),
    re_path(r'^view_homework_submission/(?P<submission_id>[a-zA-Z0-9]+)$', views.view_homework_submission, name='view_submission'),


]
