from django.contrib import admin

# Register your models here.

from .models import *

# Register your models here.
admin.site.register(News)
# admin.site.register(Project)
admin.site.register(Member)
admin.site.register(Scholarship)
admin.site.register(Comment)


class ProjectImageInline(admin.TabularInline):  # or admin.StackedInline
    model = ProjectImage
    extra = 1  # Number of empty forms to display
    fields = ('image', 'is_main')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('name', 'status', 'category', 'date')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'is_main')
    list_editable = ('is_main',)  # Allow toggling is_main in list view
