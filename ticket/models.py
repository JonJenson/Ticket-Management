from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Ticket(models.Model):  # Corrected: inherit from models.Model
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    engineer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='engineer', null=True ,blank =True)
    ticket_id = models.CharField(max_length=15, unique=True)
    ticket_title = models.CharField(max_length=50)
    ticket_description = models.TextField()
    status = models.CharField(max_length=20, choices=(
        ('Active', 'Active'), ('Pending', 'Pending'), ('Resolved', 'Resolved')), default='Pending')
    created_on = models.DateTimeField()
    
    last_modified = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=5, choices=(('Low', 'Low'), ('High', 'High')))
    is_assigned_to_engineer = models.BooleanField(default=False)
    resolution_steps = models.TextField(blank =True , null=True)
