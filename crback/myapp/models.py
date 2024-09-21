from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Existing Models

class College(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'state', 'district')

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'state', 'district')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    REPRESENTATIVE_CHOICES = [
        ('college', 'College'),
        ('school', 'School')
    ]

    name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=10, default="")
    email = models.EmailField(default='default@example.com')
    state = models.CharField(max_length=100, default="")
    district = models.CharField(max_length=100, default="")
    college = models.CharField(max_length=200, default="", blank=True, null=True)
    school = models.CharField(max_length=200, default="", blank=True, null=True)
    year_of_study = models.CharField(max_length=20, default="")
    representative_type = models.CharField(max_length=10, choices=REPRESENTATIVE_CHOICES, default='college')
    unique_id = models.CharField(max_length=50, default="")
    points = models.IntegerField(default=0)  # Add this line if points are needed

    def __str__(self):
        return self.name


class CollegeRepresentative(UserProfile):
    class Meta:
        proxy = True
        verbose_name = 'College Representative'
        verbose_name_plural = 'College Representatives'


class SchoolRepresentative(UserProfile):
    class Meta:
        proxy = True
        verbose_name = 'School Representative'
        verbose_name_plural = 'School Representatives'


# New Models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    added_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title


class UniqueID(models.Model):
    representative_type = models.CharField(max_length=50)  # 'college' or 'school'
    unique_id = models.CharField(max_length=50)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.unique_id


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    drive_link = models.URLField(max_length=200)
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    points_awarded = models.IntegerField(default=50)  # Initial 50 points for submission
    additional_points = models.IntegerField(default=0)  # Points to be awarded after verification

    def __str__(self):
        return f"{self.user.username} - {self.task.title}"
