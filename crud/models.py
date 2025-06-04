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
    
class Attendance(models.Model):
    class Meta:
        db_table = 'table_attendance'

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    attendance_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)  # Link attendance to a user
    shift = models.ForeignKey(Shifts, on_delete=models.SET_NULL, null=True, blank=True)  # Link attendance to a shift
    date = models.DateField(auto_now_add=True)  # Date of attendance
    time_in = models.TimeField(blank=True, null=True)  # Time the user clocked in
    time_out = models.TimeField(blank=True, null=True)  # Time the user clocked out
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')  # Attendance status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.date} ({self.status})"