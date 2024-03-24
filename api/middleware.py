import logging

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request data
        logging.info(f"Request: {request.method} {request.path}, Body: {request.body}, Headers: {request.headers}")
        
        # Pass the request to the next middleware or view
        response = self.get_response(request)

        return response
