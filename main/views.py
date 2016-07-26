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
        queue = self.request.user.queue.id
        search = self.request.GET.get('search')
        if search:
            search_name = search.replace("+", " ").lower()
            return Program.objects.filter(name__contains=search_name)
        else:
            return Program.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     queue_pk = self.kwargs.get('queue_pk')
    #     context['queue'] = Queue.objects.get(id=queue_pk)
    #     return context

class ProgramDetailView(DetailView):
    model = Program

    def get_queryset(self, **kwargs):
        program_id = self.kwargs.get('pk')
        return Program.objects.filter(id=program_id)


class QueueCreateView(CreateView):
    model = QueueProgram
    fields = ['network']
    success_url = reverse_lazy('program_list_view')


    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        queue = self.kwargs.get('pk')
        program = self.kwargs.get('program_pk')
        form.queue = Queue.objects.get(id=queue)
        form.program = Program.objects.get(id=program)
        form.save()
        print(form, form.queue, form.program)
        return HttpResponseRedirect(reverse_lazy('index_view')) # <<- change
