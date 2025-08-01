from django.contrib import admin
from .models import Workout

class WorkoutAdmin(admin.ModelAdmin):
    """
    Admin configuration for Workout model
    Displays and manages workout details with related fields
    """
    list_display = ('name', 'created_at', 'visibility', 'ownership')  # Fields to display in list view
    list_filter = ('visibility', 'created_at')  # Filters for list view
    search_fields = ('name', 'description')  # Searchable fields
    filter_horizontal = ('sections', 'exercises')  # Horizontal filter for ManyToMany fields

    # Fields to display in detail view
    fields = ('name', 'created_at', 'description', 'visibility', 'ownership', 'sections', 'exercises')

    # Read-only fields
    readonly_fields = ('created_at',)

admin.site.register(Workout, WorkoutAdmin)
