from django.http import HttpResponseForbidden   
from django.utils.deprecation import MiddlewareMixin 

class RejectSpambotRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request): 
        whitelist1 = 'tipcoinapi.herokuapp.com'
        whitelist2 = 'tipzcoin.herokuapp.com'
        try:
            referer = request.headers['Referer']
        except:
            referer = request.headers['Host']
            if referer in whitelist1 or referer in whitelist2:
                return
            else:
                return HttpResponseForbidden()
        if whitelist1 in referer or whitelist2 in referer:
            return 
        else:
            return HttpResponseForbidden()
