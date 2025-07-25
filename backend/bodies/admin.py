from django.contrib import admin
from .models import Body, BodyChangeHistory


@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Body model.
    Customizes the display and editing of body metrics.
    """
    list_display = ('id', 'body_fat', 'weight', 'height', 'resting_heart_rate', 'created_at')
    list_filter = ('resting_heart_rate', 'created_at')
    search_fields = ('id', 'body_fat', 'weight')
    date_hierarchy = 'created_at'
    fields = (
        'body_fat', 'weight', 'body_fat_mass', 'lean_body_mass', 'chest', 'shoulder', 'waist',
        'resting_heart_rate', 'thigh_left', 'thigh_right', 'hip', 'calf_left', 'calf_right',
        'height', 'bicep_left', 'bicep_right', 'steps', 'sleep'
    )
    readonly_fields = ('created_at',)  # Prevent manual modification of creation timestamp

    def get_queryset(self, request):
        """
        Optimize queryset by prefetching related change history.
        """
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('bodychangehistory_set')


@admin.register(BodyChangeHistory)
class BodyChangeHistoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BodyChangeHistory model.
    Customizes the display of change history.
    """
    list_display = ('id', 'body', 'field_name', 'old_value', 'new_value', 'timestamp')
    list_filter = ('timestamp', 'field_name')
    search_fields = ('body__id', 'field_name', 'old_value', 'new_value')
    date_hierarchy = 'timestamp'
    readonly_fields = ('body', 'field_name', 'old_value', 'new_value', 'timestamp')  # All fields are read-only
