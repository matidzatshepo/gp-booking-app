from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Doctor
class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=100)
    bio = models.TextField()
    contact_info = models.TextField()
    profile_picture = models.ImageField(upload_to='doctor_pictures/', blank=True, null=True)
    clinic_address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    price_per_appointment = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

# Custom User model
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Avoid reverse accessor clashes by customizing related_name
    groups = models.ManyToManyField(
        Group,
        related_name= 'custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

# Availability
class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="availabilities")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor.name} available on {self.date} from {self.start_time} to {self.end_time}"

# Appointnment 
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username}'s appointment with Dr. {self.doctor.name} on {self.date} at {self.time}"

# Review
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user','doctor') # Only one review per doctor per user
        ordering = ['-created_at'] 
    
    def __str__(self):
        return f"Review by {self.user.username} for Dr {self.doctor.name}({self.rating}★)"
