from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf.urls import url, include
from main.models import Program, Profile, Queue, Rating, QueueProgram, FamilyQueue
from django.http import HttpResponseRedirect
import random
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.mail import send_mail
from what_to_watch.settings import EMAIL_HOST_USER
from django.shortcuts import render_to_response
from django.template import RequestContext


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
    success_url = reverse_lazy('program_list_view')

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
    paginate_by = 8
    template_name = 'main/children_profile_list.html'

    def get_queryset(self):
        children = Profile.objects.filter(parent=self.request.user.id).order_by('rating_limit')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program_queryset = self.request.user.queue.queueprogram_set.all()
        queue_list = []
        for item in program_queryset:
            queue_list.append(item.program.name)
        context['queue_list'] = queue_list
        page = self.request.GET.get('page')
        if page:
            context['page'] = page
        else:
            context['page'] = "1"
        return context

class ProgramDetailView(DetailView):
    model = Program

    def get_queryset(self, **kwargs):
        program_id = self.kwargs.get('pk')
        return Program.objects.filter(id=program_id)

class QueueProgramDetailView(DetailView):
    model = QueueProgram

    def get_queryset(self, **kwargs):
        queueprogram_id = self.kwargs.get('pk')
        program_id = queueprogram_id.program.id
        print(program_id)

class QueueCreateView(CreateView):
    model = QueueProgram
    fields = ['network']

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        queue = self.kwargs.get('pk')
        program = self.kwargs.get('program_pk')
        page = self.kwargs.get('page')
        form.queue = Queue.objects.get(id=queue)
        form.program = Program.objects.get(id=program)
        rating_limit = self.request.user.profile.rating_limit
        if rating_limit:
            if form.program.rating.id > rating_limit.id:
                form.save()
                return self.send_email(form,**kwargs)
        form.save()
        return HttpResponseRedirect(reverse('program_list_view') + "?page={}".format(page))

    def send_email(self, form, **kwargs):
        rating_limit = self.request.user.profile.rating_limit
        if self.request.user.profile.display_name:
            child = self.request.user.profile.display_name
        else:
            child = self.request.user

        if self.request.user.profile.parent.display_name:
            parent = self.request.user.profile.parent.display_name
        else:
            parent = self.request.user.profile.parent
        rating = form.program.rating
        review = form.program.review
        positive_message = form.program.positive_message
        positive_role_model = form.program.positive_message
        violence = form.program.violence
        sex = form.program.sex
        language = form.program.language
        consumerism = form.program.consumerism
        substance = form.program.substance
        subject = "New Program Added that Exceeds Rating Limit"
        message = "Hi {},\n\nWe just wanted to let you know that {} added the program {} which exceeds the rating limit of {} you set up.\n\nIf you'd like to remove this show from queue, please sign in to your account.\n\nYou may want to know the following:\n\nThe show is rated {}.\n\nReview:\n{}\n\nPositive Message:\n{}\n\nPositive Role Model:\n{}\n\nViolence:\n{}\n\nSex:\n{}\n\nLanguage:\n{}\n\nConsumerism:\n{}\n\nSubstance:\n{}\n\n\n\nThis is an unmanaged account.  Please do not reply.".format(parent,child, form.program, rating_limit, rating, review, positive_message, positive_role_model, violence, sex, language, consumerism, substance)
        from_email = EMAIL_HOST_USER
        to_email = self.request.user.profile.parent.email
        if subject and message and from_email:
            send_mail(subject, message, from_email, [str(to_email)])
            page = self.kwargs.get('page')
            return HttpResponseRedirect(reverse('program_list_view') + "?page={}".format(page))

class QueueListView(ListView):
    model = QueueProgram
    paginate_by = 16

    def get_queryset(self, **kwargs):
        return QueueProgram.objects.filter(queue=self.request.user.queue.id)

class ChildQueueListView(ListView):
    model = QueueProgram
    paginate_by = 16
    template_name = 'main/child_queue_list.html'

    def get_queryset(self, **kwargs):
        programs = QueueProgram.objects.all()
        queue = self.kwargs.get('pk')
        search = self.request.GET.get('search')
        if search:
            search_name = search.replace("+", " ").lower()
            return QueueProgram.objects.filter(queue=self.request.user.queue.id).filter(program__contains=search_name)
        else:
            return QueueProgram.objects.filter(queue=queue)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        child_id = self.kwargs.get('pk')
        child = Profile.objects.get(id=child_id)
        context['child'] = child
        return context

class QueueProgramDeleteView(DeleteView):
    model = QueueProgram
    success_url = reverse_lazy('queue_list_view')

class FamilyQueueCreateView(CreateView):
    model = FamilyQueue
    fields = ['user']
    success_url = reverse_lazy('family_queue_template_view')

    def get_form(self):
        form = super().get_form()
        users = User.objects.all()
        user_list = []
        if self.request.user.profile.parent == None:
            parent = self.request.user.profile
        else:
            parent = self.request.user.profile.parent
        user_list.append(parent.id)
        children = Profile.objects.filter(parent=parent)
        for child in children:
            user_list.append(child.id)
        form.fields['user'].queryset = User.objects.filter(pk__in=user_list)
        return form

class FamilyQueueTemplateView(TemplateView):
    model = FamilyQueue
    template_name = 'main/familyqueue_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = FamilyQueue.objects.last()
        program_list, rating_limit = list(group.get_random_program())
        print(len(program_list))
        if len(program_list) >= 1:
            upper_range = len(program_list)-1
            print('upper range', upper_range)
            index_value = random.randint(0,upper_range)
            context['rating_limit'] = rating_limit
            context['random_program'] = program_list[index_value]
            return context
        else:
            pass


class AboutMeTemplateView(TemplateView):
    template_name = 'main/about_me.html'

def login_success(request):
    profile = Profile.objects.get(user=request.user)
    if profile.parent == None:
        if profile.email:
            return redirect('program_list_view')
        else:
            return redirect("profile_update_view")
    else:
        return redirect("program_list_view")
