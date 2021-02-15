from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True)
    watchlist = models.JSONField(default="{}")
    radar = models.JSONField(default="{}")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
