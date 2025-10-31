from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime
from django.utils import timezone
def get_today_date():
    return datetime.now().date()

def get_current_time():
    return datetime.now().time()


class Course(models.Model):
    CLASS_CHOICES = [
        ('MSA', 'Modern Standard Arabic'),
        ('AC', 'Arabic For Children'),
        ('CC', 'Conversation Club'),
        ('AI', 'Arabic for Islamic Studies'),
        ('LCA', 'Levant Colloquial Arabic'),
        ('BA', 'Business and Tourism Arabic'),
        ('NEW', 'New Class Choice'),
    ]
    name = models.CharField(max_length=10, choices=CLASS_CHOICES)



class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    courses_taught = models.ManyToManyField(Course)

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance_hours = models.IntegerField(default=0)
    balance_minutes = models.IntegerField(default=0)


class Event(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Booked', 'Booked'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"Teacher: {self.teacher}, Status: {self.status}"

    class Meta:
        ordering = ['start_time']

class Class(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
   

class ClassRequest(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_and_time_requested = models.DateTimeField()
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
