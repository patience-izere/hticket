from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('create/<int:project_id>/', views.ticket_create, name='ticket_create'),
    path('edit/<int:ticket_id>/', views.ticket_edit, name='ticket_edit'),
    path('list/<int:project_id>/', views.ticket_list, name='ticket_list'),
]
