from django.contrib import admin
from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'sender', 'project', 'is_used', 'created_at')
    search_fields = ('email',)
