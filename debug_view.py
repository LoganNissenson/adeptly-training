"""
Temporary debug view for diagnosing deployment issues
"""

from django.http import HttpResponse
import sys
import os

def debug_info(request):
    """Simple view to show debug information"""
    info = []
    info.append("<h1>Adeptly Debug Information</h1>")
    
    # Request details
    info.append("<h2>Request Information</h2>")
    info.append(f"<p>Method: {request.method}</p>")
    info.append(f"<p>Path: {request.path}</p>")
    info.append(f"<p>GET params: {request.GET}</p>")
    info.append(f"<p>Host: {request.get_host()}</p>")
    
    # Environment details
    info.append("<h2>Environment</h2>")
    info.append(f"<p>Python version: {sys.version}</p>")
    info.append(f"<p>Working directory: {os.getcwd()}</p>")
    
    # Settings check
    from django.conf import settings
    info.append("<h2>Django Settings</h2>")
    info.append(f"<p>DEBUG: {settings.DEBUG}</p>")
    info.append(f"<p>ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}</p>")
    info.append(f"<p>INSTALLED_APPS: {', '.join(settings.INSTALLED_APPS)}</p>")
    info.append(f"<p>STATIC_URL: {settings.STATIC_URL}</p>")
    info.append(f"<p>STATIC_ROOT: {settings.STATIC_ROOT}</p>")
    
    return HttpResponse("<br>".join(info))
