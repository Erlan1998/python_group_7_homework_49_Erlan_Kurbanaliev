"""list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from webapp.views import (
    IndexView,
    TaskView,
    TaskAddView,
    TaskUpdateView,
    TaskDeleteView,
    IndexViewProject,
    ProjectView,
    ProjectCreate,
    ProjectDeleteView,
    ProjectUpdateView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view(), name='index_tasks'),
    path('task/<int:id>/', TaskView.as_view(), name='task'),
    path('project/<int:id>/task/add/', TaskAddView.as_view(), name='task_add'),
    path('task/<int:id>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:id>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('', IndexViewProject.as_view(), name='index_project'),
    path('project/<int:id>/', ProjectView.as_view(), name='project'),
    path('project/create/', ProjectCreate.as_view(), name='project_create'),
    path('project/<int:id>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:id>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('accounts/', include('accounts.urls')),
]
