from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from projects.api_views import ProjectResourceHandler, ProjectListHandler, CompanyListHandler, \
        TeamManagersListHandler, NonTeamManagersListHandler, ResourcesListHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }


team_managers_handler = Resource(TeamManagersListHandler, **ad)
non_team_managers_handler = Resource(NonTeamManagersListHandler, **ad)
resources_handler = Resource(ResourcesListHandler, **ad)
project_handler = Resource(ProjectResourceHandler, **ad)
project_list_handler = Resource(ProjectListHandler, **ad)
company_list_handler = Resource(CompanyListHandler, **ad)


urlpatterns = patterns('',
    # URLs handled in projects.api_views
    (r'projects/(?P<project_number>[-\w\./\s]+)/team_managers/$', team_managers_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/non_team_managers/$', non_team_managers_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/resources/$', resources_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/$', project_handler),
    (r'projects/$', project_list_handler),
    (r'companies/$', company_list_handler),


)
