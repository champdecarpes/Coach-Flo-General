from django.contrib import admin
from .models import Client
from trainers.models import Trainer
from bodies.models import Body
from exercises.models import Exercise
from workouts.models import Workout
from programs.models import Program


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Client model.
    Customizes the display and editing of client data with related fields.
    """
    list_display = ('id', 'mail', 'trainer', 'birthdate', 'created_at')  # Fields to display in the list view
    list_filter = ('trainer', 'birthdate', 'created_at')  # Filter options in the sidebar
    search_fields = ('mail', 'trainer__full_name', 'birthdate')  # Searchable fields
    date_hierarchy = 'created_at'  # Date hierarchy for filtering
    fields = (
        'mail', 'birthdate', 'trainer', 'body_metrics', 'exercises', 'workouts', 'programs',
        ('is_active', 'is_staff', 'is_superuser')  # Group auth fields for better layout
    )
    readonly_fields = ('created_at', 'mail')  # Prevent modification of creation timestamp and email
    filter_horizontal = ('exercises', 'workouts', 'programs')  # Use horizontal filter for ManyToMany fields

    def get_queryset(self, request):
        """
        Optimize queryset by prefetching related objects.
        """
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('exercises', 'workouts', 'programs', 'trainer', 'body_metrics')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Customize the foreign key widget to limit choices based on context.
        """
        if db_field.name == 'trainer':
            kwargs['queryset'] = Trainer.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Customize the many-to-many widget to limit choices based on context.
        """
        if db_field.name in ['exercises', 'workouts', 'programs']:
            kwargs['queryset'] = {
                'exercises': Exercise.objects.all(),
                'workouts': Workout.objects.all(),
                'programs': Program.objects.all(),
            }[db_field.name]
        return super().formfield_for_manytomany(db_field, request, **kwargs)
