from django.contrib import admin
from .models import Rank, Topic, UserTopicStats, Problem, TrainingSession, TopicExperienceEarned

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserTopicStats)
class UserTopicStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'experience', 'rank')
    list_filter = ('topic', 'rank')
    search_fields = ('user__username', 'topic__name')

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_topics', 'difficulty', 'estimated_time_to_complete')
    list_filter = ('topics', 'difficulty')
    filter_horizontal = ('topics', 'solved_by')
    search_fields = ('name', 'prompt')
    
    def get_topics(self, obj):
        return ", ".join([t.name for t in obj.topics.all()])
    get_topics.short_description = 'Topics'

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'completed_at', 'was_completed', 'correct_attempts', 'incorrect_attempts')
    list_filter = ('user', 'was_completed', 'created_at')
    filter_horizontal = ('problems', 'problems_completed', 'topics_covered')
    search_fields = ('user__username',)

@admin.register(TopicExperienceEarned)
class TopicExperienceEarnedAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'experience_earned', 'earned_at')
    list_filter = ('topic', 'user', 'earned_at')
    search_fields = ('user__username', 'topic__name')
