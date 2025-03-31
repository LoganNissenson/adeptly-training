from django.core.management.base import BaseCommand
from adeptly.models import Problem, Topic
from django.db import transaction

class Command(BaseCommand):
    help = 'Import HVAC control systems practice problems into the Adeptly app'
    
    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Importing HVAC control systems problems into Adeptly...')
            
            # Get existing topics - handle possible duplicates
            topics = {}
            topic_names = [
                'HVAC Design',
                'Control Systems',
                'Energy Code Compliance',
                'HVAC Load Calculations',
            ]
            
            # Get the first instance of each topic (in case of duplicates)
            for topic_name in topic_names:
                topics[topic_name] = Topic.objects.filter(name=topic_name).first()
                if topics[topic_name] is None:
                    self.stdout.write(self.style.ERROR(f'Topic {topic_name} does not exist! Please run initialize_adeptly first.'))
                    return
            
            # HVAC Control Systems Problems
            control_problems = [
                {
                    "name": "Analog vs Binary Control Points",
                    "topics": ['Control Systems', 'HVAC Design'],
                    "prompt": "In a building automation system controlling an air handling unit, which of the following is NOT a typical application for an analog control point?",
                    "choice_a": "Variable frequency drive speed control",
                    "choice_b": "Discharge air temperature sensor",
                    "choice_c": "Fire alarm system status",
                    "choice_d": "Chilled water valve modulation",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 3,
                    "difficulty": 2
                },
                {
                    "name": "PID Controller Tuning",
                    "topics": ['Control Systems'],
                    "prompt": "A PID controller is being tuned for a VAV box with a 6-second actuator stroke time. The system exhibits sluggish response with significant overshoot. Which of the following control parameter adjustments would most effectively address this issue?",
                    "choice_a": "Increase the proportional gain and decrease the integral time",
                    "choice_b": "Decrease the proportional gain and increase the integral time",
                    "choice_c": "Increase both the proportional gain and derivative time",
                    "choice_d": "Decrease the proportional gain and increase the derivative time",
                    "correct_answer": "D",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                {
                    "name": "DDC System Architecture",
                    "topics": ['Control Systems', 'HVAC Design'],
                    "prompt": "In a multi-building campus BAS (Building Automation System) using BACnet, you need to design the network architecture. The system will have 12 buildings, each with approximately 1,500 points. Which network topology would be most appropriate?",
                    "choice_a": "Single flat network with all controllers as BACnet IP devices",
                    "choice_b": "Hierarchical system with BACnet IP backbone and MS/TP subnetworks",
                    "choice_c": "Star topology with a central server directly controlling all field devices",
                    "choice_d": "Peer-to-peer network using only BACnet MS/TP throughout",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 5,
                    "difficulty": 4
                },
                {
                    "name": "Variable Flow System Analysis",
                    "topics": ['Control Systems', 'HVAC Design'],
                    "prompt": "A variable primary flow chilled water system with three chillers (500 tons each) is experiencing unstable operation during low-load conditions. The system has a minimum flow requirement of 20% of design flow. Which control strategy would best improve stable operation at low loads?",
                    "choice_a": "Install a bypass valve with flow meter controlled to maintain minimum flow",
                    "choice_b": "Implement a control algorithm to stage chillers based only on return water temperature",
                    "choice_c": "Install three-way valves on all coils instead of two-way valves",
                    "choice_d": "Operate all three chillers simultaneously at partial load",
                    "correct_answer": "A",
                    "estimated_time_to_complete": 5,
                    "difficulty": 4
                },
                {
                    "name": "Damper Control Sequencing",
                    "topics": ['Control Systems', 'Energy Code Compliance'],
                    "prompt": "For an air-handling unit with an economizer, both the minimum outside air damper and the economizer damper are fully open, but the return air damper is only partially open. What is the most likely system operating condition?",
                    "choice_a": "Free cooling mode with outdoor air temperature between return air and supply air setpoint",
                    "choice_b": "Mechanical cooling mode with 100% outdoor air required for IAQ",
                    "choice_c": "Mixed air temperature control with high cooling demand",
                    "choice_d": "Economizer fault with stuck outdoor air damper",
                    "correct_answer": "A",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                {
                    "name": "Chiller Plant Optimization",
                    "topics": ['Control Systems', 'Energy Code Compliance'],
                    "prompt": "A chiller plant has four identical 350-ton chillers with varying efficiency curves. The plant operates under partial load conditions 85% of the time. Which control strategy would provide the best annual energy efficiency?",
                    "choice_a": "Base-loading the most efficient chiller and sequentially staging the others",
                    "choice_b": "Equal load sharing among all operating chillers",
                    "choice_c": "Operating chillers based on real-time efficiency monitoring to minimize total kW/ton",
                    "choice_d": "Running chillers in a rotating schedule to equalize run hours",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 5,
                    "difficulty": 4
                },
                {
                    "name": "VAV Terminal Unit Control",
                    "topics": ['Control Systems', 'HVAC Design'],
                    "prompt": "A pressure-independent VAV terminal unit with a reheat coil is exhibiting unstable control. The space temperature oscillates ±3°F around setpoint, and the damper position constantly adjusts. What is the most likely cause of this issue?",
                    "choice_a": "Oversized terminal unit flow sensor",
                    "choice_b": "Improper PID loop tuning parameters",
                    "choice_c": "Undersized reheat coil valve",
                    "choice_d": "Insufficient supply air temperature",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                {
                    "name": "Control Valve Sizing",
                    "topics": ['Control Systems', 'HVAC Design'],
                    "prompt": "A heating hot water coil needs to deliver 200,000 BTU/hr with 180°F water and a 30°F temperature drop. The system operates at 25 psi differential pressure. What is the proper control valve Cv value for this application?",
                    "choice_a": "1.8",
                    "choice_b": "3.2",
                    "choice_c": "4.7",
                    "choice_d": "6.5",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                {
                    "name": "Demand Control Ventilation",
                    "topics": ['Control Systems', 'Energy Code Compliance', 'HVAC Load Calculations'],
                    "prompt": "A conference room designed for 50 occupants uses CO2-based demand control ventilation. The room has a ventilation requirement of 15 CFM per person and a base ventilation rate of 0.06 CFM/ft² for building components. The room is 1,000 ft². If the outdoor CO2 level is 400 ppm and the indoor CO2 setpoint is 1,000 ppm, what should the target maximum CO2 differential be for controlling the outdoor air damper?",
                    "choice_a": "400 ppm",
                    "choice_b": "600 ppm",
                    "choice_c": "800 ppm",
                    "choice_d": "1,000 ppm",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 5,
                    "difficulty": 4
                },
                {
                    "name": "Fault Detection and Diagnostics",
                    "topics": ['Control Systems', 'HVAC Design'],
                    "prompt": "A building automation system with fault detection capabilities reports that the cooling coil valve is commanded 100% open, but the leaving air temperature is not decreasing. The air handling unit uses chilled water for cooling. Which of the following is NOT a potential cause of this fault?",
                    "choice_a": "Air trapped in the cooling coil",
                    "choice_b": "Failed valve actuator",
                    "choice_c": "Chilled water pump failure",
                    "choice_d": "Dirty air filters",
                    "correct_answer": "D",
                    "estimated_time_to_complete": 4,
                    "difficulty": 3
                },
                {
                    "name": "Control System Communication Protocols",
                    "topics": ['Control Systems'],
                    "prompt": "A project requires integration of multiple building systems including HVAC, lighting, and access control into a single management platform. The HVAC system uses BACnet MS/TP, the lighting control system uses DALI, and the access control system uses Modbus TCP. What is the most appropriate integration method?",
                    "choice_a": "Convert all systems to use Modbus RTU",
                    "choice_b": "Install gateways to translate protocols to BACnet IP and use it as the integration platform",
                    "choice_c": "Implement a proprietary protocol converter for each subsystem",
                    "choice_d": "Replace all controllers with dual-protocol devices",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 5,
                    "difficulty": 4
                },
            ]
            
            # Add problems to database
            for problem_data in control_problems:
                problem_topics = problem_data.pop('topics')
                
                # Create the problem
                problem = Problem.objects.create(**problem_data)
                
                # Add topics to the problem
                for topic_name in problem_topics:
                    topic = topics[topic_name]
                    problem.topics.add(topic)
                
                self.stdout.write(f'Added problem: {problem.name}')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(control_problems)} HVAC control systems problems to Adeptly'))
