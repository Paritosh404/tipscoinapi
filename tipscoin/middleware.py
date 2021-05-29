from django.http import HttpResponseForbidden   
from django.utils.deprecation import MiddlewareMixin 

class RejectSpambotRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request): 
        whitelist1 = 'tipcoinapi.herokuapp.com'
        whitelist2 = 'tipzcoin.herokuapp.com'
        referer = request.headers['Referer']
        if whitelist1 in referer or whitelist2 in referer:
            return  # reject the request and return 403 forbidden response

        return HttpResponseForbidden() # return None in case of a valid request