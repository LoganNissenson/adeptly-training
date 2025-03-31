from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from adeptly.models import Topic, Rank, Problem

class Command(BaseCommand):
    help = 'Initialize Adeptly with default data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting initialization...')
        
        # Create default topics
        topics = [
            'HVAC Design',
            'HVAC Load Calculations',
            'Ductwork Design',
            'Refrigeration',
            'Energy Code Compliance',
            'Electrical Design',
            'Electrical Code Requirements',
            'Power Distribution',
            'Lighting Design',
            'Plumbing Systems',
            'Fire Protection',
            'Control Systems',
        ]
        
        created_topics = []
        for topic_name in topics:
            topic, created = Topic.objects.get_or_create(name=topic_name)
            created_topics.append(topic)
            if created:
                self.stdout.write(f'Created topic: {topic_name}')
            else:
                self.stdout.write(f'Topic already exists: {topic_name}')
        
        # Create ranks
        ranks = [
            'Beginner',
            'Intermediate',
            'Advanced',
            'Expert',
        ]
        
        for rank_name in ranks:
            rank, created = Rank.objects.get_or_create(name=rank_name)
            if created:
                self.stdout.write(f'Created rank: {rank_name}')
            else:
                self.stdout.write(f'Rank already exists: {rank_name}')
        
        # Create a sample problem
        if Problem.objects.count() == 0:
            problem = Problem.objects.create(
                name="Sample HVAC Duct Sizing Problem",
                prompt="A 30 ft long duct with a flow rate of 1,200 CFM needs to maintain a maximum friction rate of 0.08 in. wg per 100 ft. What is the appropriate duct diameter?",
                choice_a="10 inches",
                choice_b="12 inches",
                choice_c="14 inches",
                choice_d="16 inches",
                correct_answer="B",
                estimated_time_to_complete=5,
                difficulty=2
            )
            
            # Add topics to the problem
            hvac_design = Topic.objects.get(name='HVAC Design')
            ductwork_design = Topic.objects.get(name='Ductwork Design')
            problem.topics.add(hvac_design, ductwork_design)
            
            self.stdout.write('Created sample problem')
        
        self.stdout.write(self.style.SUCCESS('Initialization complete'))
