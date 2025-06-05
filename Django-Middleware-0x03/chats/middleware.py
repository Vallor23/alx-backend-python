import datetime
import logging

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