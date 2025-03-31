from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Problem, Topic

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = [
            'name', 'topics', 'prompt', 
            'choice_a', 'choice_b', 'choice_c', 'choice_d', 
            'correct_answer', 'problem_diagram', 'solution_diagram',
            'estimated_time_to_complete', 'difficulty'
        ]
        widgets = {
            'prompt': forms.Textarea(attrs={'rows': 4}),
            'topics': forms.CheckboxSelectMultiple(),
            'correct_answer': forms.RadioSelect(),
            'difficulty': forms.RadioSelect(),
        }

class TrainingPreferencesForm(forms.Form):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Select topics to include in your training"
    )
    
    DIFFICULTY_CHOICES = [
        (1, 'Very Easy'),
        (2, 'Easy'),
        (3, 'Medium'),
        (4, 'Hard'),
        (5, 'Very Hard'),
    ]
    
    difficulty_levels = forms.MultipleChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        initial=[2, 3, 4],  # Default to Easy, Medium, Hard
        label="Select difficulty levels"
    )
    
    time_available = forms.IntegerField(
        min_value=5,
        max_value=120,
        initial=15,
        help_text="Enter training time in minutes (5-120)",
        label="Available training time"
    )


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter topic name'}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'password1', 'password2'
        ]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
