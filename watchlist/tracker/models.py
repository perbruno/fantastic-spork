from django.db import models

import uuid

# Create your models here.

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=90, blank=True, null=True,db_index=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __str__(self):
        return f'{self.code} - {self.name}'
