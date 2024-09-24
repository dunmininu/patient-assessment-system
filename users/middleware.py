from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        # Process the request here
        self.process_request(request)

        # Call the next middleware or view
        response = self.get_response(request)

        # Process the response here
        return response

    def process_request(self, request):
        if request.user.is_authenticated:
            request.tenant = request.user.tenant
        else:
            request.tenant = None
