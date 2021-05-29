from django.http import HttpResponseForbidden   
from django.utils.deprecation import MiddlewareMixin 

class RejectSpambotRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request): 
        print("hre") 
        referer = request.META.get('SERVER_NAME', None)
        print(referer)
        if referer == 'spambot_site_referer':
            return HttpResponseForbidden() # reject the request and return 403 forbidden response

        return # return None in case of a valid request