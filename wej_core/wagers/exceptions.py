from django.db import IntegrityError


class AlreadyExistsError(IntegrityError):
    pass


class AlreadyParticipantError(IntegrityError):
    pass