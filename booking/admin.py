from django.contrib import admin
from .models import Course, Teacher, Student, Class, ClassRequest

admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(ClassRequest)

