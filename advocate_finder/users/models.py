import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_client = models.BooleanField(default=False)
    is_advocate = models.BooleanField(default=False)


class AdvocateAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='staffadmins')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    national_id = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username   


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    physical_address = models.TextField(max_length=255, null=True, blank=True)
    national_id = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    year_of_birth = models.CharField(max_length=4, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    profile_img = models.ImageField(upload_to='Profile', default='default.png', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


class LawyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    specialization = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    bar_association_membership = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username
    



class Advocate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.specialization}'


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.reviewer.username} - {self.advocate.user.username}'


class PracticeArea(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.advocate.user.username}'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: {self.subject}'


class Availability(models.Model):
    advocate = models.OneToOneField(Advocate, on_delete=models.CASCADE)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.advocate.user.username} availability'


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advocate = models.ForeignKey(Advocate, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.user.username} - {self.advocate.user.username}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message



class Case(models.Model):
    CASE_TYPES = (
        ('MED', 'Medical'),
        ('LGL', 'Legal'),
        ('FIN', 'Financial'),
        ('HR', 'Human Resources'),  # Example of additional case type
        ('CR', 'Criminal'),
        # Add more case types as needed
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(AdvocateAdmin, on_delete=models.CASCADE)
    case_type = models.CharField(max_length=3, choices=CASE_TYPES)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    case_number = models.CharField(max_length=15, unique=True)  # Max length set to 15 for "MED/5678/2022"
    
    def generate_case_number(self):
        random_digits = ''.join(random.choices(string.digits, k=4))  # Random 4 digits
        year = str(self.created_at.year)  # Current year
        self.case_number = f"{self.case_type}/{random_digits}/{year}"
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            self.generate_case_number()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
