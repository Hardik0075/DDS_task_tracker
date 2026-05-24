from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'task_name', 
        'vendor_source', 
        'country', 
        'category', 
        'assigned_to', 
        'priority', 
        'status', 
        'story_points',
        'updated_at'
    )
    list_filter = (
        'status', 
        'priority', 
        'category', 
        'country'
    )
    search_fields = (
        'task_name', 
        'vendor_source', 
        'country', 
        'notes', 
        'assigned_to__username'
    )
    ordering = ('-updated_at',)
    
    # Organize fields inside admin edit form
    fieldsets = (
        ('General Info', {
            'fields': ('task_name', 'vendor_source', 'country', 'category')
        }),
        ('Execution', {
            'fields': ('assigned_to', 'priority', 'status', 'story_points', 'deployment_link')
        }),
        ('Details', {
            'fields': ('notes', 'created_by')
        }),
    )
    
    # Auto-populate created_by field with current user if not set
    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
