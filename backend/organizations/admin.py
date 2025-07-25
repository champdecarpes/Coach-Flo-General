from django.contrib import admin
from .models import Organization
from branding.models import Brand


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Organization model.
    Customizes the display and editing of organization data with related Brand.
    """
    list_display = ('id', 'mail', 'branding', 'is_active', 'created_at')  # Fields to display in the list view
    list_filter = ('is_active', 'created_at')  # Filter options in the sidebar
    search_fields = ('mail', 'branding__name')  # Searchable fields
    readonly_fields = ('is_active', 'created_at', 'mail')  # Prevent modification of non-editable fields
    fields = ('mail', 'branding', 'is_active')  # Define editable and read-only fields

    def get_queryset(self, request):
        """
        Optimize queryset by selecting related Brand.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('branding')
