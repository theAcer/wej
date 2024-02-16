from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from wej_core.users.models import User
from django.conf import settings


from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

from wej_core.wagers.signals import (
    wager_request_accepted,
    wager_request_rejected,
    wager_request_canceled,
    wager_request_viewed,
    wager_removed,
    wager_request_created,
)

class WagerManager(models.Manager):
    """Wagers manager"""

    def requests(self, wager):
        """Return a list of wager requests for a particular wager"""
        qs = WagerRequest.objects.filter(wager=wager)
        qs = self._wager_request_select_related(qs, "from_user", "to_user")
        wager_requests = list(qs)
        return wager_requests

    def sent_requests(self):
        pass

    def unread_requests(self):
        pass

    def unread_requests_count(self):
        pass

    def read_requests(self):
        pass

    def rejected_requests(self):
        pass

    def unrejected_requests_count(self):
        pass


class Wager(models.Model):
    title = models.CharField(max_length=100, null=True)
    creator = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name="wagers_created", null=True)
    description = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    winning_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    number_of_winners = models.PositiveIntegerField(null=True)
    participants = models.ManyToManyField(
        AUTH_USER_MODEL,
        through='WagerParticipant',
        related_name='wagers_participated',
        blank=True
        )
    objects = WagerManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.creator not in self.participants.all():
            self.participants.add(self.creator)

    def add_participant(self, user, stake):
        """Add a participant to the specified wager with a stake"""
        participant, created = WagerParticipant.objects.get_or_create(wager=self, participant=user)
        participant.stake = stake
        participant.save()
        self.participants.add(user)

    def remove_participant(self, user):
            """Remove a participant from the specified wager"""
            participant = self.wagerparticipant_set.get(participant=user)
            participant.delete()

    def is_participant(self, user):
        """Check if a user is a participant in the wager"""
        return self.wagerparticipant_set.filter(participant=user).exists()

    def __str__(self):
        return f"{self.description} - {self.title}"


class WagerParticipant(models.Model):
    wager = models.ForeignKey(Wager, on_delete=models.CASCADE, null=True)
    participant = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    stake = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_creator = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.participant} - {self.wager}"


class Event(models.Model):
    creator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()


    def __str__(self):
        return self.title


class WagerRequestManager(models.Manager):
    def requests(self, user):
        """Return a list of wager requests for the user."""
        return list(self.filter(to_user=user))

    def sent_requests(self, user):
        """Return a list of wager requests sent by the user."""
        return list(self.filter(from_user=user))

    def unread_requests(self, user):
        """Return a list of unread wager requests for the user."""
        return list(self.filter(to_user=user, viewed__isnull=True))

    def unread_request_count(self, user):
        """Return a count of unread wager requests for the user."""
        return self.filter(to_user=user, viewed__isnull=True).count()

    def mark_viewed(self, user, wager_request):
        """Mark a wager request as viewed by the user."""
        if wager_request.to_user == user and not wager_request.viewed:
            wager_request.viewed = timezone.now()
            wager_request.save()


class WagerRequest(models.Model):
    """Model to represent Wager requests"""

    from_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wager_requests_sent",
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wager_requests_received",
    )

    message = models.TextField(_("Message"), blank=True)
    wager = models.ForeignKey(Wager, on_delete=models.CASCADE)  # Link to the specific Wager
    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    objects = WagerRequestManager()

    class Meta:
        verbose_name = _("Wager Request")
        verbose_name_plural = _("Wager Requests")
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.from_user_id} wager requested #{self.to_user_id}"

    def accept(self):
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot send requests to themselves.")
        # Add the 'to_user' to the associated wager as a participant
        self.wager.add_participant(self.to_user)
        wager_request_accepted.send(
            sender=self, from_user=self.from_user, to_user=self.to_user
        )
        self.delete()
        return True

    def reject(self):
        """reject this wager request"""
        self.rejected = timezone.now()
        self.save()
        wager_request_rejected.send(sender=self)
        return True



class WagerInvitation(models.Model):
    sender = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wager_invitations_sent'
        )
        
    recipient = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wager_invitations_received'
        )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to the specific Event
    created = models.DateTimeField(auto_now_add=True)
    
    # You can add additional fields to the model, such as a message for the invitation.
    message = models.TextField(blank=True, null=True)
    
    # Add a field to represent the status of the invitation, e.g., "accepted," "rejected," or "pending."
    status = models.CharField(max_length=10, default='pending')
    
    class Meta:
        verbose_name = "Wager Invitation"
        verbose_name_plural = "Wager Invitations"

    def __str__(self):
        return f"{self.sender} invited {self.recipient} to {self.event}"

