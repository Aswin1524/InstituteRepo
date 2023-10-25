from django.db import models
from Users.models import Profile, Student, Instructor

# Create your models here.
class Course(models.Model):
    courseID = models.CharField(max_length=10, primary_key=True, unique=True, serialize=False)
    courseName = models.CharField(max_length=100)
    projectTypeChoices = [('Mini Project', 'Mini Project'), ('B.Tech Project', 'B.Tech Project'), ('M.Tech Project', 'M.Tech Project')]
    projectType = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.courseID} - {self.courseName} - {self.projectType}"
    
class Project(models.Model):
    projectID = models.AutoField(primary_key=True, unique=True, serialize=False)
    projectName = models.CharField(max_length=100)
    projectDescription = models.TextField()
    projectTypeChoices = [('Course Project', 'Course Project'), ('Research Project', 'Research Project')]
    projectType = models.CharField(max_length=100, choices=projectTypeChoices, default='Course Project')
    def __str__(self):
        return f"{self.projectID} - {self.projectName} - {self.projectDescription} - {self.projectType}"
    
class CourseProject(models.Model):
    projectID = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True, unique=True, serialize=False)
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    midTermEvaluation = models.BooleanField(default=False)
    midTermEvaluationDate = models.DateField(blank=True, null=True)
    midTermEvaluationRemarks = models.TextField(blank=True, null=True)
    endTermEvaluation = models.BooleanField(default=False)
    endTermEvaluationDate = models.DateField(blank=True, null=True)
    endTermEvaluationRemarks = models.TextField(blank=True, null=True)
    semester = models.IntegerField()
    def __str__(self):
        return f"{self.projectID} - {self.courseID} - {self.year} - {self.semester}"
    
class ResearchProject(models.Model):
    projectID = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True, unique=True, serialize=False)
    researchArea = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    def __str__(self):
        return f"{self.projectID} - {self.researchArea} - {self.startDate} - {self.endDate}"
    
class ProjectTag(models.Model):
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['projectID', 'tag'], name='unique_project_tag')
        ]

    def __str__(self):
        return f"{self.projectID} - {self.tag}"

class ProjectInstructor(models.Model):
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE)
    kerberosID = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    isApproved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['projectID', 'kerberosID'], name='unique_project_instructor')
        ]

    def __str__(self):
        return f"{self.kerberosID} - {self.projectID} - {self.isApproved}"
    
class ProjectStudent(models.Model):
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE)
    kerberosID = models.ForeignKey(Student, on_delete=models.CASCADE)
    isApproved = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['projectID', 'kerberosID'], name='unique_project_student')
        ]

    def __str__(self):
        return f"{self.kerberosID} - {self.projectID} - {self.isApproved}"
    
class ProjectDocument(models.Model):
    documentID = models.AutoField(primary_key=True, unique=True, serialize=True)
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE)
    documentName = models.FileField(upload_to='documents/',blank=False)
    documentDescription = models.TextField()
    uploadedBy = models.ForeignKey(Profile, on_delete=models.CASCADE)
    uploadedOn = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.projectID} - {self.documentName} - {self.uploadedBy} - {self.uploadedOn}"
    
    
class Evaluation(models.Model):
    evaluationID = models.AutoField(primary_key=True, unique=True, serialize=True)
    projectID = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    deadline = models.DateField()
    evaluationDate = models.DateField()
    evaluationCompleted = models.BooleanField(default=False)
    evaluationRemarks = models.TextField()
    def __str__(self):
        return f"{self.projectID} - {self.evaluationDate} - {self.evaluationType} - {self.evaluationRemarks}"

    
class Request(models.Model):
    requestID = models.AutoField(primary_key=True, unique=True, serialize=True)
    projectID = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    requestTo = models.ForeignKey(Instructor, on_delete=models.CASCADE, blank=True, null=True)
    requestFrom = models.ForeignKey(Profile, on_delete=models.CASCADE)
    requestDescription = models.TextField()
    requestStatusChoices = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Forwarded', 'Forwarded')]
    requestStatus = models.CharField(max_length=100, choices=requestStatusChoices, default='Pending')
    supportingDocuments = models.FileField(upload_to='documents/',blank=True, null=True)
    requestDate = models.DateField(auto_now_add=True)
    requestRemarks = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.projectID} - {self.requestStatus} - {self.requestDate}"