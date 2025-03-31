from django.core.management.base import BaseCommand
from adeptly.models import Topic
from django.db import transaction

class Command(BaseCommand):
    help = 'Add default topics to the Adeptly app'
    
    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Adding default topics to Adeptly...')
            
            # Define default topics
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
            
            # Add each topic if it doesn't exist
            topics_created = 0
            for topic_name in topic_names:
                topic, created = Topic.objects.get_or_create(name=topic_name)
                if created:
                    topics_created += 1
                    self.stdout.write(f'Created topic: {topic_name}')
                else:
                    self.stdout.write(f'Topic already exists: {topic_name}')
            
            # Create success message
            if topics_created > 0:
                success_message = f'Successfully added {topics_created} new topics to Adeptly!'
            else:
                success_message = 'No new topics needed to be added (all already exist).'
            
            self.stdout.write(self.style.SUCCESS(success_message))
