from django.core.management.base import BaseCommand
from adeptly.models import Problem, Topic
from django.db import transaction

class Command(BaseCommand):
    help = 'Import engineering practice problems into the Adeptly app'
    
    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write('Importing engineering problems into Adeptly...')
            
            # Get existing topics - handle possible duplicates
            topics = {}
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
            
            # Get the first instance of each topic (in case of duplicates)
            for topic_name in topic_names:
                topics[topic_name] = Topic.objects.filter(name=topic_name).first()
                if topics[topic_name] is None:
                    self.stdout.write(self.style.ERROR(f'Topic {topic_name} does not exist! Please run initialize_adeptly first.'))
                    return
            
            # HVAC & Refrigeration PE Exam Problems
            hvac_problems = [
                {
                    "name": "Psychrometrics - Mixed Air Conditions",
                    "topics": ['HVAC Design'],
                    "prompt": "A HVAC system mixes outside air at 95°F dry-bulb temperature and 78°F wet-bulb temperature with return air at 75°F dry-bulb temperature and 50% relative humidity. The mixed air is 30% outside air by volume. Assuming standard atmospheric pressure, what is the mixed air dry-bulb temperature?",
                    "choice_a": "81°F",
                    "choice_b": "83°F",
                    "choice_c": "85°F",
                    "choice_d": "87°F",
                    "correct_answer": "A",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Heating Load Calculation",
                    "topics": ['HVAC Load Calculations'],
                    "prompt": "A rectangular room has dimensions of 15 ft × 20 ft with a ceiling height of 9 ft. The room has two exterior walls with 50 ft² of windows (U-value = 0.35 BTU/hr·ft²·°F) and 250 ft² of wall area (U-value = 0.08 BTU/hr·ft²·°F). The indoor design temperature is 72°F, and the outdoor design temperature is 10°F. Assuming an infiltration rate of 0.5 air changes per hour and neglecting internal heat gains, what is the approximate heating load for the room?",
                    "choice_a": "4,500 BTU/hr",
                    "choice_b": "6,700 BTU/hr",
                    "choice_c": "8,900 BTU/hr",
                    "choice_d": "11,200 BTU/hr",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Refrigeration Cycle Analysis",
                    "topics": ['Refrigeration'],
                    "prompt": "A vapor-compression refrigeration system operates with R-134a refrigerant. The following conditions are known: Evaporator temperature: 35°F, Condenser temperature: 110°F, Compressor isentropic efficiency: 80%, Refrigerant leaves the condenser as saturated liquid, Refrigerant enters the compressor as saturated vapor, Cooling load: 5 tons. What is the approximate coefficient of performance (COP) of the cycle?",
                    "choice_a": "2.1",
                    "choice_b": "3.2",
                    "choice_c": "4.3",
                    "choice_d": "5.4",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                {
                    "name": "Duct Design - Pressure Loss",
                    "topics": ['Ductwork Design'],
                    "prompt": "A circular duct with a diameter of 12 inches carries 1,200 CFM of air at standard conditions. The duct has a length of 75 feet with three 90° elbows (loss coefficient = 0.3 each) and one damper (loss coefficient = 0.2). Using a friction factor of 0.019 and air density of 0.075 lb/ft³, what is the total pressure loss in the duct system?",
                    "choice_a": "0.12 in. w.g.",
                    "choice_b": "0.25 in. w.g.",
                    "choice_c": "0.38 in. w.g.",
                    "choice_d": "0.51 in. w.g.",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Heat Transfer - Composite Wall",
                    "topics": ['HVAC Design', 'Energy Code Compliance'],
                    "prompt": "A composite wall consists of three layers: 4 inches of concrete (k = 0.8 BTU/hr·ft·°F), 2 inches of fiberglass insulation (k = 0.023 BTU/hr·ft·°F), and 0.5 inches of gypsum board (k = 0.1 BTU/hr·ft·°F). The indoor air temperature is 70°F with a convection coefficient of 1.5 BTU/hr·ft²·°F. The outdoor air temperature is 25°F with a convection coefficient of 4.0 BTU/hr·ft²·°F. What is the overall heat transfer coefficient (U-value) of the wall assembly?",
                    "choice_a": "0.057 BTU/hr·ft²·°F",
                    "choice_b": "0.078 BTU/hr·ft²·°F",
                    "choice_c": "0.091 BTU/hr·ft²·°F",
                    "choice_d": "0.105 BTU/hr·ft²·°F",
                    "correct_answer": "A",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                {
                    "name": "Cooling Tower Performance",
                    "topics": ['HVAC Design'],
                    "prompt": "A cooling tower is used to cool 600 GPM of water from 95°F to 85°F. The ambient air wet-bulb temperature is 76°F, and the air flow rate is 60,000 CFM. What is the cooling tower approach?",
                    "choice_a": "6°F",
                    "choice_b": "9°F",
                    "choice_c": "12°F",
                    "choice_d": "15°F",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Pump Selection",
                    "topics": ['HVAC Design'],
                    "prompt": "A chilled water system needs to deliver 200 GPM of water through a system with 100 ft of head loss. The pump will operate at 1750 RPM with water at 45°F. What is the required pump power?",
                    "choice_a": "4.2 horsepower",
                    "choice_b": "5.7 horsepower",
                    "choice_c": "7.1 horsepower",
                    "choice_d": "8.5 horsepower",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Energy Recovery Ventilation",
                    "topics": ['HVAC Design', 'Energy Code Compliance'],
                    "prompt": "An energy recovery ventilator (ERV) is used to precondition outdoor air. The outdoor air is at 10°F dry-bulb and 8°F wet-bulb temperature, and the exhaust air is at 72°F dry-bulb and 58°F wet-bulb temperature. The ERV has a sensible effectiveness of 70% and a latent effectiveness of 60%. The air flow rate is 2,000 CFM on both sides. What is the supply air temperature leaving the ERV?",
                    "choice_a": "43.4°F",
                    "choice_b": "48.7°F",
                    "choice_c": "53.4°F",
                    "choice_d": "57.8°F",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Fluid Mechanics - Pipe Flow",
                    "topics": ['HVAC Design'],
                    "prompt": "Water at 60°F flows through a 3-inch diameter pipe at a rate of 150 GPM. The pipe has a length of 200 feet with four 90° elbows (equivalent length = 5 ft each) and one globe valve (equivalent length = 60 ft). The pipe has a roughness factor of 0.0002 ft. What is the pressure drop in the pipe system?",
                    "choice_a": "2.4 psi",
                    "choice_b": "3.7 psi",
                    "choice_c": "5.1 psi",
                    "choice_d": "6.5 psi",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Thermodynamics - Air Compression",
                    "topics": ['HVAC Design'],
                    "prompt": "An air compressor takes in air at standard atmospheric conditions (14.7 psia, 70°F) and compresses it to 100 psig. The compressor has an isentropic efficiency of 75% and a mechanical efficiency of 90%. The air flow rate is 300 CFM at the inlet. Assuming air behaves as an ideal gas with k = 1.4 and a specific heat at constant pressure of 0.24 BTU/lb·°F, what is the discharge temperature of the compressed air?",
                    "choice_a": "292°F",
                    "choice_b": "354°F",
                    "choice_c": "418°F",
                    "choice_d": "483°F",
                    "correct_answer": "D",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
            ]
            
            # Electrical Engineering Power Systems PE Exam Problems
            electrical_problems = [
                {
                    "name": "Three-Phase Power Calculation",
                    "topics": ['Electrical Design', 'Power Distribution'],
                    "prompt": "A balanced three-phase load is connected in wye configuration to a 480V, 60Hz power system. The load draws 50A per phase with a lagging power factor of 0.85. What is the real power consumed by the load?",
                    "choice_a": "28.2 kW",
                    "choice_b": "35.1 kW",
                    "choice_c": "40.8 kW",
                    "choice_d": "48.0 kW",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 2
                },
                {
                    "name": "Transformer Sizing",
                    "topics": ['Electrical Design', 'Power Distribution'],
                    "prompt": "A facility requires a three-phase transformer to supply a load of 200 kVA at 208V. The primary voltage is 4160V, and the transformer needs to have a 25% future load growth capacity. The transformer will be located outdoors in an area with an ambient temperature of 40°C. What is the minimum transformer kVA rating required?",
                    "choice_a": "200 kVA",
                    "choice_b": "225 kVA",
                    "choice_c": "250 kVA",
                    "choice_d": "300 kVA",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Fault Current Analysis",
                    "topics": ['Electrical Design', 'Power Distribution'],
                    "prompt": "A 2000 kVA, 13.8 kV/480V, three-phase transformer has an impedance of 5.75%. The available fault current at the primary of the transformer is 8000A. What is the maximum fault current available at the secondary of the transformer?",
                    "choice_a": "18.2 kA",
                    "choice_b": "24.5 kA",
                    "choice_c": "30.1 kA",
                    "choice_d": "36.8 kA",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                {
                    "name": "Voltage Drop Calculation",
                    "topics": ['Electrical Design', 'Electrical Code Requirements'],
                    "prompt": "A 150 HP, 460V, three-phase motor is supplied by a feeder consisting of three #2/0 AWG THWN copper conductors in steel conduit. The feeder length is 250 feet, and the motor operates at 90% of full load with a power factor of 0.85 and an efficiency of 0.92. The conductor has a resistance of 0.0778 ohms/1000ft and a reactance of 0.0446 ohms/1000ft. What is the percentage voltage drop in the feeder?",
                    "choice_a": "1.8%",
                    "choice_b": "2.4%",
                    "choice_c": "3.2%",
                    "choice_d": "3.9%",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Motor Starting Methods",
                    "topics": ['Electrical Design', 'Power Distribution', 'Control Systems'],
                    "prompt": "A 100 HP, 460V, three-phase induction motor has a full-load current of 124A, a locked-rotor current of 745A, and a starting power factor of 0.35. The motor is supplied from a utility service with a 500 kVA transformer that has an impedance of 5.5%. For autotransformer starting with a 65% tap, what is the approximate starting current?",
                    "choice_a": "245A",
                    "choice_b": "315A",
                    "choice_c": "385A",
                    "choice_d": "455A",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                {
                    "name": "Grounding System Design",
                    "topics": ['Electrical Design', 'Electrical Code Requirements'],
                    "prompt": "Design a substation ground grid for an area measuring 50 ft × 50 ft. The soil resistivity is 100 ohm-meters, and the maximum fault current is 10 kA with a clearing time of 0.5 seconds. The grid will use 4/0 AWG copper conductors spaced 10 ft apart in both directions with 8-ft ground rods at each intersection. What is the approximate grid resistance to remote earth?",
                    "choice_a": "0.9 ohms",
                    "choice_b": "1.4 ohms",
                    "choice_c": "2.0 ohms",
                    "choice_d": "2.7 ohms",
                    "correct_answer": "B",
                    "estimated_time_to_complete": 6,
                    "difficulty": 5
                },
                {
                    "name": "Power Factor Correction",
                    "topics": ['Electrical Design', 'Power Distribution'],
                    "prompt": "A facility has a load of 800 kW with a power factor of 0.75 lagging. The utility charges a power factor penalty when the power factor is below 0.95. What is the size of capacitor bank needed to improve the power factor to 0.95?",
                    "choice_a": "213 kVAR",
                    "choice_b": "252 kVAR",
                    "choice_c": "294 kVAR",
                    "choice_d": "344 kVAR",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 3
                },
                {
                    "name": "Overcurrent Protection Coordination",
                    "topics": ['Electrical Design', 'Electrical Code Requirements', 'Power Distribution'],
                    "prompt": "A radial distribution system has three levels of protection: Main breaker (1600A frame, LSI trip unit), Feeder breaker (400A frame, LSI trip unit), and Load breaker (100A frame, thermal-magnetic trip). The maximum fault current available at the main breaker is 35 kA. The feeder serves several motor loads with a total full-load current of 320A and a momentary starting current of 1600A. What is the appropriate setting for the feeder breaker long-time pickup?",
                    "choice_a": "0.7 × 400A = 280A",
                    "choice_b": "0.8 × 400A = 320A",
                    "choice_c": "0.9 × 400A = 360A",
                    "choice_d": "1.0 × 400A = 400A",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 5
                },
                {
                    "name": "Harmonics Analysis",
                    "topics": ['Electrical Design', 'Power Distribution'],
                    "prompt": "A variable frequency drive (VFD) generates the following harmonic current components (as a percentage of the fundamental): 5th harmonic: 23%, 7th harmonic: 11%, 11th harmonic: 9%, 13th harmonic: 7%, 17th harmonic: 4%, 19th harmonic: 3%. The VFD supplies a 50 HP motor with a fundamental current of 65A. What is the total harmonic distortion (THD) of the current?",
                    "choice_a": "20.4%",
                    "choice_b": "26.3%",
                    "choice_c": "28.7%",
                    "choice_d": "31.2%",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 4
                },
                {
                    "name": "Load Flow Analysis",
                    "topics": ['Electrical Design', 'Power Distribution'],
                    "prompt": "A simple power system consists of: Generator: 10 MVA, 13.8 kV, X\"d = 15%, Transformer: 10 MVA, 13.8 kV/4.16 kV, Z = 6%, Transmission line: 5 miles, Z = 0.1 + j0.3 ohms/mile, Load: 8 MW at 0.8 power factor lagging. What is the approximate sending-end voltage needed to maintain 4.16 kV at the load?",
                    "choice_a": "4.32 kV",
                    "choice_b": "4.53 kV",
                    "choice_c": "4.78 kV",
                    "choice_d": "5.05 kV",
                    "correct_answer": "C",
                    "estimated_time_to_complete": 6,
                    "difficulty": 5
                },
            ]
            
            # Combine all problems
            all_problems = hvac_problems + electrical_problems
            
            # Add problems to database
            for problem_data in all_problems:
                problem_topics = problem_data.pop('topics')
                
                # Create the problem
                problem = Problem.objects.create(**problem_data)
                
                # Add topics to the problem
                for topic_name in problem_topics:
                    topic = topics[topic_name]
                    problem.topics.add(topic)
                
                self.stdout.write(f'Added problem: {problem.name}')
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added {len(all_problems)} engineering problems to Adeptly'))
