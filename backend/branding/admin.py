from django.contrib import admin
from .models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Brand model.
    Customizes the display and editing of brand names.
    """
    list_display = ('id', 'name')  # Fields to display in the list view
    list_filter = ('name',)  # Filter options in the sidebar
    search_fields = ('name',)  # Searchable fields
    ordering = ('name',)  # Default ordering
