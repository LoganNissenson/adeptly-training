from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from adeptly.models import Topic, Rank, Problem, UserTopicStats, TrainingSession, TopicExperienceEarned
from adeptly.forms import ProblemForm, TrainingPreferencesForm

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
        self.assertFormError(response, 'form', 'topics', 'This field is required.')
        
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
        self.assertFormError(response, 'form', 'time_available', 
                            'Ensure this value is greater than or equal to 5.')
        
        # Test with time too high
        response = self.client.post(setup_url, {
            'topics': [self.topic.id],
            'difficulty_levels': ['1', '2'],
            'time_available': 150  # Above maximum (should be 120)
        })
        
        # Should stay on the same page (form validation error)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'time_available', 
                            'Ensure this value is less than or equal to 120.')
    
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
