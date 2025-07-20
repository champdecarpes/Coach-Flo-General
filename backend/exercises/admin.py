from django.contrib import admin
from .models import Exercise, TrackingFields

# Admin class for Exercise model
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """
    Admin class for Exercise model
    Configures display, filtering, search and validation in admin panel
    """
    list_display = ['id', 'modality', 'muscle_group', 'movement_pattern', 'strength', 'timed', 'tracking_fields_display']
    # Includes custom method to display tracking_fields

    list_filter = ['modality', 'muscle_group', 'movement_pattern']

    search_fields = ['modality', 'muscle_group', 'movement_pattern', 'instructions']

    fields = ['modality', 'muscle_group', 'movement_pattern', 'strength', 'bodyweight',
              'timed', 'distance_x_time', 'instructions', 'links', 'default_note',
              'monitored_fields']

    def get_readonly_fields(self, request, obj=None):
        """
        Defines fields that are read-only
        For example, can make monitored_fields read-only if needed
        """
        if obj:  # Only for existing objects
            return ['monitored_fields', 'tracking_fields_display']
        return []

    def save_model(self, request, obj, form, change):
        """
        Overrides model saving to perform clean validation
        Calls clean method before saving
        """
        obj.clean()  # Perform custom validation
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Optimizes queries by including TrackingFields data
        """
        qs = super().get_queryset(request)
        return qs.select_related('tracking_fields')

    def tracking_fields_display(self, obj):
        """
        Custom method to display tracking_fields data
        Returns a string representation of related TrackingFields
        """
        if obj.tracking_fields:
            return f"Time: {obj.tracking_fields.time}, Speed: {obj.tracking_fields.speed}"
        return "No tracking data"
    tracking_fields_display.short_description = "Tracking Fields"

# Register TrackingFields model separately if direct access is needed
@admin.register(TrackingFields)
class TrackingFieldsAdmin(admin.ModelAdmin):
    """
    Admin class for TrackingFields model
    Configures display and editing of individual records
    """
    list_display = ['id', 'time', 'speed', 'distance', 'reps']
    list_filter = ['time', 'reps']
    search_fields = ['time', 'speed']
