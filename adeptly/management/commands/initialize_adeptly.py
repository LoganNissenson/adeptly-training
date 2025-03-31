from django.core.management.base import BaseCommand
from adeptly.models import Topic, Rank
from django.db import transaction

class Command(BaseCommand):
    help = 'Initialize Adeptly with basic data like topics and ranks'
    
    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Initializing Adeptly application with basic data...')
            
            # Create topics if they don't exist
            topic_names = [
                'HVAC Design',
                'HVAC Load Calculations',
                'Ductwork Design',
                'Refrigeration',
                'Energy Code Compliance',
                'Electrical Design',
                'Electrical Code Requirements',
                'Power Distribution',
                'Lighting Design',
                'Control Systems',
            ]
            
            for topic_name in topic_names:
                topic, created = Topic.objects.get_or_create(name=topic_name)
                if created:
                    self.stdout.write(f'Created topic: {topic_name}')
                else:
                    self.stdout.write(f'Topic already exists: {topic_name}')
            
            # Create ranks if they don't exist
            rank_names = [
                'Beginner',
                'Intermediate',
                'Advanced',
                'Expert',
            ]
            
            for rank_name in rank_names:
                rank, created = Rank.objects.get_or_create(name=rank_name)
                if created:
                    self.stdout.write(f'Created rank: {rank_name}')
                else:
                    self.stdout.write(f'Rank already exists: {rank_name}')
            
            self.stdout.write(self.style.SUCCESS('Successfully initialized Adeptly!'))
