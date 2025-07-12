from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin view for the custom user model.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_active')
    
    def get_queryset(self, request):
        """
        Override the get_queryset method to return only active users.
        """
        qs = super().get_queryset(request)
        return qs.filter(is_active=True)
    def save_model(self, request, obj, form, change):
        """
        Override the save_model method to set the user as active when created.
        """
        if not change:
            obj.is_active = True
        super().save_model(request, obj, form, change)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)