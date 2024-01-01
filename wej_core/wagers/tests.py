# wagers/tests.py
from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.core.cache import cache
from .models import Event, Participant,Wager, WagerManager, WagerRequest

from wagers.exceptions import AlreadyExistsError, AlreadyParticipantError



class login:
    def __init__(self, testcase, user, password):
        self.testcase = testcase
        success = testcase.client.login(username=user, password=password)
        self.testcase.assertTrue(
            success, f"login with username={user!r}, password={password!r} failed"
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class BaseTestCase(TestCase):
    def setUp(self):
        """
        Setup some initial users

        """
        self.user_pw = "test"
        self.user_bob = self.create_user("bob", "bob@bob.com", self.user_pw)
        self.user_steve = self.create_user("steve", "steve@steve.com", self.user_pw)
        self.user_susan = self.create_user("susan", "susan@susan.com", self.user_pw)
        self.user_amy = self.create_user("amy", "amy@amy.amy.com", self.user_pw)

        """
        setup some participants
        """
        self.participant_bob = self.create_participant(self.user_bob)
        self.participant_steve = self.create_participant(self.user_steve)
        self.participant_susan = self.create_participant(self.user_susan)
        self.participant_amy = self.create_participant(self.user_amy)
        cache.clear()
        """
        setup initial wager

        """
        self.test_wager_1 = self.create_wager(
            title="test wager",
            creator=self.user_bob,
            description="test description",
            amount=100,
            stake=10,
            winning_percentage=50.00,
            number_of_winners=1,
        )
    def tearDown(self):
        cache.clear()
        self.client.logout()

    def login(self, user, password):
        return login(self, user, password)

    def create_user(self, username, email_address, password):
        user = CustomUser.objects.create_user(username, email_address, password)
        return user
    
    def create_participant(self, user):
        # Create Participant instance for the user
        return Participant.objects.create(user=user)

    def create_wager(self, title, creator, description, amount, stake, winning_percentage, number_of_winners):
        return Wager.objects.create(
            title=title,
            creator=creator,
            description=description,
            amount=amount,
            stake=stake,
            winning_percentage=winning_percentage,
            number_of_winners=number_of_winners,
        )

    def create_wager(self, title, creator, description, amount, stake, winning_percentage, number_of_winners):
        return Wager.objects.create(
            title=title,
            creator=creator,
            description=description,
            amount=amount,
            stake=stake,
            winning_percentage=winning_percentage,
            number_of_winners=number_of_winners,
        )

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)

class WagersModelTests(BaseTestCase):

    def test_accept_wager_request(self):
        # Create a WagerRequest instance
        wager_request = WagerRequest.objects.create(
            from_user=self.user_steve,
            to_user=self.user_bob,
            wager=self.test_wager_1  # Assuming test_wager_1 is the desired wager
        )

        # Check that the wager request exists
        self.assertIsNotNone(wager_request)

        # Accept the wager request
        accepted = wager_request.accept()

        # Check that the wager request was accepted successfully
        self.assertTrue(accepted)
        
        # Check that the 'to_user' is now a participant in the associated wager
        self.assertIn(self.participant_bob, self.test_wager_1.participants.all())
