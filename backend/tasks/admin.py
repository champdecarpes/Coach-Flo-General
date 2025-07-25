from django.contrib import admin
from .models import Task
from bodies.models import Body


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Task model.
    Customizes the display and editing of tasks with related Body metrics.
    """
    list_display = ('id', 'name', 'date', 'done', 'body_metric')  # Fields to display in the list view
    list_filter = ('done', 'date')  # Filter options in the sidebar
    search_fields = ('name', 'note')  # Searchable fields
    date_hierarchy = 'date'  # Date hierarchy for filtering
    fields = ('name', 'date', 'note', 'done', 'body_metric')  # Define editable fields
    # No readonly_fields by default, as date can be edited unless specified otherwise

    def get_queryset(self, request):
        """
        Optimize queryset by selecting related Body metrics.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('body_metric')
