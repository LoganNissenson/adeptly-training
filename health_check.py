"""
Health check view for Render.com
"""

from django.http import HttpResponse

def health_check(request):
    """Simple health check view"""
    return HttpResponse("Adeptly application is running!")
