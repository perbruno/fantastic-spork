from django.db import models

import uuid

class User(models.Model):
    #  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(primary_key=True) #  db_index=True)
    watchlist = models.JSONField(default="{}")
    radar = models.JSONField(default="{}")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
