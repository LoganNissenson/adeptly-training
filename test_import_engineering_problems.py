#!/usr/bin/env python
import os
import sys
import django
from django.test import TestCase
from django.core.management import call_command
from django.db import connection
from io import StringIO
import unittest
from unittest.mock import patch
from django.db.models import Count

# Add the project directory to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(project_dir)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp_project.settings')
django.setup()

from adeptly.models import Problem, Topic, Rank

class ImportEngineeringProblemsTestCase(TestCase):
    """Test the import_engineering_problems management command"""
    
    def setUp(self):
        """Set up the test environment by creating necessary topics and ranks"""
        # Clean up any existing duplicate topics first
        self.cleanup_duplicate_topics()
        
        # Create test topics
        self.topics = [
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
        
        for topic_name in self.topics:
            # Only create if it doesn't exist
            if not Topic.objects.filter(name=topic_name).exists():
                Topic.objects.create(name=topic_name)
                print(f"Created topic: {topic_name}")
            else:
                print(f"Topic already exists: {topic_name}")
        
        # Create test ranks (needed for user topic stats if that's part of your model)
        rank_names = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
        for rank_name in rank_names:
            if not Rank.objects.filter(name=rank_name).exists():
                Rank.objects.create(name=rank_name)
    
    def cleanup_duplicate_topics(self):
        """Remove duplicate topics to prevent MultipleObjectsReturned error"""
        # Find topics with duplicate names
        duplicates = Topic.objects.values('name').annotate(
            count=Count('id')).filter(count__gt=1)
        
        for duplicate in duplicates:
            name = duplicate['name']
            print(f"Found duplicate topic: {name}")
            
            # Keep the first one, delete the rest
            topics = Topic.objects.filter(name=name).order_by('id')
            keep_id = topics.first().id
            
            # Delete all except the first one
            for topic in topics.exclude(id=keep_id):
                print(f"Deleting duplicate topic: {name} (ID: {topic.id})")
                topic.delete()
    
    def test_import_command(self):
        """Test that the import_engineering_problems command imports problems correctly"""
        # Count problems before import
        problems_before = Problem.objects.count()
        
        # Redirect stdout to capture command output
        out = StringIO()
        
        # Call the management command
        with patch('sys.stdout', new=out):
            call_command('import_engineering_problems')
        
        output = out.getvalue()
        print(output)  # Print the command's output for debugging
        
        # Count problems after import
        problems_after = Problem.objects.count()
        
        # Verify that 20 problems were added (total new problems created)
        self.assertEqual(problems_after - problems_before, 20)
        
        # The correct expected counts based on the import_engineering_problems.py file
        topic_problem_counts = {
            'HVAC Design': 7,  # Multiple problems assigned to this topic
            'HVAC Load Calculations': 1,
            'Ductwork Design': 1,
            'Refrigeration': 1,
            'Energy Code Compliance': 2,
            'Electrical Design': 10,    # All 10 electrical problems have this topic
            'Electrical Code Requirements': 3,
            'Power Distribution': 8, 
            'Control Systems': 1,
            'Lighting Design': 0,      # No problems with this topic
        }
        
        # Check that we have the expected number of problems for each topic
        for topic_name, expected_count in topic_problem_counts.items():
            # Get the topic - handle potential duplicates
            topic = Topic.objects.filter(name=topic_name).first()
            self.assertIsNotNone(topic, f"Topic '{topic_name}' not found")
            
            # Count problems associated with this topic
            actual_count = topic.problems.count()
            
            # Only check the problems added in this test run
            if topic.problems.exists():
                # Get the IDs of problems from this test run
                new_problem_ids = Problem.objects.filter(
                    id__gt=problems_before
                ).values_list('id', flat=True)
                
                # Count problems from this test run for this topic
                actual_count = topic.problems.filter(id__in=new_problem_ids).count()
            else:
                actual_count = 0
                
            self.assertEqual(
                actual_count, 
                expected_count, 
                f"Expected {expected_count} problems for topic '{topic_name}', but found {actual_count}"
            )
        
        # Verify some specific problems were created correctly
        hvac_problem = Problem.objects.filter(
            name="Psychrometrics - Mixed Air Conditions",
            id__gt=problems_before
        ).first()
        self.assertIsNotNone(hvac_problem, "HVAC problem not found")
        if hvac_problem:
            self.assertEqual(hvac_problem.correct_answer, "A")
            self.assertEqual(hvac_problem.estimated_time_to_complete, 6)
            self.assertEqual(hvac_problem.difficulty, 3)
        
        electrical_problem = Problem.objects.filter(
            name="Three-Phase Power Calculation",
            id__gt=problems_before
        ).first()
        self.assertIsNotNone(electrical_problem, "Electrical problem not found")
        if electrical_problem:
            self.assertEqual(electrical_problem.correct_answer, "B")
            self.assertEqual(electrical_problem.estimated_time_to_complete, 6)
            self.assertEqual(electrical_problem.difficulty, 2)
        
        # Check that a problem with multiple topics has all expected topics
        heat_transfer_problem = Problem.objects.filter(
            name="Heat Transfer - Composite Wall",
            id__gt=problems_before
        ).first()
        self.assertIsNotNone(heat_transfer_problem, "Heat Transfer problem not found")
        
        if heat_transfer_problem:
            heat_transfer_topics = heat_transfer_problem.topics.values_list('name', flat=True)
            self.assertIn('HVAC Design', heat_transfer_topics)
            self.assertIn('Energy Code Compliance', heat_transfer_topics)
        
        print("Test completed successfully! All import validations passed.")

if __name__ == '__main__':
    # Run the tests
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ImportEngineeringProblemsTestCase)
    test_result = unittest.TextTestRunner().run(test_suite)
    
    # Exit with appropriate status code
    sys.exit(not test_result.wasSuccessful())
