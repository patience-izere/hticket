from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Invitation
from .forms import InvitationForm, JoinForm


@login_required
def invite_member(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.sender = request.user
            invitation.save()
            # In production, enqueue email send via Celery. Dev: console backend.
            return HttpResponse(status=204, headers={'HX-Trigger': 'invitationSent'})
    else:
        form = InvitationForm()

    return render(request, 'invitations/invite_form.html', {'form': form})


def join_invitation(request, token):
    invitation = get_object_or_404(Invitation, token=token)
    if invitation.is_used:
        return render(request, 'invitations/join_expired.html', {'message': 'Invitation already used'})
    if invitation.expires_at and invitation.expires_at < timezone.now():
        return render(request, 'invitations/join_expired.html', {'message': 'Invitation expired'})

    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            # create username from email local part if needed
            base_username = invitation.email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = User.objects.create_user(username=username, email=invitation.email, password=form.cleaned_data['password1'])
            invitation.is_used = True
            invitation.save()
            # add to project if provided
            if invitation.project:
                invitation.project.members.add(user)
            login(request, user)
            return redirect('admin:index')  # replace with dashboard when available
    else:
        form = JoinForm()

    return render(request, 'invitations/join_form.html', {'form': form, 'email': invitation.email})
