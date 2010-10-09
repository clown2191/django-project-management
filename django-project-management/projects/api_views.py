import logging

from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended, validate
import settings

from projects.models import *
from projects.forms import EditPID

if settings.DEBUG:
    log = logging.getLogger('projects-api-views')
    log.setLevel(logging.DEBUG)
    h = logging.StreamHandler()
    f = logging.Formatter("%(levelname)s %(asctime)s module=%(module)s fn=%(funcName)s() line=%(lineno)d msg=%(message)s")
    h.setFormatter(f)
    log.addHandler(h)
else:
    log.setLevel(logging.NOTSET)


class ProjectResourceHandler(BaseHandler):
    """
    URI: /api/projects/%project_number%/
    VERBS: GET, PUT, DELETE

    Handles a single instance of Project
    """

    allowed_methods = ('GET', 'PUT', 'DELETE')
    model = Project

    def read(self, request, project_number):
        """ View a project """

        log.debug("GET request from user %s for project number %s" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)
        return proj

    def update(self, request, project_number):
        """ Update the project """

        log.debug("PUT request from user %s for project number %s" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)
        log.debug("Fetched object from database %s" % proj)
        form = EditPID(request.POST, instance=proj)
        if form.is_valid():
            t = form.save()
            if request.POST.get('team_managers_placeholder'):
                for id in request.POST['team_managers_placeholder'].split(','):
                    t.team_managers.add(id)
            log.debug('Saving %s back to database' % t)
            t.save()
            return t
        else:
            resp = rc.BAD_REQUEST
            resp.write(form.errors)
            log.debug('Validation errors with %s' % t)
            t.save()
            return resp

    def delete(self, request, project_number):
        """ Put the project into archived state, not actually delete it """

        log.debug("PUT request from user %s for project number %s" % ( request.user, project_number ))
        proj = Project.objects.get(project_number=project_number)
        log.debug("Fetched object from database %s" % proj)
        proj.project_status = 5
        proj.save()
        log.debug("Archived project %s" % proj)
        return rc.ALL_OK





class ProjectListHandler(BaseHandler):
    """ 
    URI: /api/projects/
    VERBS: GET, PUT

    Returns a list of projects the user is allowed to see
    """

    allowed_methods  = ('GET', 'POST')
    models = Project

    @validate(EditPID)
    def create(self, request):
        """ Create a new Project """

        log.debug("POST request from user %s to create a new project"% request.user)

        # Only users with the create_project permission can do this
        if 'projects.can_create_project' not in request.user.get_all_permissions():
            log.debug('User %s is not allowed to create projects, DENIED' % request.user)
            return rc.FORBIDDEN

        # Go ahead and create the project....
        form = EditPID(request.POST)
        t = form.save()
        return t


    def read(self, request):
        """ Return a list of projects filtered by ACL """

        log.debug("GET request from user %s for project list" % request.user)
        projects = Project.objects.filter(active=True, read_acl__in=request.user.groups.all()).exclude(project_status=5).distinct()
        return projects
