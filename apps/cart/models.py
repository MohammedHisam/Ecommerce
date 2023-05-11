from django.db import models
from django.contrib.auth.models import User
from apps.shop.models import Fruits


# Create your models here.
class CartList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruits, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user



