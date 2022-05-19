from django.contrib import admin

from tasks.models import Task


# reload ... ... ... ...


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "description", "owner"]


admin.site.register(Task, TaskAdmin)
