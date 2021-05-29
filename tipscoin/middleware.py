from django.http import HttpResponseForbidden   
from django.utils.deprecation import MiddlewareMixin 

class RejectSpambotRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request): 
        referer = request.META.get('HTTP_X_FORWARDED_FOR', None)
        print('HTTP_X_FORWARDED_FOR')
        print(referer)
        if referer == 'tipcoinapi.herokuapp.com' or referer == 'tipscoinapi.herokuapp.com':
            return  # reject the request and return 403 forbidden response

        return HttpResponseForbidden() # return None in case of a valid request