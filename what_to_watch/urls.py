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
from main.views import IndexView, CreateUserView, ProfileUpdateView, ProgramListView, ProgramDetailView, QueueUpdateView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^create_user/$', CreateUserView.as_view(), name='create_user_view'),
    url(r'^accounts/profile/$', login_required(ProfileUpdateView.as_view()), name="profile_update_view"),
    url(r'^program_list/$', ProgramListView.as_view(), name='program_list_view'),
    url(r'^program_detail/(?P<pk>\d+)/$', ProgramDetailView.as_view(), name='program_detail_view'),
    url(r'^queue_update/(?P<pk>\d+)/(?P<program_pk>\d+)/$', login_required(QueueUpdateView.as_view()), name='queue_update_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
