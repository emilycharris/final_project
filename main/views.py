from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include
from main.models import Program, Profile, Queue, Rating, QueueProgram, GroupQueue
from django.http import HttpResponseRedirect
import random


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/login"

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['display_name','parent', 'rating_limit', 'email']
    success_url = reverse_lazy('profile_update_view')

    def get_object(self, queryset=None):
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

class ProgramDetailView(DetailView):
    model = Program

    def get_queryset(self, **kwargs):
        program_id = self.kwargs.get('pk')
        return Program.objects.filter(id=program_id)

class QueueCreateView(CreateView):
    model = QueueProgram
    fields = ['network']

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        queue = self.kwargs.get('pk')
        program = self.kwargs.get('program_pk')
        form.queue = Queue.objects.get(id=queue)
        form.program = Program.objects.get(id=program)
        form.save()
        print(form, form.queue, form.program)
        return HttpResponseRedirect(reverse_lazy('queue_list_view')) # <<- change

class QueueListView(ListView):
    model = QueueProgram

    def get_queryset(self):
        return QueueProgram.objects.filter(queue=self.request.user.queue.id)

class GroupQueueCreateView(CreateView):
    model = GroupQueue
    fields = ['user']
    success_url = reverse_lazy('group_queue_template_view')

class GroupQueueTemplateView(TemplateView):
    model = GroupQueue
    template_name = 'main/groupqueue_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = GroupQueue.objects.filter(user=self.request.user).last()
        program_list, rating_limit = list(group.get_random_program())
        upper_range = len(program_list)-1
        index_value = random.randint(0,upper_range)
        print(index_value)
        print(rating_limit)
        context['rating_limit'] = rating_limit
        context['random_program'] = program_list[index_value]
        return context
