from rest_framework import status
from rest_framework.response import Response
from Users.models import *
from Projects.models import *

def validate_signup(data):
    if ('kerberosID' not in data):
        return 'Kerberos ID not provided'
    if ('phoneNumber' not in data):
        return 'Phone number not provided'
    return True

def validate_project(data):
    if ('name' not in data):
        return Response({'error': 'Project name not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if ('description' not in data):
        return Response({'error': 'Project description not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if ('type' not in data):
        return Response({'error': 'Project type not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if ('instructors' not in data or len(data['instructors']) == 0):
        return Response({'error': 'Instructors not provided'}, status=status.HTTP_400_BAD_REQUEST)    
    if data['type'] not in ['Course Project', 'Research Project']:
        return Response({'error': 'Project type not valid'}, status=status.HTTP_400_BAD_REQUEST)

    if(len(data['instructors']) != len(set(data['instructors']))):
        return Response({'error': 'Repeated instructors'}, status=status.HTTP_400_BAD_REQUEST)

    for instructor in data['instructors']:
        i = Instructor.objects.filter(kerberosID=instructor).exists()
        if not i:
            return Response({'error': f'Invalid instructor {instructor}'}, status=status.HTTP_400_BAD_REQUEST)
        
    if(len(data['students']) != len(set(data['students']))):
        return Response({'error': 'Repeated students'}, status=status.HTTP_400_BAD_REQUEST)
        
    for students in data['students']:
        i = Student.objects.filter(kerberosID=students).exists()
        if not i:
            return Response({'error': f'Invalid student {students}'}, status=status.HTTP_400_BAD_REQUEST)
        
    # check for repeated tags
    if len(data['tags']) != len(set(data['tags'])):
        return Response({'error': 'Repeated tags'}, status=status.HTTP_400_BAD_REQUEST)
    
    return True

def validate_course_project(data):
    if('courseID' not in data):
        return Response({'error': 'Course ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if('year' not in data):
        return Response({'error': 'Year not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if('semester' not in data):
        return Response({'error': 'Semester not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not Course.objects.filter(courseID=data['courseID']).exists():
        return Response({'error': 'Course ID not valid'}, status=status.HTTP_400_BAD_REQUEST)
    
    return True

def validate_research_project(data):
    if('researchArea' not in data):
        return Response({'error': 'Research area not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if('startDate' not in data):
        return Response({'error': 'Start date not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    return True

def validate_request(data):
    if('requestTo' not in data):
        return Response({'error': 'Request Addressed to person not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if('description' not in data):
        return Response({'error': 'Request description not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    return True
    