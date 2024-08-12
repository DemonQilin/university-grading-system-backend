from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Professor

admin.site.register(Student, UserAdmin)
admin.site.register(Professor, UserAdmin)
