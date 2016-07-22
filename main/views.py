from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include
from main.models import Program



# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class CreateUserView(CreateView):
    pass

class ProfileUpdateView(UpdateView):
    pass

class ProgramListView(ListView):
    model = Program

class ProgramDetailView(DetailView):
    model = Program

    def get_queryset(self, **kwargs):
        program_id = self.kwargs.get('pk')
        return Program.objects.filter(id=program_id)
