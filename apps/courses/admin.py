from django.contrib import admin

from apps.courses.models import Course, Lesson

admin.site.register(Course)
admin.site.register(Lesson)
