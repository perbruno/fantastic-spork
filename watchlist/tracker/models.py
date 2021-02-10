from django.db import models

import uuid

# Create your models here.

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, db_index=True)
    name = models.CharField(max_length=90, blank=True, null=True,db_index=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


def post_stock(cd,nm,prc): 
    record = Stock(code=cd, name=nm ,price=prc)
    record.save()

def get_stock(code): #wip
    record = Stock.objects.filter(code__exact=code)
    print(record)
    return record