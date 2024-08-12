from django.contrib import admin

from grades.models import Subject, Restriction, Course, Inscription, CourseInscription

# Register your models here.
admin.site.register(Subject)
admin.site.register(Restriction)
admin.site.register(Course)
admin.site.register(Inscription)
admin.site.register(CourseInscription)
