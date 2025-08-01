from django.contrib import admin
from .models import Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Section model.
    Customizes the display and editing of sections with related exercises.
    """
    list_display = ('id', 'name', 'section_type', 'start_time', 'rounds', 'created_at')  # Fields to display
    list_filter = ('section_type', 'created_at')  # Filter options
    search_fields = ('name', 'section_type', 'note')  # Searchable fields
    date_hierarchy = 'created_at'  # Date hierarchy for filtering
    fields = (
        'name', 'section_type', 'exercises', 'start_time', 'rounds', 'duration', 'rest', 'note', 'created_at'
    )  # Define editable and read-only fields
    readonly_fields = ('created_at',)  # Prevent manual modification of creation timestamp
    filter_horizontal = ('exercises',)  # Use horizontal filter for ManyToMany field

    def get_queryset(self, request):
        """
        Optimize queryset by prefetching related exercises.
        """
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('exercises')
