from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('resident', 'Resident'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Disaster(models.Model):
    SEVERITY_CHOICES = (
        ('Low', 'Low'),
        ('Mild', 'Mild'),
        ('High', 'High'),
        ('Severe', 'Severe'),
    )
    type = models.CharField(max_length=100)
    message = models.TextField()
    location = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.type} - {self.location} ({self.severity})"


class Request(models.Model):
    REQUEST_TYPE_CHOICES = (
        ('Medical Assistance', 'Medical Assistance'),
        ('Supply', 'Supply'),
        ('Missing Person', 'Missing Person'),
        ('Rescue', 'Rescue'),
        ('Other', 'Other'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    is_sos = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    form_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    source_page = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Request {self.id} - {self.type} ({self.status})"


class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('Earthquake', 'Earthquake'),
        ('Flood', 'Flood'),
        ('Typhoon', 'Typhoon'),
    )
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    form_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    source_page = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Report {self.id} - {self.type} ({self.status})"