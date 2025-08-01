from django.contrib import admin
from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Program model.
    Customizes the display and editing of programs with related fields.
    """
    list_display = ('id', 'name', 'ownership', 'visibility', 'start_date', 'end_date', 'created_at')  # Fields to display
    list_filter = ('visibility', 'start_date', 'end_date', 'created_at')  # Filter options
    search_fields = ('name', 'description')  # Searchable fields
    date_hierarchy = 'created_at'  # Date hierarchy for filtering
    fields = (
        'name', 'start_date', 'end_date', 'visibility', 'description', 'ownership',
        'workouts', 'sections', 'exercises', 'created_at'
    )  # Define editable and read-only fields
    readonly_fields = ('created_at',)  # Prevent manual modification of creation timestamp
    filter_horizontal = ('workouts', 'sections', 'exercises')  # Use horizontal filter for ManyToMany fields

    def get_queryset(self, request):
        """
        Optimize queryset by prefetching related objects.
        """
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('workouts', 'sections', 'exercises', 'ownership')
