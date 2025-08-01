from django.contrib import admin
from .models import TrainerProfile, ClientProfile, OrganizationProfile, User


class TrainerProfileInline(admin.StackedInline):
    model = TrainerProfile
    can_delete = False


class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False


class OrganizationProfileInline(admin.StackedInline):
    model = OrganizationProfile
    can_delete = False


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'role', 'date_joined')
    list_filter = ('role', 'date_joined')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined',)
    inlines = []

    def get_inlines(self, request, obj=None):
        if obj and obj.role == 'trainer':
            return [TrainerProfileInline]
        elif obj and obj.role == 'client':
            return [ClientProfileInline]
        elif obj and obj.role == 'organization':
            return [OrganizationProfileInline]
        return []
