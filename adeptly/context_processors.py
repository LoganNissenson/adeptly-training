from django.conf import settings
from .models import Topic, UserTopicStats

def adeptly_context(request):
    """
    A context processor that provides app-wide context variables
    """
    context = {
        'app_name': 'Adeptly Training',
        'app_version': '1.0.0',
    }
    
    # Add user-specific data if user is logged in
    if request.user.is_authenticated:
        try:
            # Get user's top topics by experience
            top_topics = UserTopicStats.objects.filter(user=request.user).order_by('-experience')[:3]
            context['user_top_topics'] = top_topics
        except:
            # Handle the case where the user has no topic stats
            pass
    
    return context
