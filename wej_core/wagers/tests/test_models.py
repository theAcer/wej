import pytest
from wej_core.wagers.models import WagerParticipant, WagerRequest


@pytest.mark.django_db
def test_add_participant(test_wager, user_bob):
    # Check that the creator is already a participant
    assert test_wager.is_participant(test_wager.creator)

    # Add a new participant
    new_participant = test_wager.add_participant(user_bob)

    # Check that the new participant is added
    assert test_wager.is_participant(user_bob)

    # Check that the new participant is not the creator
    assert not new_participant.is_creator

@pytest.mark.django_db
def test_remove_participant(test_wager, user_bob):
    # Add a participant
    test_wager.add_participant(user_bob)

    # Check that the participant is added
    assert test_wager.is_participant(user_bob)

    # Remove the participant
    test_wager.remove_participant(user_bob)

    # Check that the participant is removed
    assert not test_wager.is_participant(user_bob)

@pytest.mark.django_db
def test_creator_is_participant(test_wager):
    # Check that the creator is a participant
    assert test_wager.is_participant(test_wager.creator)

@pytest.mark.django_db
def test_accept_wager_request(test_wager, user_steve, user_bob):
    # Create a WagerRequest instance
    wager_request = WagerRequest.objects.create(
        from_user=user_steve,
        to_user=user_bob,
        wager=test_wager
    )

    # Check that the wager request exists
    assert wager_request is not None

    # Check that the 'to_user' is not yet a participant in the associated wager
    assert not test_wager.is_participant(user_bob)

    # Accept the wager request
    accepted = wager_request.accept()

    # Check that the wager request was accepted successfully
    assert accepted

    # Check that the 'to_user' is now a participant in the associated wager
    assert test_wager.is_participant(user_bob)