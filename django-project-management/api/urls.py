from django.conf.urls.defaults import *
from piston.authentication import HttpBasicAuthentication
from piston.resource import Resource
from projects.api_views import ProjectResourceHandler, ProjectListHandler, CompanyListHandler, \
        TeamManagersListHandler, NonTeamManagersListHandler, ResourcesListHandler
from risks.api_views import RiskResourceHandler, RiskListHandler, \
        UserRiskListHandler

auth = HttpBasicAuthentication(realm="My Realm")
ad = { 'authentication': auth }

# Handlers defined in projects.api_views
team_managers_handler = Resource(TeamManagersListHandler, **ad)
non_team_managers_handler = Resource(NonTeamManagersListHandler, **ad)
resources_handler = Resource(ResourcesListHandler, **ad)
project_handler = Resource(ProjectResourceHandler, **ad)
project_list_handler = Resource(ProjectListHandler, **ad)
company_list_handler = Resource(CompanyListHandler, **ad)

# Handlers defined in risks.api_views
risk_handler = Resource(RiskResourceHandler, **ad)
risk_list_handler = Resource(RiskListHandler, **ad)
user_risk_list_handler = Resource(UserRiskListHandler, **ad)

urlpatterns = patterns('',
    # URLs handled in projects.api_views
    (r'projects/(?P<project_number>[-\w\./\s]+)/team_managers/$', team_managers_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/non_team_managers/$', non_team_managers_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/resources/$', resources_handler),
    (r'projects/(?P<project_number>[-\w\./\s]+)/$', project_handler),
    (r'projects/$', project_list_handler),
    (r'companies/$', company_list_handler),

    # URLs handled in risks.api_views
    (r'risks/(?P<project_number>[-\w\./\s]+)/(?P<risk_number>[-\w\./\s]+)/$', risk_handler),
    (r'risks/(?P<project_number>[-\w\./\s]+)/$', risk_list_handler),
    (r'risks/$', user_risk_list_handler),

)
