from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('<int:project_id>/board/', views.project_board, name='project_board'),
]
