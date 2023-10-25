from django.contrib import admin
from .models import *

# Register your models here.
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('kerberosID', 'name', 'email', 'phoneNumber')
    search_fields = ('kerberosID', 'name', 'email', 'phoneNumber')

class StudentsAdmin(admin.ModelAdmin):
    list_display = ('kerberosID', 'entryNumber', 'programme')
    search_fields = ('kerberosID', 'entryNumber', 'programme')

class InstructorsAdmin(admin.ModelAdmin):
    list_display = ('kerberosID', 'deptID')
    search_fields = ('kerberosID', 'deptID')




admin.site.register(Profile, PeopleAdmin)
admin.site.register(Student, StudentsAdmin)
admin.site.register(Instructor, InstructorsAdmin)
