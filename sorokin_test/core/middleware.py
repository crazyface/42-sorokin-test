from models import RequestStore
import re


class RequestMiddleWare(object):
    def process_response(self, request, response):
        path = url=request.path
        if not re.match("^(/media|/admin|.*\.ico).*$", path):
            RequestStore.objects.create(
                               url=request.path,
                               req_get=request.GET,
                               req_post=request.POST,
                               req_cookies=request.COOKIES,
                               req_session=request.session,
                               req_meta=request.META,
                               res_status_code=response.status_code)
        return response
