"""
A manual migration script for Adeptly data.
Use this if the export/import scripts don't work.
"""

import os
import django
import sys

def main():
    print("Starting manual migration from SQLite to PostgreSQL...")
    
    # First, make sure we're using SQLite to read data
    os.environ['USE_SQLITE'] = 'true'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings')
    
    # Initialize Django
    django.setup()
    
    # Get data from SQLite
    print("Fetching data from SQLite...")
    
    # Import models
    from django.contrib.auth.models import User
    from adeptly.models import Topic, Rank, Problem, UserTopicStats, TrainingSession, TopicExperienceEarned
    
    # Get all data from each model
    users = list(User.objects.all().values())
    topics = list(Topic.objects.all().values())
    ranks = list(Rank.objects.all().values())
    problems = list(Problem.objects.all().values())
    user_topic_stats = list(UserTopicStats.objects.all().values())
    training_sessions = list(TrainingSession.objects.all().values())
    topic_experience_earned = list(TopicExperienceEarned.objects.all().values())
    
    # Get many-to-many relationships
    problem_topics = {}
    for problem in Problem.objects.all():
        problem_topics[problem.id] = list(problem.topics.all().values_list('id', flat=True))
    
    print(f"Found {len(users)} users")
    print(f"Found {len(topics)} topics")
    print(f"Found {len(ranks)} ranks")
    print(f"Found {len(problems)} problems")
    print(f"Found {len(user_topic_stats)} user topic stats")
    print(f"Found {len(training_sessions)} training sessions")
    print(f"Found {len(topic_experience_earned)} topic experience records")
    
    # Now switch to PostgreSQL for writing
    print("\nSwitching to PostgreSQL for data import...")
    
    # Remove SQLite setting to use PostgreSQL
    del os.environ['USE_SQLITE']
    
    # Reload Django with new settings
    for key in list(sys.modules.keys()):
        if key.startswith('django') or key.startswith('adeptly'):
            del sys.modules[key]
    
    # Reinitialize Django with PostgreSQL
    import django
    django.setup()
    
    # Import models again (as they were removed)
    from django.contrib.auth.models import User
    from adeptly.models import Topic, Rank, Problem, UserTopicStats, TrainingSession, TopicExperienceEarned
    
    # Check database connection
    from django.db import connection
    if connection.vendor != 'postgresql':
        print(f"❌ Error: Not connected to PostgreSQL! Current database: {connection.vendor}")
        return
    
    print("Connected to PostgreSQL successfully!")
    
    # Clear existing data in PostgreSQL
    print("Clearing existing data in PostgreSQL...")
    TopicExperienceEarned.objects.all().delete()
    TrainingSession.objects.all().delete()
    UserTopicStats.objects.all().delete()
    Problem.objects.all().delete()
    Rank.objects.all().delete()
    Topic.objects.all().delete()
    User.objects.all().delete()
    
    # Import data
    print("\nImporting data to PostgreSQL...")
    
    # Import users
    print("Importing users...")
    for user_data in users:
        user_id = user_data.pop('id')
        User.objects.create(id=user_id, **user_data)
    
    # Import topics
    print("Importing topics...")
    for topic_data in topics:
        topic_id = topic_data.pop('id')
        Topic.objects.create(id=topic_id, **topic_data)
    
    # Import ranks
    print("Importing ranks...")
    for rank_data in ranks:
        rank_id = rank_data.pop('id')
        Rank.objects.create(id=rank_id, **rank_data)
    
    # Import problems
    print("Importing problems...")
    for problem_data in problems:
        problem_id = problem_data.pop('id')
        problem = Problem.objects.create(id=problem_id, **problem_data)
        
        # Add topics to problem
        if problem_id in problem_topics:
            for topic_id in problem_topics[problem_id]:
                topic = Topic.objects.get(id=topic_id)
                problem.topics.add(topic)
    
    # Import user topic stats
    print("Importing user topic stats...")
    for stats_data in user_topic_stats:
        UserTopicStats.objects.create(**stats_data)
    
    # Import training sessions
    print("Importing training sessions...")
    for session_data in training_sessions:
        TrainingSession.objects.create(**session_data)
    
    # Import topic experience earned
    print("Importing topic experience earned...")
    for exp_data in topic_experience_earned:
        TopicExperienceEarned.objects.create(**exp_data)
    
    print("\n✅ Manual migration completed successfully!")
    print("Your PostgreSQL database should now contain all the data from SQLite.")
    print("You can now run the Django server with: python manage.py runserver")

if __name__ == "__main__":
    main()
