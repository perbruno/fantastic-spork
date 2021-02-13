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
    try:
        record = Stock.objects.filter(code__iexact=code).values().latest('created_at')
    except models.ObjectDoesNotExist as err:
        print('{}: {}'.format(code,err))
    else:
        return record

def get_stock_history(code):
    try:
        records = Stock.objects.filter(code__iexact=code).order_by('-created_at').values('created_at','price')
    except models.ObjectDoesNotExist as err:
        print('{}: {}'.format(code,err))
    else:
        return list(records)

def get_last_stocks():
    Stock.objects.distinct('code')
    sql = Stock.objects.raw("""
        select 
            id,
            tracker_stock.code as code,
            price,
            created_at 
        from (
            select 
                code, 
                max(created_at) as cdate  
            from tracker_stock 
            group by code
        ) as last_stocks 
        join tracker_stock 
            ON tracker_stock.code = last_stocks.code 
            AND tracker_stock.created_at = last_stocks.cdate;
    """)
    rows = []
    for row in sql:
        rows.append([row.code,row.price])
    return rows