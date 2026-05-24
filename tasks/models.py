from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # Category Choices
    CATEGORY_PRINTER = 'printer'
    CATEGORY_CONSUMABLES = 'consumables'
    
    CATEGORY_CHOICES = [
        (CATEGORY_PRINTER, 'Printer'),
        (CATEGORY_CONSUMABLES, 'Consumables'),
    ]

    # Priority Choices
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CRITICAL = 'critical'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_CRITICAL, 'Critical'),
    ]

    # Status Choices (Kanban Board Columns)
    STATUS_TO_DO = 'to_do'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_UNDER_VALIDATION = 'under_validation'
    STATUS_DEPLOYED_STAGE = 'deployed_stage'
    STATUS_DEPLOYED_PROD = 'deployed_prod'
    STATUS_DONE = 'done'
    STATUS_BLOCKED = 'blocked'

    STATUS_CHOICES = [
        (STATUS_TO_DO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_UNDER_VALIDATION, 'Under Validation'),
        (STATUS_DEPLOYED_STAGE, 'Deployed to Stage'),
        (STATUS_DEPLOYED_PROD, 'Deployed to Prod'),
        (STATUS_DONE, 'Done'),
        (STATUS_BLOCKED, 'Blocked'),
    ]

    vendor_source = models.CharField(max_length=255, verbose_name="Vendor / Source")
    task_name = models.CharField(max_length=255, verbose_name="Task Name")
    country = models.CharField(max_length=100, verbose_name="Country")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_PRINTER, verbose_name="Category")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks', verbose_name="Assigned To")
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM, verbose_name="Priority")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_TO_DO, verbose_name="Status")
    story_points = models.IntegerField(null=True, blank=True, verbose_name="Story Points")
    notes = models.TextField(blank=True, null=True, verbose_name="Problem / Notes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks', verbose_name="Created By")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    deployment_link = models.URLField(blank=True, null=True, verbose_name="Deployment Link")

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.task_name} ({self.vendor_source})"
