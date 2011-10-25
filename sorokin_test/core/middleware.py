from models import RequestStore
import re

class RequestMiddleWare(object):
    object = None

    def process_request(self, request):
        print request
        path = url=request.path
        if not re.match("^(/media|/admin|.*\.ico).*$", path):
            self.object = RequestStore.objects.create(
                               url=request.path,
                               req_get=request.GET,
                               req_post=request.POST,
                               req_cookies=request.COOKIES,
                               req_session=request.session,
                               req_meta=request.META)

    
    def process_response(self, request, response):
        if self.object:
            self.object.res_status_code=response.status_code
            self.object.save()
        return response
