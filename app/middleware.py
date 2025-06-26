from django.shortcuts import redirect
from django.urls import reverse
import re

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile the regex for admin URLs, excluding the login page
        self.admin_url_pattern = re.compile(r'^/admin/(?!login)')

    def __call__(self, request):
        # Check if the request path matches an admin URL and the user is not staff
        if self.admin_url_pattern.match(request.path) and not (request.user.is_authenticated and request.user.is_staff):
            # Redirect to admin login
            return redirect(reverse('admin_login') + '?next=' + request.path)
        
        return self.get_response(request)