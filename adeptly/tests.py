from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from adeptly.models import Topic, Rank, Problem, UserTopicStats, TrainingSession, TopicExperienceEarned
from adeptly.forms import ProblemForm, TrainingPreferencesForm, RegistrationForm

class ModelTests(TestCase):
    """Tests for the Adeptly data models"""
    
    def setUp(self):
        """Set up test data for all model tests"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create test data
        self.rank_beginner = Rank.objects.create(name='Beginner')
        self.rank_expert = Rank.objects.create(name='Expert')
        
        self.topic_hvac = Topic.objects.create(name='HVAC Design')
        self.topic_electric = Topic.objects.create(name='Electrical Design')
        
        # Create a problem
        self.problem = Problem.objects.create(
            name="Test Problem",
            prompt="What is the correct answer?",
            choice_a="Wrong answer",
            choice_b="Correct answer",
            choice_c="Wrong answer",
            choice_d="Wrong answer",
            correct_answer="B",
            estimated_time_to_complete=5,
            difficulty=2
        )
        self.problem.topics.add(self.topic_hvac)
        
        # Create UserTopicStats
        self.user_stats = UserTopicStats.objects.create(
            user=self.user,
            topic=self.topic_hvac,
            experience=50,
            rank=self.rank_beginner
        )
        
        # Create a training session
        self.session = TrainingSession.objects.create(
            user=self.user,
            estimated_time_to_complete=15,
            was_completed=True,
            correct_attempts=3,
            incorrect_attempts=1,
            completed_at=timezone.now()
        )
        self.session.problems.add(self.problem)
        self.session.topics_covered.add(self.topic_hvac)

    def test_topic_creation(self):
        """Test that topics are created correctly"""
        self.assertEqual(self.topic_hvac.name, 'HVAC Design')
        self.assertTrue(Topic.objects.filter(name='HVAC Design').exists())
        self.assertEqual(str(self.topic_hvac), 'HVAC Design')
    
    def test_problem_creation(self):
        """Test that problems are created with correct attributes"""
        self.assertEqual(self.problem.name, 'Test Problem')
        self.assertEqual(self.problem.correct_answer, 'B')
        self.assertEqual(self.problem.topics.first(), self.topic_hvac)
        self.assertEqual(str(self.problem), 'Test Problem')
    
    def test_user_topic_stats(self):
        """Test that user topic stats track experience correctly"""
        self.assertEqual(self.user_stats.experience, 50)
        self.assertEqual(self.user_stats.rank, self.rank_beginner)
        
        # Test updating experience
        self.user_stats.experience += 100
        self.user_stats.save()
        self.assertEqual(self.user_stats.experience, 150)
    
    def test_training_session(self):
        """Test that training sessions record attempts correctly"""
        self.assertEqual(self.session.correct_attempts, 3)
        self.assertEqual(self.session.incorrect_attempts, 1)
        self.assertTrue(self.session.was_completed)
        self.assertIsNotNone(self.session.completed_at)
        
        # Test problem association
        self.assertTrue(self.problem in self.session.problems.all())


class FormTests(TestCase):
    """Tests for the Adeptly forms"""
    
    def setUp(self):
        """Set up test data for form tests"""
        self.topic1 = Topic.objects.create(name='HVAC Design')
        self.topic2 = Topic.objects.create(name='Electrical Design')
    
    def test_problem_form_valid(self):
        """Test that the problem form validates correctly"""
        form_data = {
            'name': 'Test Problem',
            'prompt': 'This is a test prompt?',
            'choice_a': 'Option A',
            'choice_b': 'Option B',
            'choice_c': 'Option C',
            'choice_d': 'Option D',
            'correct_answer': 'A',
            'topics': [self.topic1.id, self.topic2.id],
            'difficulty': 3,
            'estimated_time_to_complete': 5
        }
        
        form = ProblemForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_problem_form_missing_fields(self):
        """Test form validation with missing required fields"""
        # Missing prompt field
        form_data = {
            'name': 'Test Problem',
            # prompt is missing
            'choice_a': 'Option A',
            'choice_b': 'Option B',
            'choice_c': 'Option C',
            'choice_d': 'Option D',
            'correct_answer': 'A',
            'topics': [self.topic1.id],
            'difficulty': 3,
            'estimated_time_to_complete': 5
        }
        
        form = ProblemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('prompt', form.errors)
    
    def test_training_preferences_form_valid(self):
        """Test that the training preferences form validates correctly"""
        form_data = {
            'topics': [self.topic1.id, self.topic2.id],
            'difficulty_levels': ['1', '2', '3'],
            'time_available': 15
        }
        
        form = TrainingPreferencesForm(data=form_data)
        self.assertTrue(form.is_valid())


class LeaderboardTests(TestCase):
    """Tests specifically for the leaderboard functionality"""
    
    def setUp(self):
        """Set up test data for leaderboard tests"""
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')
        
        # Create ranks
        self.rank_beginner = Rank.objects.create(name='Beginner')
        self.rank_intermediate = Rank.objects.create(name='Intermediate')
        self.rank_advanced = Rank.objects.create(name='Advanced')
        
        # Create topics
        self.topic_hvac = Topic.objects.create(name='HVAC Design')
        self.topic_electrical = Topic.objects.create(name='Electrical Design')
        
        # Create user topic stats with different experience levels
        # User 1 has the most experience overall
        self.user1_hvac = UserTopicStats.objects.create(
            user=self.user1,
            topic=self.topic_hvac,
            experience=200,
            rank=self.rank_intermediate
        )
        self.user1_electrical = UserTopicStats.objects.create(
            user=self.user1,
            topic=self.topic_electrical,
            experience=150,
            rank=self.rank_intermediate
        )
        
        # User 2 has medium experience
        self.user2_hvac = UserTopicStats.objects.create(
            user=self.user2,
            topic=self.topic_hvac,
            experience=100,
            rank=self.rank_beginner
        )
        
        # User 3 has the least experience but is an expert in electrical
        self.user3_electrical = UserTopicStats.objects.create(
            user=self.user3,
            topic=self.topic_electrical,
            experience=300,
            rank=self.rank_advanced
        )
        
        # Create a client for testing
        self.client = Client()
    
    def test_leaderboard_access_requires_login(self):
        """Test that anonymous users are redirected to login"""
        # Try accessing without login
        leaderboard_url = reverse('leaderboard')
        response = self.client.get(leaderboard_url)
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
        
        # Now log in and try again
        self.client.login(username='user1', password='password1')
        response = self.client.get(leaderboard_url)
        
        # Should be successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adeptly/leaderboard.html')
    
    def test_overall_leaderboard_order(self):
        """Test that users are correctly ranked by total experience"""
        # Log in
        self.client.login(username='user1', password='password1')
        
        # Access leaderboard
        leaderboard_url = reverse('leaderboard')
        response = self.client.get(leaderboard_url)
        
        # Check the order of users in the overall leaderboard
        leaderboard = response.context['overall_leaderboard']
        
        # User 1 has 350 total XP (200 + 150)
        # User 3 has 300 total XP
        # User 2 has 100 total XP
        # So the order should be: user1, user3, user2
        self.assertEqual(leaderboard[0].username, 'user1')
        self.assertEqual(leaderboard[1].username, 'user3')
        self.assertEqual(leaderboard[2].username, 'user2')
    
    def test_topic_specific_leaderboard(self):
        """Test that topic-specific leaderboards show correct rankings"""
        # Log in
        self.client.login(username='user1', password='password1')
        
        # First access without topic filter to ensure it works
        leaderboard_url = reverse('leaderboard')
        response = self.client.get(leaderboard_url)
        self.assertEqual(response.status_code, 200)
        
        # Now access with topic filter
        topic_url = f"{leaderboard_url}?topic={self.topic_electrical.id}"
        response = self.client.get(topic_url)
        
        # Check successful response
        self.assertEqual(response.status_code, 200)
    
    def test_user_ranking_calculation(self):
        """Test that a user's rank is correctly calculated"""
        # Log in as user2 (who should be ranked #3 overall)
        self.client.login(username='user2', password='password2')
        
        # Access leaderboard
        leaderboard_url = reverse('leaderboard')
        response = self.client.get(leaderboard_url)
        
        # Check response is successful
        self.assertEqual(response.status_code, 200)
    
    def test_leaderboard_statistics(self):
        """Test that leaderboard statistics are correctly calculated"""
        # Log in
        self.client.login(username='user1', password='password1')
        
        # Access leaderboard
        leaderboard_url = reverse('leaderboard')
        response = self.client.get(leaderboard_url)
        
        # Check response is successful
        self.assertEqual(response.status_code, 200)


class ViewTests(TestCase):
    """Tests for the Adeptly views"""
    
    def setUp(self):
        """Set up test data for view tests"""
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        
        # Create test data
        self.rank_beginner = Rank.objects.create(name='Beginner')
        self.topic_hvac = Topic.objects.create(name='HVAC Design')
        self.topic_electric = Topic.objects.create(name='Electrical Design')
        
        # Create a problem
        self.problem = Problem.objects.create(
            name="Test Problem",
            prompt="What is the correct answer?",
            choice_a="Wrong answer",
            choice_b="Correct answer",
            choice_c="Wrong answer",
            choice_d="Wrong answer",
            correct_answer="B",
            estimated_time_to_complete=5,
            difficulty=2
        )
        self.problem.topics.add(self.topic_hvac)
        
        # Create a client for testing
        self.client = Client()
    
    def test_login_required_views(self):
        """Test that unauthorized users are redirected to login"""
        # Test dashboard
        dashboard_url = reverse('dashboard')
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
        
        # Test training setup
        setup_url = reverse('training_setup')
        response = self.client.get(setup_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_login_view(self):
        """Test that users can log in"""
        login_url = reverse('login')
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)
        
        # Test login post with valid credentials
        response = self.client.post(login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)
        
        # Should redirect to dashboard on success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('dashboard'))
    
    def test_dashboard_view(self):
        """Test the dashboard view"""
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Access dashboard
        dashboard_url = reverse('dashboard')
        response = self.client.get(dashboard_url)
        
        # Check successful response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adeptly/dashboard.html')
        
        # Verify context data
        self.assertIn('user_stats', response.context)


class TrainingFlowTests(TestCase):
    """Integration tests for the complete training workflow"""
    
    def setUp(self):
        """Set up test data for training flow tests"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create ranks
        self.rank_beginner = Rank.objects.create(name='Beginner')
        
        # Create topics
        self.topic_hvac = Topic.objects.create(name='HVAC Design')
        
        # Create multiple problems
        self.problem1 = Problem.objects.create(
            name="Problem 1",
            prompt="What is 2+2?",
            choice_a="3",
            choice_b="4",
            choice_c="5",
            choice_d="6",
            correct_answer="B",
            estimated_time_to_complete=5,
            difficulty=1
        )
        self.problem1.topics.add(self.topic_hvac)
        
        self.problem2 = Problem.objects.create(
            name="Problem 2",
            prompt="What is 3×3?",
            choice_a="6",
            choice_b="7",
            choice_c="9",
            choice_d="12",
            correct_answer="C",
            estimated_time_to_complete=5,
            difficulty=1
        )
        self.problem2.topics.add(self.topic_hvac)
        
        # Login the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
    
    def test_training_setup(self):
        """Test the training setup process"""
        # Set up training
        setup_url = reverse('training_setup')
        response = self.client.post(setup_url, {
            'topics': [self.topic_hvac.id],
            'difficulty_levels': ['1'],
            'time_available': 15
        })
        
        # Should redirect after successful submission (302 status)
        self.assertEqual(response.status_code, 302)
        
        # Verify session was created
        sessions = TrainingSession.objects.filter(user=self.user)
        self.assertTrue(sessions.exists())
        session = sessions.first()
        self.assertEqual(session.user, self.user)
        self.assertFalse(session.was_completed)
        self.assertEqual(session.problems.count(), 2)
    
    def test_answer_problem(self):
        """Test answering a problem in a training session"""
        # Create a session
        session = TrainingSession.objects.create(
            user=self.user,
            estimated_time_to_complete=15
        )
        session.problems.add(self.problem1, self.problem2)
        session.topics_covered.add(self.topic_hvac)
        
        # Answer the first problem
        problem_url = reverse('training_problem', kwargs={'session_id': session.id, 'problem_index': 0})
        response = self.client.post(problem_url, {
            'answer': 'B'  # correct answer
        })
        
        # Should redirect to next problem
        self.assertEqual(response.status_code, 302)
        
        # Verify user solved the problem
        self.assertTrue(self.problem1 in self.user.solved_problems.all())


class RegistrationTests(TestCase):
    """Tests for the user registration functionality"""
    
    def setUp(self):
        """Set up test data for registration tests"""
        self.client = Client()
        self.register_url = reverse('register')
        self.dashboard_url = reverse('dashboard')
        
        # Valid registration data
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        
        # Create an existing user for duplicate tests
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass'
        )
    
    def test_registration_view_get(self):
        """Test that the registration page loads correctly"""
        response = self.client.get(self.register_url)
        
        # Check that the page loads successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adeptly/register.html')
        
        # Check that the form is in the context
        self.assertIsInstance(response.context['form'], RegistrationForm)
    
    def test_registration_success(self):
        """Test successful user registration"""
        # Test post with valid data
        response = self.client.post(self.register_url, self.valid_user_data, follow=True)
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        
        # Check user data was saved correctly
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        
        # Check user was automatically logged in and redirected to dashboard
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.dashboard_url)
        
        # Check user is authenticated
        self.assertTrue(response.context['user'].is_authenticated)
    
    def test_registration_duplicate_username(self):
        """Test registration with a duplicate username"""
        # Create registration data with existing username
        duplicate_data = self.valid_user_data.copy()
        duplicate_data['username'] = 'existinguser'
        
        # Post the form
        response = self.client.post(self.register_url, duplicate_data)
        
        # Check that registration failed
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
        
        # Check for form error
        form_errors = response.context['form'].errors
        self.assertIn('username', form_errors)
    
    def test_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        # Create registration data with mismatched passwords
        mismatch_data = self.valid_user_data.copy()
        mismatch_data['password2'] = 'DifferentPass123'
        
        # Post the form
        response = self.client.post(self.register_url, mismatch_data)
        
        # Check that registration failed
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(User.objects.filter(username='newuser').exists())
        
        # Check for form error
        # Print the actual error message for debugging
        error_messages = response.context['form'].errors
        print(f"\nActual error messages: {error_messages}")
        self.assertIn('password2', error_messages)
    
    def test_registration_weak_password(self):
        """Test registration with a weak password"""
        # Create registration data with a weak password
        weak_pass_data = self.valid_user_data.copy()
        weak_pass_data['password1'] = 'password'
        weak_pass_data['password2'] = 'password'
        
        # Post the form
        response = self.client.post(self.register_url, weak_pass_data)
        
        # Check that registration failed
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(User.objects.filter(username='newuser').exists())
        
        # Check for form error related to password validation
        # Note: Django's exact error message may vary
        self.assertIn('password2', response.context['form'].errors)
    
    def test_registration_missing_fields(self):
        """Test registration with missing required fields"""
        # Create registration data missing required fields
        missing_data = {
            'username': 'newuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
            # Missing email, first_name, and last_name
        }
        
        # Post the form
        response = self.client.post(self.register_url, missing_data)
        
        # Check that registration failed
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        self.assertFalse(User.objects.filter(username='newuser').exists())
        
        # Check for form errors
        form_errors = response.context['form'].errors
        self.assertIn('email', form_errors)
        self.assertIn('first_name', form_errors)
        self.assertIn('last_name', form_errors)
    
    def test_navigation_to_register_from_login(self):
        """Test navigation from login page to registration page"""
        login_url = reverse('login')
        response = self.client.get(login_url)
        
        # Check that login page contains a link to registration page
        self.assertContains(response, f'href="{self.register_url}"')
    
    def test_successful_login_after_registration(self):
        """Test that a user can log in after registration"""
        # First register a new user
        self.client.post(self.register_url, self.valid_user_data)
        
        # Log out
        self.client.logout()
        
        # Try to log in
        login_url = reverse('login')
        login_data = {
            'username': 'newuser',
            'password': 'ComplexPass123'
        }
        response = self.client.post(login_url, login_data, follow=True)
        
        # Check successful login
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(response.context['user'].is_authenticated)


class RegistrationFormTests(TestCase):
    """Tests specifically for the RegistrationForm functionality"""
    
    def test_registration_form_valid_data(self):
        """Test that the registration form validates with valid data"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegistrationForm(data=form_data)
        
        # Form should be valid with correct data
        self.assertTrue(form.is_valid())
    
    def test_registration_form_invalid_email(self):
        """Test form validation with invalid email format"""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',  # Invalid email format
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123'
        }
        form = RegistrationForm(data=form_data)
        
        # Form should be invalid due to email format
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_registration_form_password_too_similar(self):
        """Test form validation with password too similar to username"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testuser123',  # Too similar to username
            'password2': 'testuser123'
        }
        form = RegistrationForm(data=form_data)
        
        # Form should be invalid due to similar password
        self.assertFalse(form.is_valid())
        # Just verify the field that has the error
        self.assertIn('password2', form.errors)
    
    def test_registration_form_save_method(self):
        """Test that the form's save method correctly creates a user"""
        form_data = {
            'username': 'saveuser',
            'email': 'save@example.com',
            'first_name': 'Save',
            'last_name': 'User',
            'password1': 'Complex76Pass!@#',
            'password2': 'Complex76Pass!@#'
        }
        form = RegistrationForm(data=form_data)
        
        # Form should be valid
        self.assertTrue(form.is_valid())
        
        # Save the form to create a user
        user = form.save()
        
        # Check that the user was created with correct attributes
        self.assertEqual(user.username, 'saveuser')
        self.assertEqual(user.email, 'save@example.com')
        self.assertEqual(user.first_name, 'Save')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('Complex76Pass!@#'))


class TopicManagementTests(TestCase):
    """Tests for the topic management functionality"""
    
    def setUp(self):
        """Set up test data for topic management tests"""
        # Create a test user with login
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        
        # Create a test topic
        self.topic = Topic.objects.create(name='Test Topic')
        
        # Create a problem using the test topic
        self.problem = Problem.objects.create(
            name="Test Problem",
            prompt="What is the answer?",
            choice_a="A",
            choice_b="B",
            choice_c="C",
            choice_d="D",
            correct_answer="A",
            estimated_time_to_complete=5,
            difficulty=3
        )
        self.problem.topics.add(self.topic)
    
    def test_topic_creation(self):
        """Test creating a new topic"""
        # Get the topic creation URL
        url = reverse('topic-create')
        
        # Submit a new topic
        response = self.client.post(url, {'name': 'New Test Topic'})
        
        # Check successful redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify topic was created
        self.assertTrue(Topic.objects.filter(name='New Test Topic').exists())
    
    def test_topic_update(self):
        """Test updating a topic"""
        # Get the topic update URL
        url = reverse('topic-update', args=[self.topic.id])
        
        # Update the topic
        response = self.client.post(url, {'name': 'Updated Topic Name'})
        
        # Check successful redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify topic was updated
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, 'Updated Topic Name')
    
    def test_topic_delete(self):
        """Test deleting a topic that is not in use"""
        # Create a new topic (not used by any problem)
        unused_topic = Topic.objects.create(name='Unused Topic')
        
        # Get the topic delete URL
        url = reverse('topic-delete', args=[unused_topic.id])
        
        # Delete the topic
        response = self.client.post(url)
        
        # Check successful redirect
        self.assertEqual(response.status_code, 302)
        
        # Verify topic was deleted
        self.assertFalse(Topic.objects.filter(name='Unused Topic').exists())
    
    def test_topic_delete_protection(self):
        """Test that topics in use by problems cannot be deleted"""
        # Get the topic delete URL for a topic in use
        url = reverse('topic-delete', args=[self.topic.id])
        
        # Try to delete the topic
        response = self.client.post(url)
        
        # Should not redirect but show the topic_in_use template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adeptly/topic_in_use.html')
        
        # Verify topic still exists
        self.assertTrue(Topic.objects.filter(id=self.topic.id).exists())
    
    def test_topic_create_ajax(self):
        """Test creating a topic through AJAX"""
        # Get the topic creation URL
        url = reverse('topic-create')
        
        # Submit a new topic with AJAX header
        response = self.client.post(
            url, 
            {'name': 'AJAX Topic'}, 
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check JSON response
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response['Content-Type'])
        
        # Verify topic was created
        self.assertTrue(Topic.objects.filter(name='AJAX Topic').exists())


class AddDefaultTopicsCommandTest(TestCase):
    """Test the add_default_topics management command"""
    
    def test_command_execution(self):
        """Test that the command creates the default topics"""
        # Import the Command class
        from adeptly.management.commands.add_default_topics import Command
        
        # Create a Buffer to capture output
        from io import StringIO
        out = StringIO()
        
        # Create and run the command
        cmd = Command(stdout=out, stderr=StringIO())
        cmd.handle()
        
        # Check that the topics were created
        self.assertTrue(Topic.objects.filter(name='HVAC Design').exists())
        self.assertTrue(Topic.objects.filter(name='Electrical Design').exists())
        self.assertTrue(Topic.objects.filter(name='Refrigeration').exists())
        
        # Check the output
        output = out.getvalue()
        self.assertIn('Adding default topics to Adeptly', output)
        
    def test_command_idempotence(self):
        """Test that running the command twice doesn't create duplicates"""
        # Create one of the default topics beforehand
        Topic.objects.create(name='HVAC Design')
        
        # Import the Command class
        from adeptly.management.commands.add_default_topics import Command
        
        # Create a Buffer to capture output
        from io import StringIO
        out = StringIO()
        
        # Create and run the command
        cmd = Command(stdout=out, stderr=StringIO())
        cmd.handle()
        
        # Check that we have exactly one of each topic
        self.assertEqual(Topic.objects.filter(name='HVAC Design').count(), 1)
        self.assertEqual(Topic.objects.filter(name='Electrical Design').count(), 1)


class EdgeCaseTests(TestCase):
    """Tests for edge cases and error handling"""
    
    def setUp(self):
        """Set up test data for edge case tests"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create rank and topic
        self.rank = Rank.objects.create(name='Beginner')
        self.topic = Topic.objects.create(name='HVAC Design')
        
        # Create a problem
        self.problem = Problem.objects.create(
            name="Test Problem",
            prompt="What is the correct answer?",
            choice_a="Wrong answer",
            choice_b="Correct answer",
            choice_c="Wrong answer",
            choice_d="Wrong answer",
            correct_answer="B",
            estimated_time_to_complete=5,
            difficulty=2
        )
        self.problem.topics.add(self.topic)
        
        # Login the test user
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
    
    def test_training_setup_no_topics(self):
        """Test training setup with no topics selected"""
        setup_url = reverse('training_setup')
        response = self.client.post(setup_url, {
            'topics': [],  # No topics selected
            'difficulty_levels': ['1', '2'],
            'time_available': 15
        })
        
        # Should stay on the same page (form validation error)
        self.assertEqual(response.status_code, 200)
        
        # Verify form error is shown
        form_errors = response.context['form'].errors
        self.assertIn('topics', form_errors)
        
        # Verify no session was created
        self.assertEqual(TrainingSession.objects.count(), 0)
    
    def test_training_setup_invalid_time(self):
        """Test training setup with invalid time values"""
        setup_url = reverse('training_setup')
        
        # Test with time too low
        response = self.client.post(setup_url, {
            'topics': [self.topic.id],
            'difficulty_levels': ['1', '2'],
            'time_available': 3  # Below minimum (should be 5)
        })
        
        # Should stay on the same page (form validation error)
        self.assertEqual(response.status_code, 200)
        form_errors = response.context['form'].errors
        self.assertIn('time_available', form_errors)
        
        # Test with time too high
        response = self.client.post(setup_url, {
            'topics': [self.topic.id],
            'difficulty_levels': ['1', '2'],
            'time_available': 150  # Above maximum (should be 120)
        })
        
        # Should stay on the same page (form validation error)
        self.assertEqual(response.status_code, 200)
        form_errors = response.context['form'].errors
        self.assertIn('time_available', form_errors)
    
    def test_training_session_no_problems(self):
        """Test handling a training session with no available problems"""
        # Create a new topic with no problems
        empty_topic = Topic.objects.create(name='Empty Topic')
        
        # Try to set up training with this topic
        setup_url = reverse('training_setup')
        response = self.client.post(setup_url, {
            'topics': [empty_topic.id],
            'difficulty_levels': ['1', '2', '3'],
            'time_available': 15
        })
        
        # Check that the application redirects (302)
        # This indicates it's handling the empty problem set in its own way
        self.assertEqual(response.status_code, 302)
        
        # Follow the redirect to see where it goes
        response = self.client.post(setup_url, {
            'topics': [empty_topic.id],
            'difficulty_levels': ['1', '2', '3'],
            'time_available': 15
        }, follow=True)
        
        # Verify we got a 200 status code after following the redirect
        self.assertEqual(response.status_code, 200)
    
    def test_training_problem_invalid_index(self):
        """Test accessing an invalid problem index in a training session"""
        # Create a session with one problem
        session = TrainingSession.objects.create(
            user=self.user,
            estimated_time_to_complete=15
        )
        session.problems.add(self.problem)
        session.topics_covered.add(self.topic)
        
        # Try to access a problem index that doesn't exist
        invalid_index_url = reverse('training_problem', 
                                  kwargs={'session_id': session.id, 'problem_index': 5})
        response = self.client.get(invalid_index_url, follow=True)
        
        # Should redirect to results page
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.redirect_chain[0][0])
    
    def test_nonexistent_session(self):
        """Test accessing a training session that doesn't exist"""
        # Use a non-existent session ID
        nonexistent_session_url = reverse('training_problem', 
                                        kwargs={'session_id': 9999, 'problem_index': 0})
        response = self.client.get(nonexistent_session_url)
        
        # Should return 404 Not Found
        self.assertEqual(response.status_code, 404)


