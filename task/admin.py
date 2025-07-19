from django.contrib import admin
from .models import Task, AuditTask

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'status', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('description', 'user__username')
    ordering = ('-created_at',)

@admin.register(AuditTask)
class AuditTaskAdmin(admin.ModelAdmin):
    list_display = ('id','status', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'user')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
