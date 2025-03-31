from django.db import models
from django.contrib.auth.models import User

class Rank(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserTopicStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_stats')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    experience = models.IntegerField(default=0)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} Stats"

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    ]
    
    name = models.CharField(max_length=200)
    topics = models.ManyToManyField(Topic, related_name='problems')
    prompt = models.TextField()
    choice_a = models.CharField(max_length=255)
    choice_b = models.CharField(max_length=255)
    choice_c = models.CharField(max_length=255)
    choice_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
    ])
    problem_diagram = models.ImageField(upload_to='problem_diagrams/', null=True, blank=True)
    solution_diagram = models.ImageField(upload_to='solution_diagrams/', null=True, blank=True)
    estimated_time_to_complete = models.IntegerField(help_text="Estimated time in minutes")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=3)
    solved_by = models.ManyToManyField(User, related_name='solved_problems', blank=True)
    
    def __str__(self):
        return self.name

class TrainingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_sessions')
    problems = models.ManyToManyField(Problem, related_name='training_sessions')
    estimated_time_to_complete = models.IntegerField(help_text="Estimated time in minutes")
    was_completed = models.BooleanField(default=False)
    correct_attempts = models.IntegerField(default=0)
    incorrect_attempts = models.IntegerField(default=0)
    problems_completed = models.ManyToManyField(Problem, related_name='completed_in_sessions', blank=True)
    topics_covered = models.ManyToManyField(Topic, related_name='covered_in_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Training Session for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class TopicExperienceEarned(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    experience_earned = models.IntegerField()
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} earned {self.experience_earned} in {self.topic.name}"
