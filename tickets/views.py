from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import TicketForm
from .models import Ticket
from projects.models import Project


@login_required
def ticket_create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.members.all() and getattr(request.user, 'role', '') != 'MANAGER':
        raise PermissionDenied

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.project = project
            ticket.reporter = request.user
            ticket.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'ticketListUpdated'})
    else:
        form = TicketForm()

    return render(request, 'tickets/partials/ticket_form.html', {'form': form, 'project': project})


@login_required
def ticket_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # permission: only members or managers can view
    if request.user not in project.members.all() and getattr(request.user, 'role', '') != 'MANAGER':
        raise PermissionDenied

    tickets = Ticket.objects.filter(project=project).order_by('-created_at')
    return render(request, 'tickets/partials/ticket_list.html', {'tickets': tickets, 'project': project})


@login_required
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    project = ticket.project
    if request.user not in project.members.all() and getattr(request.user, 'role', '') != 'MANAGER':
        raise PermissionDenied

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={'HX-Trigger': 'ticketUpdated'})
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'tickets/partials/ticket_form.html', {'form': form, 'project': project, 'ticket': ticket})
