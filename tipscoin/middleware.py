from django.http import HttpResponseForbidden   
from django.utils.deprecation import MiddlewareMixin 

class RejectSpambotRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request): 
        whitelist = ['tipcoinapi.herokuapp.com', 'tipscoinapi.herokuapp.com']
        referer = request.headers['Referer']
        print(referer)
        for i in whitelist:
            if i in referer:
                return  # reject the request and return 403 forbidden response

        return HttpResponseForbidden() # return None in case of a valid request