from django.db import models

# Create your models here.


class Chai(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "chai"

    def __str__(self):
         return self.name