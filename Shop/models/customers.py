from django.db import models

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    Email = models.EmailField()
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    def isEmailExit(self):
        if Customer.objects.filter(Email=self.Email):
            return True
        else:
            return False

    @staticmethod
    def get_customer_email(email):
        try:
            return Customer.objects.get(Email=email)
        except:
            return False
