from django.urls import path
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
    UserCreate,

)


urlpatterns = [
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
    path('project/<int:id>/user/add/', UserCreate.as_view(), name='user_add'),

]