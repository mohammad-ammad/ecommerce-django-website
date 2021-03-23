from django.db import models
from .product import Product
from .customers import Customer
import datetime

class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customerid(customerid):
        return Orders.objects.filter(customer=customerid).order_by('-date')