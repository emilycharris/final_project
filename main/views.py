from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include
from main.models import Program, Profile, Queue, Rating, QueueProgram
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from extra_views.generic import GenericInlineFormSet
from django.http import HttpResponseRedirect


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
        # try:
        #     profile = self.request.user.profile
        # except DoesNotExist:
        #     profile = Profile(user=self.request.user)
        return self.request.user.profile

class ProgramListView(ListView):
    model = Program
    paginate_by = 15

    def get_queryset(self, **kwargs):
        programs = Program.objects.all()
        search = self.request.GET.get('search')
        if search:
            search_name = search.replace("+", " ").lower()
            return Program.objects.filter(name__contains=search_name)
        else:
            return Program.objects.all()

class ProgramDetailView(DetailView):
    model = Program

    def get_queryset(self, **kwargs):
        program_id = self.kwargs.get('pk')
        return Program.objects.filter(id=program_id)

class QueueProgramInline(InlineFormSet):
    model = QueueProgram
    fields = ['network']
    extra = 1

class QueueCreateView(CreateWithInlinesView):
    model = Queue
    inlines = [QueueProgramInline]
    fields = []
    success_url = reverse_lazy("index_view") # <<- change

    def forms_valid(self, form, inlines, **kwargs):
        form = form.save(commit=False)
        form.user = self.request.user
        form.save()
        for formset in inlines:
            for inline_form in formset:
                program_id = self.kwargs.get('pk')
                unsaved_form = inline_form.save(commit=False)
                unsaved_form.program = Program.objects.get(id=program_id)
                unsaved_form.queue = form
                unsaved_form.save()
        return HttpResponseRedirect(reverse_lazy('index_view')) # <<- change

#django-extra-views https://github.com/AndrewIngram/django-extra-views/
