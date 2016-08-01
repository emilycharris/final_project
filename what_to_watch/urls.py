"""what_to_watch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main.views import IndexView, CreateParentView, ParentProfileUpdateView, ProgramListView, ProgramDetailView, QueueCreateView, QueueListView, FamilyQueueCreateView, FamilyQueueTemplateView, QueueProgramDeleteView, CreateChildView, ChildrenProfileListView, ChildProfileUpdateView, login_success
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^accounts/profile/$', login_required(ParentProfileUpdateView.as_view()), name="profile_update_view"),
    url(r'^program_list/$', login_required(ProgramListView.as_view()), name='program_list_view'),
    url(r'^program_detail/(?P<pk>\d+)/$', login_required(ProgramDetailView.as_view()), name='program_detail_view'),
    url(r'^queue_create/(?P<pk>\d+)/(?P<program_pk>\d+)/$', login_required(QueueCreateView.as_view()), name='queue_create_view'),
    url(r'^queue_list_view/$', login_required(QueueListView.as_view()), name='queue_list_view'),
    url(r'^queue_delete_view/(?P<pk>\d+)/$', login_required(QueueProgramDeleteView.as_view()), name='queue_program_delete_view'),
    url(r'^family_queue_create/$', login_required(FamilyQueueCreateView.as_view()), name='family_queue_create_view'),
    url(r'^family_queue/$', login_required(FamilyQueueTemplateView.as_view()), name='family_queue_template_view'),
    url(r'^sign_up/$', CreateParentView.as_view(), name='create_parent_view'),
    url(r'^sign_up_family/$', login_required(CreateChildView.as_view()), name='create_child_view'),
    url(r'^child_profile/(?P<pk>\d+)/$', login_required(ChildProfileUpdateView.as_view()), name='child_profile_update_view'),
    url(r'^children_profile_list/$', login_required(ChildrenProfileListView.as_view()), name='children_profile_list_view'),
    url(r'^login_success/$', login_success, name='login_success'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
