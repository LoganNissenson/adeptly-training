from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.db.models import Sum, Count, Q, F, Value, IntegerField, Case, When

from .models import User, Topic, Problem, TrainingSession, UserTopicStats, TopicExperienceEarned, Rank
from .forms import ProblemForm, TrainingPreferencesForm, RegistrationForm, TopicForm

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'adeptly/register.html', {'form': form})

@login_required
def dashboard(request):
    """
    Main dashboard for the Adeptly application.
    Shows user stats, recent training, and navigation options.
    """
    user = request.user
    
    # Calculate user stats
    total_experience = UserTopicStats.objects.filter(user=user).aggregate(Sum('experience'))['experience__sum'] or 0
    
    # Calculate user's overall rank
    users_above = User.objects.annotate(
        total_experience=Sum('topic_stats__experience')
    ).filter(total_experience__gt=total_experience).count()
    user_rank = users_above + 1
    
    user_stats = {
        'total_experience': total_experience,
        'topics_trained': UserTopicStats.objects.filter(user=user).count(),
        'problems_solved': user.solved_problems.count(),
        'recent_sessions': user.training_sessions.order_by('-created_at')[:5],
        'rank': user_rank,
    }
    
    return render(request, 'adeptly/dashboard.html', {
        'user_stats': user_stats,
    })

@login_required
def training_setup(request):
    """
    View for setting up a custom training session.
    Users select topics, difficulty, and training time.
    """
    if request.method == 'POST':
        form = TrainingPreferencesForm(request.POST)
        if form.is_valid():
            # Create a new training session
            session = TrainingSession.objects.create(
                user=request.user,
                estimated_time_to_complete=form.cleaned_data['time_available']
            )
            
            # Add selected topics
            session.topics_covered.set(form.cleaned_data['topics'])
            
            # Select problems based on preferences
            problems = Problem.objects.filter(
                topics__in=form.cleaned_data['topics'],
                difficulty__in=form.cleaned_data['difficulty_levels']
            ).distinct()
            
            # Check if we have any problems matching the criteria
            if not problems.exists():
                session.was_completed = True
                session.completed_at = timezone.now()
                session.save()
                return redirect('training_results', session_id=session.id)
            
            # Limit problems based on available time
            avg_time_per_problem = problems.aggregate(avg=Sum('estimated_time_to_complete') / Count('id'))['avg'] or 5
            max_problems = int(form.cleaned_data['time_available'] / avg_time_per_problem)
            
            selected_problems = problems.order_by('?')[:max_problems]
            session.problems.set(selected_problems)
            session.save()
            
            return redirect('training_problem', session_id=session.id, problem_index=0)
    else:
        form = TrainingPreferencesForm()
    
    return render(request, 'adeptly/training_setup.html', {'form': form})

@login_required
def training_problem(request, session_id, problem_index):
    """
    View for displaying a problem during a training session.
    """
    session = get_object_or_404(TrainingSession, id=session_id, user=request.user)
    problems = list(session.problems.all())
    
    # Check if we've reached the end of the session or have an invalid index
    if problem_index >= len(problems) or problem_index < 0:
        session.was_completed = True
        session.completed_at = timezone.now()
        session.save()
        return redirect('training_results', session_id=session.id)
    
    current_problem = problems[problem_index]
    
    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        if selected_answer:
            is_correct = selected_answer == current_problem.correct_answer
            
            # Update session stats
            if is_correct:
                session.correct_attempts += 1
                
                # Mark problem as solved and add to completed problems
                if current_problem not in request.user.solved_problems.all():
                    request.user.solved_problems.add(current_problem)
                
                session.problems_completed.add(current_problem)
                
                # Award experience for each topic
                for topic in current_problem.topics.all():
                    # Calculate experience based on difficulty
                    exp_earned = current_problem.difficulty * 10
                    
                    # Record experience earned
                    TopicExperienceEarned.objects.create(
                        user=request.user,
                        topic=topic,
                        experience_earned=exp_earned,
                        training_session=session,
                        problem=current_problem
                    )
                    
                    # Update user topic stats
                    stat, created = UserTopicStats.objects.get_or_create(
                        user=request.user,
                        topic=topic,
                        defaults={
                            'rank': Rank.objects.get_or_create(name='Beginner')[0],
                            'experience': 0
                        }
                    )
                    
                    stat.experience += exp_earned
                    
                    # Update rank based on experience
                    if stat.experience >= 1000:
                        stat.rank = Rank.objects.get_or_create(name='Expert')[0]
                    elif stat.experience >= 500:
                        stat.rank = Rank.objects.get_or_create(name='Advanced')[0]
                    elif stat.experience >= 100:
                        stat.rank = Rank.objects.get_or_create(name='Intermediate')[0]
                    
                    stat.save()
            
            else:
                session.incorrect_attempts += 1
            
            session.save()
            
            # Move to the next problem
            return redirect('training_problem', session_id=session.id, problem_index=problem_index + 1)
    
    return render(request, 'adeptly/training_problem.html', {
        'problem': current_problem,
        'session': session,
        'problem_number': problem_index + 1,
        'total_problems': len(problems)
    })

@login_required
def training_results(request, session_id):
    """
    View for displaying the results of a completed training session.
    """
    session = get_object_or_404(TrainingSession, id=session_id, user=request.user)
    
    # Calculate statistics
    total_problems = session.problems.count()
    correct = session.correct_attempts
    accuracy = (correct / total_problems * 100) if total_problems > 0 else 0
    
    # Prepare context variables
    context = {
        'session': session,
        'total_problems': total_problems,
        'correct': correct,
        'accuracy': accuracy,
    }
    
    # If there are no problems, we don't need to calculate experience
    if total_problems == 0:
        context['total_exp_earned'] = 0
        context['experience_breakdown'] = []
        return render(request, 'adeptly/training_results.html', context)
    
    # Calculate total experience earned
    experience_breakdown = TopicExperienceEarned.objects.filter(
        training_session=session
    ).values('topic__name').annotate(total_exp=Sum('experience_earned'))
    
    total_exp_earned = TopicExperienceEarned.objects.filter(
        training_session=session
    ).aggregate(Sum('experience_earned'))['experience_earned__sum'] or 0
    
    context['experience_breakdown'] = experience_breakdown
    context['total_exp_earned'] = total_exp_earned
    
    return render(request, 'adeptly/training_results.html', context)

class ProblemListView(LoginRequiredMixin, ListView):
    """
    View for listing and managing training problems.
    """
    model = Problem
    template_name = 'adeptly/problem_list.html'
    context_object_name = 'problems'
    
    def get_queryset(self):
        queryset = Problem.objects.all()
        
        # Apply filters if present
        topic = self.request.GET.get('topic')
        difficulty = self.request.GET.get('difficulty')
        
        if topic:
            queryset = queryset.filter(topics__id=topic)
        
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['difficulty_levels'] = Problem.DIFFICULTY_CHOICES
        context['topic_form'] = TopicForm()
        return context

class ProblemCreateView(LoginRequiredMixin, CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'adeptly/problem_form.html'
    success_url = reverse_lazy('problem-list')

class ProblemUpdateView(LoginRequiredMixin, UpdateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'adeptly/problem_form.html'
    success_url = reverse_lazy('problem-list')

class ProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = Problem
    template_name = 'adeptly/problem_confirm_delete.html'
    success_url = reverse_lazy('problem-list')


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'adeptly/topic_form.html'
    success_url = reverse_lazy('problem-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # If AJAX request, return JSON response
            return JsonResponse({
                'success': True,
                'id': self.object.id,
                'name': self.object.name
            })
        return response


class TopicUpdateView(LoginRequiredMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = 'adeptly/topic_form.html'
    success_url = reverse_lazy('problem-list')


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'adeptly/topic_confirm_delete.html'
    success_url = reverse_lazy('problem-list')
    
    def post(self, request, *args, **kwargs):
        topic = self.get_object()
        
        # Check if the topic is used in any problems
        if topic.problems.exists():
            return render(request, 'adeptly/topic_in_use.html', {
                'topic': topic,
                'problem_count': topic.problems.count()
            })
        
        return super().post(request, *args, **kwargs)

@login_required
def problem_preview(request, pk):
    """
    View for previewing a problem as it would appear in a training session.
    """
    problem = get_object_or_404(Problem, id=pk)
    
    return render(request, 'adeptly/problem_preview.html', {
        'problem': problem
    })

@login_required
def leaderboard(request):
    """
    View for displaying user rankings based on experience points.
    Shows overall leaderboard and topic-specific leaderboards.
    """
    # Get all topics
    topics = Topic.objects.all()
    
    # Get the selected topic filter (if any)
    selected_topic_id = request.GET.get('topic', None)
    selected_topic = None
    
    if selected_topic_id:
        try:
            selected_topic = Topic.objects.get(id=selected_topic_id)
        except (Topic.DoesNotExist, ValueError):
            pass
    
    # Overall leaderboard - users ranked by total experience
    overall_leaderboard = User.objects.annotate(
        total_experience=Sum('topic_stats__experience')
    ).filter(total_experience__isnull=False).order_by('-total_experience')[:10]
    
    # Topic-specific leaderboard
    if selected_topic:
        topic_leaderboard = UserTopicStats.objects.filter(
            topic=selected_topic
        ).select_related('user', 'rank').order_by('-experience')[:10]
    else:
        topic_leaderboard = None
    
    # Get user's rank in the overall leaderboard (if logged in)
    user_rank = None
    if request.user.is_authenticated:
        user_total_exp = UserTopicStats.objects.filter(user=request.user).aggregate(Sum('experience'))['experience__sum'] or 0
        # Count users with more experience than the current user
        users_above = User.objects.annotate(
            total_experience=Sum('topic_stats__experience')
        ).filter(total_experience__gt=user_total_exp).count()
        
        # User's rank is the number of users with more experience + 1
        user_rank = users_above + 1
    
    # Get user's rank in the topic-specific leaderboard (if applicable)
    user_topic_rank = None
    user_topic_stats = None
    if request.user.is_authenticated and selected_topic:
        # Use a flag to track if we found the user's stats for this topic
        user_has_topic_stats = False
        
        # Get all user's stats for all topics
        user_topic_stats = UserTopicStats.objects.filter(
            user=request.user
        )
        
        # Check if the user has stats for the selected topic
        for stat in user_topic_stats:
            if stat.topic_id == selected_topic.id:
                user_has_topic_stats = True
                user_experience = stat.experience
                break
        
        # Count users with more experience in this topic only if the user has stats
        if user_has_topic_stats:
            users_above_topic = UserTopicStats.objects.filter(
                topic=selected_topic,
                experience__gt=user_experience
            ).count()
            
            # User's topic rank is the number of users with more experience + 1
            user_topic_rank = users_above_topic + 1
    
    # Get some additional stats for the leaderboard
    total_users_with_exp = User.objects.annotate(
        total_experience=Sum('topic_stats__experience')
    ).filter(total_experience__gt=0).count()
    
    # Find the most popular topic based on number of stats entries
    topic_popularity = UserTopicStats.objects.values('topic__name').annotate(
        users_count=Count('user', distinct=True)
    ).order_by('-users_count').first()
    
    most_popular_topic = topic_popularity['topic__name'] if topic_popularity else None
    
    # Find the top user's experience
    top_user_exp = UserTopicStats.objects.values('user').annotate(
        total_exp=Sum('experience')
    ).order_by('-total_exp').first()
    
    top_exp = top_user_exp['total_exp'] if top_user_exp else 0
    
    return render(request, 'adeptly/leaderboard.html', {
        'overall_leaderboard': overall_leaderboard,
        'topic_leaderboard': topic_leaderboard,
        'topics': topics,
        'selected_topic': selected_topic,
        'user_rank': user_rank,
        'user_topic_rank': user_topic_rank,
        'user_topic_stats': user_topic_stats,
        'total_users_with_exp': total_users_with_exp,
        'most_popular_topic': most_popular_topic,
        'top_exp': top_exp,
    })
