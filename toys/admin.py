from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Toy, Accessory, Review, ToyDrawing, UserProfile, HomepageReview


@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_filter = ('name', 'toy', 'price', 'stock')
    search_fields = ('name', 'toy_name')
    list_display = ('price', 'toy')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'toy', 'rating', 'created_at')

    def user_full_name(self, obj):
        # Use get_full_name if available, otherwise use username
        return obj.user.get_full_name() or obj.user.username

    user_full_name.short_description = 'User'


admin.site.register(Review, ReviewAdmin)


@admin.register(ToyDrawing)
class ToyDrawingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'width', 'height', 'price', 'status', 'is_approved', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('status', 'is_approved', 'created_at')

    actions = ['approve_drawing', 'reject_drawing', 'set_in_progress', 'set_completed']

    def approve_drawing(self, request, queryset):
        queryset.update(is_approved=True, status='in_progress')
        self.message_user(request, "Selected drawings have been approved and set to 'In Progress'.")

    def reject_drawing(self, request, queryset):
        queryset.update(is_approved=False, status='rejected')
        self.message_user(request, "Selected drawings have been rejected.")

    def set_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, "Selected drawings have been set to 'In Progress'.")

    def set_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, "Selected drawings have been set to 'Completed'.")


# Create an admin action to create missing UserProfiles
@admin.action(description="Create missing UserProfiles")
def create_missing_profiles(modeladmin, request, queryset):
    for user in queryset:
        UserProfile.objects.get_or_create(user=user)


# Unregister the original User admin to avoid conflict
admin.site.unregister(User)


# Extend the existing UserAdmin
class UserAdmin(BaseUserAdmin):
    actions = [create_missing_profiles]


# Re-register the User model with the extended UserAdmin
admin.site.register(User, UserAdmin)


# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'shipping_address')


class HomepageReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'email', 'created_at')
    search_fields = ('customer_name', 'email')
    list_filter = ('created_at',)


admin.site.register(HomepageReview, HomepageReviewAdmin)
