from django.contrib import admin
from .models import College, School, UserProfile, CollegeRepresentative, SchoolRepresentative, UniqueID


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'state')
    search_fields = ('name', 'district', 'state')
    list_filter = ('state', 'district')

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'state')
    search_fields = ('name', 'district', 'state')
    list_filter = ('state', 'district')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'district', 'college', 'school', 'representative_type', 'unique_id')
    search_fields = ('name', 'phone', 'district', 'college__name', 'school__name')
    list_filter = ('representative_type', 'district')

class CollegeRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'state', 'district', 'college', 'unique_id')
    search_fields = ('name', 'phone', 'state', 'district', 'college__name')
    list_filter = ('state', 'district')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(representative_type='college')

class SchoolRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'state', 'district', 'school', 'unique_id')
    search_fields = ('name', 'phone', 'state', 'district', 'school__name')
    list_filter = ('state', 'district')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(representative_type='school')
class UniqueIDAdmin(admin.ModelAdmin):
    list_display = ('representative_type', 'unique_id', 'is_used')
    search_fields = ('unique_id', 'representative_type')
    list_filter = ('representative_type', 'is_used')


# Register models with admin site
admin.site.register(College, CollegeAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CollegeRepresentative, CollegeRepresentativeAdmin)
admin.site.register(SchoolRepresentative, SchoolRepresentativeAdmin)
admin.site.register(UniqueID, UniqueIDAdmin)
from django.contrib import admin
from .models import Task, UserTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'added_date', 'deadline']
    search_fields = ['title']
    ordering = ['-added_date']
    date_hierarchy = 'added_date'

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'submitted_date', 'is_verified', 'points_awarded', 'additional_points']
    search_fields = ['user__username', 'task__title']
    actions = ['verify_and_award_points']

    def verify_and_award_points(self, request, queryset):
        for user_task in queryset:
            if not user_task.is_verified:
                # Mark as verified
                user_task.is_verified = True
                # Award additional points (admin can adjust this in the admin interface)
                user_task.points_awarded += user_task.additional_points
                # Update the user's total points
                user_profile = user_task.user.userprofile  # Ensure correct access to the UserProfile model
                user_profile.points += user_task.additional_points
                user_profile.save()
                user_task.save()
        self.message_user(request, "Selected tasks have been verified and points awarded.")

    verify_and_award_points.short_description = "Verify and award points for selected tasks"
