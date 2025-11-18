from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project


@login_required
def project_board(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.members.all() and getattr(request.user, 'role', '') != 'MANAGER':
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    tickets = project.ticket_set.all().order_by('-created_at')
    return render(request, 'projects/project_board.html', {'project': project, 'tickets': tickets})
