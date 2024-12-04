from django.db import models
from django.contrib.auth.models import User

class PassItem(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Предполагаем, что имя - это строка, а не int
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)



class PassOrder(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Имя клиента или название заказа
    phone = models.CharField(max_length=20, blank=True, null=True)  # Имя клиента или название заказа
    accepted_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    submited_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=False, related_name='client_cards')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='m_orders')
    payment_number = models.CharField(max_length=20, blank=True, null=True)



class PassOrderItems(models.Model):
    pass_item = models.ForeignKey(PassItem, on_delete=models.CASCADE)  # Связь с таблицей pass_item
    pass_order = models.ForeignKey(PassOrder, on_delete=models.CASCADE, related_name='passes')  # Связь с таблицей pass_order
    amount = models.IntegerField()
    
    class Meta:
        unique_together = ('pass_item', 'pass_order')

# Create your models here.