from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .simple_views import simple_home

urlpatterns = [
    # Simple test home page (temporary)
    path('simple/', simple_home, name='simple_home'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Training
    path('training/setup/', views.training_setup, name='training_setup'),
    path('training/session/<int:session_id>/problem/<int:problem_index>/', views.training_problem, name='training_problem'),
    path('training/session/<int:session_id>/results/', views.training_results, name='training_results'),
    
    # Problem management
    path('problems/', views.ProblemListView.as_view(), name='problem-list'),
    path('problems/new/', views.ProblemCreateView.as_view(), name='problem-create'),
    path('problems/<int:pk>/', views.problem_preview, name='problem-preview'),
    path('problems/<int:pk>/update/', views.ProblemUpdateView.as_view(), name='problem-update'),
    path('problems/<int:pk>/delete/', views.ProblemDeleteView.as_view(), name='problem-delete'),
    
    # Topic management
    path('topics/new/', views.TopicCreateView.as_view(), name='topic-create'),
    path('topics/<int:pk>/update/', views.TopicUpdateView.as_view(), name='topic-update'),
    path('topics/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic-delete'),
    
    # Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='adeptly/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]
