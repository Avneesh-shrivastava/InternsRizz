from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    preferred_role = models.CharField(max_length=100, blank=True)

    education = models.CharField(max_length=50, blank=True)
    college = models.CharField(max_length=200, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    experience = models.CharField(max_length=50, blank=True)

    skills = models.TextField(blank=True)
    about = models.TextField(blank=True)

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ("internship", "Internship"),
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
    ]

    WORK_MODE_CHOICES = [
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
        ("onsite", "On-site"),
    ]

    EXPERIENCE_CHOICES = [
        ("fresher", "Fresher"),
        ("0-1", "0–1 Years"),
        ("1-2", "1–2 Years"),
        ("2-3", "2–3 Years"),
        ("3+", "3+ Years"),
    ]

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    description = models.TextField()

    skills = models.TextField(
        help_text="Enter skills separated by commas"
    )

    location = models.CharField(max_length=100)

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    work_mode = models.CharField(
        max_length=20,
        choices=WORK_MODE_CHOICES
    )

    experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES
    )

    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    application_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.title} - {self.company}"