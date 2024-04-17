from django.db import models
from django.utils import timezone

created_at = timezone.now()



class UserSession(models.Model):
    session_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    stage = models.CharField(max_length=50)
    name = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    case_type = models.CharField(max_length=100, null=True, blank=True)
    selected_advocate = models.IntegerField(null=True, blank=True)



class Appointment(models.Model):
    phone_number = models.CharField(max_length=20)  # Assuming the phone number length won't exceed 20 characters
    full_name = models.CharField(max_length=100)  # Assuming the full name won't exceed 100 characters
    advocate_name = models.CharField(max_length=100)
    advocate_description = models.TextField()  # You can adjust the max_length or remove it depending on your needs
    advocate_location = models.CharField(max_length=100)
    advocate_case_types = models.CharField(max_length=200)  # Storing as comma-separated values
    advocate_rate = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal field for storing rates
    case_type = models.CharField(max_length=100)
    appointment_date = models.DateField()

    def __str__(self):
        return f"{self.full_name}'s Appointment with {self.advocate_name} on {self.appointment_date}"
    


class Advocate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    case_types = models.ManyToManyField('CaseType')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class CaseType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
