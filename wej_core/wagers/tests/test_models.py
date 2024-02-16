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
    assert test_wager.is_participant(user_bob)
    participant = WagerParticipant.objects.get(wager=test_wager, participant=user_bob)
    assert participant.stake == Decimal("30.00")


@pytest.mark.django_db
def test_is_participant(test_wager, user_bob):
    # Initially, user_bob is not a participant
    assert not test_wager.is_participant(user_bob)

    # Add user_bob as a participant
    test_wager.add_participant(user_bob, stake=30.00)

    # Now, user_bob should be a participant
    assert test_wager.is_participant(user_bob)

@pytest.mark.django_db
def test_remove_participant(test_wager, user_bob):
    # Add user_bob as a participant
    test_wager.add_participant(user_bob, stake=30.00)

    # Check if user_bob is a participant before removal
    assert test_wager.is_participant(user_bob)

    # Remove user_bob as a participant using remove_participant method
    test_wager.remove_participant(user_bob)

    # Now, user_bob should not be a participant
    assert not test_wager.is_participant(user_bob)

    # Check that the participant is removed from WagerParticipant model
    with pytest.raises(WagerParticipant.DoesNotExist):
        WagerParticipant.objects.get(wager=test_wager, participant=user_bob)


