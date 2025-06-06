import datetime
import logging
from django.http import HttpResponseForbidden
from django.utils import timezone

logger = logging.getLogger(__name__)  # get a logger for this module

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("RequestLoggingMiddleware initialized.")
        
    def __call__(self, request):
        user = request.user
        logger.info(f"{datetime.datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    pass

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.start_hour = 9
        self.end_hour = 18
        
    def __call__(self, request):
        current_time = timezone.now()
        current_hour = current_time.hour
         
        if not (self.start_hour <= current_hour < self.end_hour):
            return HttpResponseForbidden("Access is allowed only between 9 AM and 5 PM server time. Please try again later.")
         
        # If within the allowed time, proceed to the next middleware or vie
        response = self.get_response(request)
        return response
          
         