from uuid import uuid4

from django.db import models


class UUIDMixin(object):
    """
    Mixing for changing models from integer-based PK to an UUID one.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
