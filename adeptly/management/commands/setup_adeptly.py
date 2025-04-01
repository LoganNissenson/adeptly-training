from django.core.management.base import BaseCommand
from django.core.management import call_command
from adeptly.models import Topic, Problem

class Command(BaseCommand):
    help = 'Sets up Adeptly by running initialization commands and importing problems'

    def handle(self, *args, **options):
        # Check if we need to initialize the app
        if Topic.objects.count() == 0:
            self.stdout.write(self.style.WARNING('No topics found. Running initialize_adeptly...'))
            try:
                call_command('initialize_adeptly')
                self.stdout.write(self.style.SUCCESS('Successfully initialized Adeptly!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error initializing Adeptly: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Topics already exist, skipping initialization.'))

        # Check if we need to import engineering problems
        if Problem.objects.count() == 0:
            self.stdout.write(self.style.WARNING('No problems found. Running import_engineering_problems...'))
            try:
                call_command('import_engineering_problems')
                self.stdout.write(self.style.SUCCESS('Successfully imported engineering problems!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error importing problems: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Problems already exist, skipping import.'))
            
        self.stdout.write(self.style.SUCCESS('Adeptly setup complete!'))
