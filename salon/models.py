from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=25)
    password = models.CharField(max_length=2000)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the user is being created for the first time
            if not self.is_superuser:  # Check if the user is not a superuser
                self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Salon(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name

class Stylist(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    client_username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

    def formatted_appointment_date(self):
        return self.appointment_date.strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return f"{self.client_username} - {self.formatted_appointment_date()}"
