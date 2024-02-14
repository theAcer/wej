import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal
from wej_core.wagers.models import Wager, WagerParticipant

User = get_user_model()

@pytest.mark.django_db
def test_wager_creation(test_wager):
    print(f"Test User: {test_wager.creator}")
    print(f"Test Wager Title: {test_wager.title}")
    assert test_wager.title == "Test Wager"
    assert test_wager.creator.email == "steve@steve.com"

@pytest.fixture
def wager_participant(test_wager, user_bob):
    return WagerParticipant.objects.create(
        wager=test_wager,
        user=user_bob,
        stake=20.00,
    )

# Apply the decorator to the fixture or individual test functions that require database access
@pytest.mark.django_db
def test_add_participant(test_wager, user_bob):
    test_wager.add_participant(user_bob, stake=30.00)
    assert test_wager.participants.filter(user=user_bob).exists()
    participant = WagerParticipant.objects.get(wager=test_wager, user=user_bob)
    assert participant.stake == Decimal("30.00")


