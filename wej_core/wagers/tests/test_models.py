import pytest
from django.contrib.auth import get_user_model
from wej_core.wagers.models import Wager, WagerParticipant

User = get_user_model()

@pytest.mark.django_db
def test_wager_creation(test_wager):
    print(f"Test User: {test_wager.creator}")
    print(f"Test Wager Title: {test_wager.title}")
    assert test_wager.title == "Test Wager"
    assert test_wager.creator.email == "steve@steve.com"