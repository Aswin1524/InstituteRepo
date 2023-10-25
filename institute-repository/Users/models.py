from django.db import models
# from Projects.models import Project, ResearchProject

# Create your models here.
class Profile(models.Model):
    kerberosID = models.CharField(max_length=20, primary_key=True, unique=True,verbose_name="Kerberos ID", serialize=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phoneNumber = models.CharField(max_length=15,null=True, blank=True)
    categoryChoices = [('Student', 'Student'), ('Faculty', 'Faculty')]
    category = models.CharField(max_length=100, choices=categoryChoices, default='Student')
    def __str__(self):
        return f"{self.kerberosID} - {self.name}"

class Student(models.Model):
    kerberosID = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, unique=True, serialize=False)
    deptID = models.CharField(max_length=10)
    entryNumber = models.CharField(max_length=11, unique=True)
    PROGRAMME_CHOICES = [('B.Tech', 'B.Tech'), ('M.Tech', 'M.Tech'), ('PhD', 'PhD'), ('PostDoc', 'PostDoc'), ('MSc', 'MSc'), ('Dual Degree', 'Dual Degree')]
    programme = models.CharField(max_length=100,choices=PROGRAMME_CHOICES, default='B.Tech')
    def __str__(self):
        return f"{self.kerberosID} - {self.deptID} - {self.entryNumber} - {self.programme}"
    
class Instructor(models.Model):
    kerberosID = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True, unique=True, serialize=False)
    deptID = models.CharField(max_length=10, blank=True, null=True)
    uid = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return self.kerberosID
    
