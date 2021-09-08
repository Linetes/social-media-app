from typing import Any, Optional
from django import http
from django.contrib import messages
from django.db import models
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic

from groups.models import Group,GroupMember
from . import models

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')

        return super().get(request, *args, **kwargs)
