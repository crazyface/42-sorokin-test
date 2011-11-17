from models import RequestStore


class RequestMiddleWare(object):

    def process_request(self, request):
        self.object = None
        self.object = RequestStore.objects.create(url=request.path,
                                                  req_get=request.GET,
                                                  req_post=request.POST,
                                                  req_cookies=request.COOKIES,
                                                  req_session=request.session,
                                                  req_meta=request.META)

    def process_response(self, request, response):
        if self.object:
            self.object.req_status_code = response.status_code
            self.object.save()
        return response
