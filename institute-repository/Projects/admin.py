from django.contrib import admin
from .models import *

# Register your models here.
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'projectName', 'projectDescription', 'projectType')
    search_fields = ('projectID', 'projectName', 'projectDescription', 'projectType')

class CourseProjectsAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'courseID', 'year', 'semester')
    search_fields = ('projectID', 'courseID', 'year', 'semester')

class ResearchProjectsAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'researchArea', 'startDate', 'endDate')
    search_fields = ('projectID', 'researchArea', 'startDate', 'endDate')

class ProjectInstructorsAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'kerberosID')
    search_fields = ('projectID', 'kerberosID')

class ProjectStudentsAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'kerberosID')
    search_fields = ('projectID', 'kerberosID')

class ProjectDocumentsAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'documentName', 'documentDescription')
    search_fields = ('projectID', 'documentName', 'documentDescription')   

class TagAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'tag')
    search_fields = ('projectID', 'tag')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseID', 'courseName', 'projectType')
    search_fields = ('courseID', 'courseName', 'projectType')

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('projectID', 'evaluationID')
    search_fields = ('projectID', 'evaluationID')

class RequestAdmin(admin.ModelAdmin):
    list_display = ('requestID', 'projectID', 'requestTo', 'requestStatus', 'requestFrom')
    search_fields = ('requestID', 'projectID', 'requestTo', 'requestStatus', 'requestFrom')


admin.site.register(Project, ProjectsAdmin)
admin.site.register(CourseProject, CourseProjectsAdmin)
admin.site.register(ResearchProject, ResearchProjectsAdmin)
admin.site.register(ProjectInstructor, ProjectInstructorsAdmin)
admin.site.register(ProjectStudent, ProjectStudentsAdmin)
admin.site.register(ProjectDocument, ProjectDocumentsAdmin)
admin.site.register(ProjectTag, TagAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Request, RequestAdmin)