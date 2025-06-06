import time
import logging
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import timezone
from collections import defaultdict


logger = logging.getLogger(__name__)  # get a logger for this module

# Store request counts: {ip: [(timestamp, count)]}
request_counts = defaultdict(list)
RATE_LIMIT = 5  #Maximum number of allowed requests
TIME_WINDOW = 60  #Seconds(1 minute)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("RequestLoggingMiddleware initialized.")
        
    def __call__(self, request):
        user = request.user
        logger.info(f"{time.time.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response

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
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("OffensiveLanguageMiddleware initialized.")
        
    def __call__(self, request):
            x_fowarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # If behind a proxy
            if x_fowarded_for:
                ip = x_fowarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
        
            # Only apply to POST requests to /api/messages/ (chat message creation)
            if request.method == 'POST' and request.path.startswith('/api/messages/'):
                current_time = time.time()
                
                # Remove requests older than TIME_WINDOW
                request_counts[ip] = [ts for ts in request_counts[ip] if current_time - ts < TIME_WINDOW]
                
                total_requests = len(request_counts[ip])
                logger.info(f"IP: {ip}, Total requests in window: {total_requests}")
                
                # Check if the current number of messages exceeds the limit
                if total_requests > RATE_LIMIT:
                    logger.warning(f"Rate limit exceeded for IP: {ip}")
                    return HttpResponse(
                        "Too many requests. Please try again later.",
                        status=429,
                        headers={"Retry-After": str(TIME_WINDOW)}
                    )
                   
                request_counts[ip].append(current_time) 
            
            response = self.get_response(request)
            return response