from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('tickets/', include('tickets.urls', namespace='tickets')),
    path('projects/', include('projects.urls', namespace='projects')),
]
