from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from projects.api_views import ProjectResourceHandler, ProjectListHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }


project_handler = Resource(ProjectResourceHandler, **ad)
project_list_handler = Resource(ProjectListHandler, **ad)


urlpatterns = patterns('',
    (r'projects/(?P<project_number>[-\w\./\s]+)/$', project_handler),
    (r'projects/$', project_list_handler),
)
