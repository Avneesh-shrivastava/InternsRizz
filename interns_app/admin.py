from django.contrib import admin
from .models import Job
# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "job_type",
        "work_mode",
        "location",
        "experience",
        "is_active",
    )

    list_filter = (
        "job_type",
        "work_mode",
        "experience",
        "is_active",
    )

    search_fields = (
        "title",
        "company",
        "skills",
        "location",
    )