# Problem Diagrams for Adeptly

This directory contains diagram images for engineering problems in the Adeptly application.

## Diagrams Available

1. **hvac_mixed_air_diagram.svg** - Diagram for the HVAC mixed air calculation problem showing the mixing of outside air and return air in an AHU mixing box.

## How to Use These Diagrams

These diagrams can be used with problem entries in the Adeptly database by setting the `problem_diagram` field on the Problem model. 

### Example Code for Adding a Diagram to a Problem

```python
from adeptly.models import Problem
from django.core.files.base import ContentFile
import os

# Get the problem you want to update
problem = Problem.objects.get(name="Psychrometrics - Mixed Air Conditions")

# Path to the diagram file
diagram_path = os.path.join("adeptly", "problem_diagrams", "hvac_mixed_air_diagram.svg")

# Open the file and add it to the problem
with open(diagram_path, 'rb') as f:
    file_content = f.read()
    problem.problem_diagram.save("hvac_mixed_air_diagram.svg", ContentFile(file_content), save=True)
```

## Adding New Diagrams

When adding new diagrams to this directory, please follow these guidelines:

1. Use descriptive filenames that clearly indicate the problem type
2. Use SVG format for vector graphics when possible
3. Include a brief description of the diagram in this README.md file
4. Update the README.md file when new diagrams are added

## Naming Conventions

Use snake_case for filenames and include the problem type in the name, e.g.:
- hvac_mixed_air_diagram.svg
- electrical_power_factor_diagram.svg
- duct_pressure_loss_diagram.svg
