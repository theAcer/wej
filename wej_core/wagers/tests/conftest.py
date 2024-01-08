# In your tests/conftest.py file

import pytest
from django.contrib.auth import get_user_model
#from wej_core.events.models import Event
from wej_core.wagers.models import Wager, WagerRequest


user_pw = "test" 

@pytest.fixture
def user_steve():
    return get_user_model().objects.create_user(
            email="steve@steve.com",
            password= user_pw,
        )

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
    return Wager.objects.create(
        title="Test Wager",
        creator=user_steve,
        description="Test Wager Description",
        amount=100.00,
        stake=10.00,
        winning_percentage=50.00,
        number_of_winners=1,

    )

@pytest.fixture
def wager_request(user_steve, user_bob, test_wager):
    return WagerRequest.objects.create(
        from_user=user_steve,
        to_user=user_bob,
        wager=test_wager
    )
