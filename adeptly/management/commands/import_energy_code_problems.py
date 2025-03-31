from django.core.management.base import BaseCommand
from adeptly.models import Problem, Topic
from django.db import transaction

class Command(BaseCommand):
    help = 'Import energy code and standards practice problems into the Adeptly app'
    
    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Importing energy code and standards problems into Adeptly...')
            
            # Get existing topics - handle possible duplicates
            topics = {}
            topic_names = [
                'HVAC Design',
                'Energy Code Compliance',
                'Control Systems',
            ]
            
            # Get the first instance of each topic (in case of duplicates)
            for topic_name in topic_names:
                topics[topic_name] = Topic.objects.filter(name=topic_name).first()
                if topics[topic_name] is None:
                    self.stdout.write(self.style.ERROR(f'Topic {topic_name} does not exist! Please run initialize_adeptly first.'))
                    return
            
            # Energy Code and Standards Problems
            energy_code_problems = [
                # ASHRAE 62.1 Ventilation Calculation Problems
                {
                    "name": "ASHRAE 62.1 - Ventilation Rate Procedure",
                    "topics": ['HVAC Design', 'Energy Code Compliance'],
                    "prompt": "A classroom space of 800 ft² has 25 students and 1 teacher. Using ASHRAE 62.1 Ventilation Rate Procedure, what is the minimum outdoor air requirement for this space? Assume the following: People outdoor air rate (Rp) = 10 cfm/person, Area outdoor air rate (Ra) = 0.12 cfm/ft², Zone air distribution effectiveness (Ez) = 1.0.",
                    "choice_a": "260 cfm",
                    "choice_b": "296 cfm",
                    "choice_c": "325 cfm",
                    "choice_d": "356 cfm",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 5,
                    "difficulty": 3
                },
                {
                    "name": "ASHRAE 62.1 - Multiple Zone Systems",
                    "topics": ['HVAC Design', 'Energy Code Compliance'],
                    "prompt": "An air handling system serves three zones with the following characteristics:\nZone 1: Voz = 500 cfm, Vpz = 2,000 cfm\nZone 2: Voz = 300 cfm, Vpz = 1,500 cfm\nZone 3: Voz = 400 cfm, Vpz = 1,200 cfm\nIf system ventilation efficiency (Ev) is 0.7, what is the outdoor air intake flow (Vot) required according to ASHRAE 62.1?",
                    "choice_a": "1,200 cfm",
                    "choice_b": "1,429 cfm",
                    "choice_c": "1,714 cfm",
                    "choice_d": "2,000 cfm",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                
                # Economizer Requirements Problems
                {
                    "name": "Economizer Requirements - System Size",
                    "topics": ['HVAC Design', 'Energy Code Compliance', 'Control Systems'],
                    "prompt": "According to ASHRAE 90.1-2019, in which of the following scenarios would an economizer NOT be required for a new HVAC system in climate zone 4A?",
                    "choice_a": "A 55,000 BTU/h packaged rooftop unit serving an office space",
                    "choice_b": "A 75,000 BTU/h split system serving a retail space",
                    "choice_c": "A 40,000 BTU/h heat pump serving a conference room",
                    "choice_d": "A 65,000 BTU/h water-source heat pump serving a classroom",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                {
                    "name": "Economizer Requirements - Climate Zones",
                    "topics": ['HVAC Design', 'Energy Code Compliance', 'Control Systems'],
                    "prompt": "Per ASHRAE 90.1-2019, economizers are NOT required for comfort cooling systems in which of the following climate zones, regardless of cooling capacity?",
                    "choice_a": "Climate Zone 1A (Miami, FL)",
                    "choice_b": "Climate Zone 3B (Las Vegas, NV)",
                    "choice_c": "Climate Zone 4A (New York, NY)",
                    "choice_d": "Climate Zone 5B (Denver, CO)",
                    "correct_answer": "A",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                
                # Boiler Efficiency Requirements Problems
                {
                    "name": "Boiler Efficiency - Gas-Fired Requirements",
                    "topics": ['HVAC Design', 'Energy Code Compliance'],
                    "prompt": "According to ASHRAE 90.1-2019, what is the minimum thermal efficiency required for a new 2,500,000 BTU/h gas-fired hot water boiler?",
                    "choice_a": "80%",
                    "choice_b": "82%",
                    "choice_c": "84%",
                    "choice_d": "86%",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                {
                    "name": "Boiler Efficiency - System Controls",
                    "topics": ['HVAC Design', 'Energy Code Compliance', 'Control Systems'],
                    "prompt": "Per ASHRAE 90.1-2019, which of the following control strategies is NOT required for a hydronic heating system with multiple boilers and a design output capacity exceeding 1,000,000 BTU/h?",
                    "choice_a": "Outdoor air temperature reset controls",
                    "choice_b": "Sequencing controls for staging multiple boilers",
                    "choice_c": "Automatic isolation valves for each boiler",
                    "choice_d": "Variable flow pumping with VFDs",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 5,
                    "difficulty": 4
                },
            ]
            
            # Add problems to database
            for problem_data in energy_code_problems:
                problem_topics = problem_data.pop('topics')
                
                # Create the problem
                problem = Problem.objects.create(**problem_data)
                
                # Add topics to the problem
                for topic_name in problem_topics:
                    topic = topics[topic_name]
                    problem.topics.add(topic)
                
                self.stdout.write(f'Added problem: {problem.name}')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(energy_code_problems)} energy code and standards problems to Adeptly'))
