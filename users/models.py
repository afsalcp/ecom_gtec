from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart')
    
    class Meta:
        unique_together = ['user']
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='item')
    product=models.PositiveIntegerField()



