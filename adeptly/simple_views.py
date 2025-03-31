"""
Simplified views for Adeptly to help diagnose deployment issues
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.html import escape

def simple_home(request):
    """A very simple home page for testing"""
    return HttpResponse("""
    <html>
        <head>
            <title>Adeptly - Training Platform for MEP Engineers</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                .container { max-width: 800px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Adeptly</h1>
                <p>The training platform for MEP engineering professionals.</p>
                <p>If you can see this page, the basic application is working!</p>
                <p>Try these other test pages:</p>
                <ul>
                    <li><a href="/health/">Health check</a></li>
                    <li><a href="/debug/">Debug information</a></li>
                </ul>
            </div>
        </body>
    </html>
    """)
