from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    path('invite/', views.invite_member, name='invite'),
    path('join/<uuid:token>/', views.join_invitation, name='join'),
]
