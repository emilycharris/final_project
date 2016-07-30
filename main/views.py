from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url, include
from main.models import Program, Profile, Queue, Rating, QueueProgram, GroupQueue
from django.http import HttpResponseRedirect
import random
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import redirect


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

class CreateParentView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/sign_up.html'
    success_url = "/login"

class CreateChildView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'auth/sign_up.html'

    def get_success_url(self, **kwargs):
        user=User.objects.last()
        return reverse_lazy('child_profile_update_view', kwargs = {'pk':user.id})


class ParentProfileUpdateView(UpdateView):
    model = Profile
    fields = ['display_name', 'email', 'photo']
    success_url = reverse_lazy('children_profile_list_view')

    def get_object(self, queryset=None):
        return self.request.user.profile


class ChildProfileUpdateView(UpdateView):
    model = Profile
    fields = ['display_name', 'rating_limit', 'photo']
    success_url = reverse_lazy('queue_list_view')
    template_name = 'main/child_profile_update.html'

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        parent = self.request.user
        form.parent = Profile.objects.get(user=parent)
        form.save()
        return HttpResponseRedirect(reverse_lazy('children_profile_list_view'))


class ChildrenProfileListView(ListView):
    model = Profile

    def get_queryset(self):
        children = Profile.objects.filter(parent=self.request.user.id)
        return children

class ProgramListView(ListView):
    model = Program
    paginate_by = 16

    def get_queryset(self, **kwargs):
        programs = Program.objects.all()
        queue = self.request.user.queue.id
        search = self.request.GET.get('search')
        if search:
            search_name = search.replace("+", " ")
            results = Program.objects.filter(name__icontains=search_name)
            return results

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
    paginate_by = 16

    def get_queryset(self, **kwargs):
        programs = QueueProgram.objects.all()
        queue = self.request.user.queue.id
        search = self.request.GET.get('search')
        if search:
            search_name = search.replace("+", " ").lower()
            return QueueProgram.objects.filter(queue=self.request.user.queue.id).filter(program__contains=search_name)
        else:
            return QueueProgram.objects.filter(queue=self.request.user.queue.id)

class QueueProgramDeleteView(DeleteView):
    model = QueueProgram
    success_url = reverse_lazy('queue_list_view')

class GroupQueueCreateView(CreateView):
    model = GroupQueue
    fields = ['user']
    success_url = reverse_lazy('group_queue_template_view')

    def get_form(self):
        form = super().get_form()
        users = User.objects.all()
        user_list = []
        for user in users:
            if self.request.user.profile.parent == None:
                parent = self.request.user
            else:
                child = self.request.user
                parent = self.request.user.profile.parent
                user_list.append(child)
        if parent:
            user_list.append(parent)
        print(user_list)
        # Profiles that have a parent = self.request.user
        # form.fields['user'].queryset = User.objects.filter(pk__in=self.request.user)
        return form
'''
    def get_queryset(self):
        users = User.objects.all()
        user_list = []
        for user in self.users.all():
            if self.request.user.parent == None:
                parent = self.request.user
            else:
                parent = self.request.user.parent
                child = self.request.user
            user_list.append(parent)
            user_list.append(child)
            print(user_list)
            return user_list
'''

class GroupQueueTemplateView(TemplateView):
    model = GroupQueue
    template_name = 'main/groupqueue_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = GroupQueue.objects.filter(user=self.request.user).last()
        program_list, rating_limit = list(group.get_random_program())
        upper_range = len(program_list)-1
        index_value = random.randint(0,upper_range)
        context['rating_limit'] = rating_limit
        context['random_program'] = program_list[index_value]
        return context
