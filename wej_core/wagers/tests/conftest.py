# In your tests/conftest.py file

import pytest
from django.contrib.auth import get_user_model
#from wej_core.events.models import Event
from wej_core.wagers.models import Wager, WagerRequest


user_pw = "test" 

@pytest.fixture
def user_steve():
    user = get_user_model().objects.create_user(
        email="steve@steve.com",
        password=user_pw,
    )
    assert isinstance(user, get_user_model())  # Ensure 'user' is a User instance
    return user

    

@pytest.fixture
def user_bob():
    return get_user_model().objects.create_user(
            email="bob@bob.com",
            password= user_pw,
        )


#def event(user_steve):
    #return Event.objects.create(creator=user_steve, title="Event 1", description="Event description")

@pytest.fixture
def test_wager(user_steve):
    test_wager = Wager.objects.create(
        title="Test Wager",
        creator=user_steve,
        description="Test Wager Description",
        amount=100.00,
        number_of_winners=1,

    )
    assert test_wager.title == "Test Wager"
    assert test_wager.creator.email == "steve@steve.com"
    return test_wager

@pytest.fixture
def wager_request(user_steve, user_bob, test_wager):
    return WagerRequest.objects.create(
        from_user=user_steve,
        to_user=user_bob,
        wager=test_wager
    )
