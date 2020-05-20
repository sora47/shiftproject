from django.db import models


# Create your models here.

class ShiftBaseModel(models.Model):
    check = models.BooleanField()
    duty = models.CharField(max_length=10)
    year = models.IntegerField()
    month = models.IntegerField()
    two = models.BooleanField()


class ShiftModel(models.Model):
    user_id = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    base_id = models.IntegerField()
