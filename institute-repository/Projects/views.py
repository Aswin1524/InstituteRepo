from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Users.models import *
from Projects.models import *
from Users.dataValidation import *
from django.contrib.auth.models import User

# Create your views here.
@api_view(['POST'])
def createProject(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user.is_staff:
        return Response({'error': 'Not a student'}, status=status.HTTP_401_UNAUTHORIZED)
    data = request.data
    validateProject = validate_project(data)
    if(validateProject != True):
        return validateProject

    if (data['type'] == 'Course Project'):
        validateCourseProject = validate_course_project(data)
        if(validateCourseProject != True):
            return validateCourseProject
        
        project = Project.objects.create(projectName=data['name'], projectDescription=data['description'], type=data['type'])
        projectID = project.projectID
        course = Course.objects.get(courseID=data['courseID'])
        courseProject = CourseProject.objects.create(projectID=projectID, courseID=course, semester=data['semester'], year=data['year'])
        for i in data['instructors']:
            ProjectInstructor.objects.create(projectID=projectID, kerberosID=i)
        ProjectStudent.objects.create(projectID=projectID, kerberosID=request.user.username)
        for i in data['students']:
            if(i != request.user.username):
                ProjectStudent.objects.create(projectID=projectID, kerberosID=i)
        for i in data['tags']:
            ProjectTag.objects.create(projectID=projectID, tag=i)

        return Response({'message': 'Project created successfully'}, status=status.HTTP_201_CREATED)
    
    elif (data['type'] == 'Research Project'):
        validateResearchProject = validate_research_project(data)
        if(validateResearchProject != True):
            return validateResearchProject
        
        project = Project.objects.create(projectName=data['name'], projectDescription=data['description'], type=data['type'])
        projectID = project.projectID
        researchProject = ResearchProject.objects.create(projectID=projectID, researchArea=data['researchArea'], startDate=data['startDate'])
        for i in data['instructors']:
            ProjectInstructor.objects.create(projectID=projectID, kerberosID=i)
        ProjectStudent.objects.create(projectID=projectID, kerberosID=request.user.username)
        for i in data['students']:
            if(i != request.user.username):
                ProjectStudent.objects.create(projectID=projectID, kerberosID=i)
        for i in data['tags']:
            ProjectTag.objects.create(projectID=projectID, tag=i)
        
        return Response({'message': 'Project created successfully'}, status=status.HTTP_201_CREATED)
        
    else:
        return Response({'error': 'Invalid project type'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def createRequest(request):
    if not request.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    if request.user.is_staff:
        return Response({'error': 'Not a student'}, status=status.HTTP_401_UNAUTHORIZED)
    data = request.data
    validateRequest = validate_request(data)
    if(validateRequest != True):
        return validateRequest
    
    requestFrom = request.user.username
    requestTo = data['requestTo']
    projectID = data['projectID']
    requestDescription = data['description']
    document = data['document']
    request = Request.objects.create(requestFrom=requestFrom, requestTo=requestTo, projectID=projectID, requestDescription=requestDescription, document=document)
    return Response({'message': 'Request created successfully'}, status=status.HTTP_201_CREATED)

    
