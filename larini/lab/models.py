from django.db import models

class PassItem(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Предполагаем, что имя - это строка, а не int
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    class Meta:
        managed = False



class PassOrder(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  # Имя клиента или название заказа
    phone = models.CharField(max_length=20, blank=True, null=True)  # Имя клиента или название заказа
    accepted_date = models.DateField(blank=True, null=True)
    created_date = models.DateField()
    status = models.IntegerField(default=1)
    submited_date = models.DateField(blank=True, null=True)



class PassOrderItems(models.Model):
    pass_item = models.ForeignKey(PassItem, on_delete=models.CASCADE)  # Связь с таблицей pass_item
    pass_order = models.ForeignKey(PassOrder, on_delete=models.CASCADE)  # Связь с таблицей pass_order
    amount = models.IntegerField()
    
    class Meta:
        unique_together = ('pass_item', 'pass_order')

# Create your models here.
