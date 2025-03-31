from django.core.management.base import BaseCommand
from adeptly.models import Problem
from django.core.files.base import ContentFile
import os

class Command(BaseCommand):
    help = 'Update a problem with a diagram'
    
    def add_arguments(self, parser):
        parser.add_argument('problem_name', type=str, help='Name of the problem to update')
        parser.add_argument('diagram_filename', type=str, help='Filename of the diagram in the problem_diagrams folder')
    
    def handle(self, *args, **options):
        problem_name = options['problem_name']
        diagram_filename = options['diagram_filename']
        
        try:
            # Get the problem to update
            problem = Problem.objects.get(name=problem_name)
            
            # Path to the diagram file
            diagram_path = os.path.join("adeptly", "problem_diagrams", diagram_filename)
            
            # Check if file exists
            if not os.path.exists(diagram_path):
                self.stdout.write(self.style.ERROR(f'Diagram file not found at: {diagram_path}'))
                return
            
            # Open the file and add it to the problem
            with open(diagram_path, 'rb') as f:
                file_content = f.read()
                # If there's already a diagram, delete it first
                if problem.problem_diagram:
                    problem.problem_diagram.delete(save=False)
                
                problem.problem_diagram.save(diagram_filename, ContentFile(file_content), save=True)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully updated problem "{problem_name}" with diagram {diagram_filename}'))
            
        except Problem.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Problem "{problem_name}" not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating problem: {str(e)}'))
