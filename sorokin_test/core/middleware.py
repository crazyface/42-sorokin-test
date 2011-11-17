from models import RequestStore


class RequestMiddleWare(object):
    curr_req = None

    def process_request(self, request):
        self.curr_req = RequestStore.objects.create(url=request.path,
                                                  req_get=request.GET,
                                                  req_post=request.POST,
                                                  req_cookies=request.COOKIES,
                                                  req_session=request.session,
                                                  req_meta=request.META)

    def process_response(self, request, response):
        if self.curr_req:
            self.curr_req.req_status_code = response.status_code
            self.curr_req.save()
        return response
