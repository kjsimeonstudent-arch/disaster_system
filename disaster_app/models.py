from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('resident', 'Resident'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name

#main alert model
class Disaster(models.Model):
    TYPE_CHOICES = (
        ('flood', 'Flood'),
        ('typhoon', 'Typhoon'),
        ('earthquake', 'Earthquake'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    location = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.location}"

class Report(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} - {self.status}"