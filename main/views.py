from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include
from main.models import Program, Profile, Queue, Rating, QueueProgram
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login"

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['parent', 'rating_limit', 'email']
    success_url = reverse_lazy('profile_update_view')

    def get_object(self, queryset=None):
        return self.request.user.profile

class ProgramListView(ListView):
    model = Program

class ProgramDetailView(DetailView):
    model = Program

    def get_queryset(self, **kwargs):
        program_id = self.kwargs.get('pk')
        return Program.objects.filter(id=program_id)

class QueueProgramInline(InlineFormSet):
    model = QueueProgram
    fields = ['program', 'network']
    extra = 1

class QueueCreateView(CreateWithInlinesView):
    model = Queue
    inlines = [QueueProgramInline]
    fields = []
    success_url = reverse_lazy("index_view") # <<- change

    def forms_valid(self, form, inlines):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        for formset in inlines:
            print(formset.instance)
            formset.save()
        return HttpResponseRedirect(reverse_lazy('index_view')) # <<- change

#django-extra-views https://github.com/AndrewIngram/django-extra-views/
