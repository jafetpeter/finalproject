from django.db import models

class Users(models.Model):
    class Meta:
        db_table = 'table_users'

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user_id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=55, blank=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False)
    contact_number = models.CharField(max_length=55, blank=True)
    email = models.EmailField(max_length=55, blank=True)
    username = models.CharField(max_length=55, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    shift = models.ForeignKey('Shifts', on_delete=models.SET_NULL, null=True, blank=True)  # Allow only one shift per user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class Shifts(models.Model):
    class Meta:
        db_table = 'table_shifts'

    shift_id = models.BigAutoField(primary_key=True)
    time_in = models.TimeField(blank=False)
    time_out = models.TimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.time_in} to {self.time_out}"