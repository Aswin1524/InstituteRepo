import requests
from Users.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
from django.contrib.auth.models import User
import ldap
from django.contrib.auth import logout
from Users.dataValidation import *
import os

l = ldap.initialize('ldap://ldap2.iitd.ac.in')
l.protocol_version = ldap.VERSION3

# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


@api_view(['GET'])
def user(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(kerberosID=request.user.username)
        name = profile.name
        email = profile.email
        phoneNumber = profile.phoneNumber
        category = profile.category
        if category == 'Student':
            student = Student.objects.get(kerberosID=request.user.username)
            entryNumber = student.entryNumber
            programme = student.programme
            # projects = ProjectStudents.objects.filter(kerberosID=request.user.kerberosID)
            return Response({'name': name, 'email': email, 'phoneNumber': phoneNumber, 'entryNumber': entryNumber, 'programme': programme}, status=status.HTTP_200_OK)
        elif category == 'Faculty':
            faculty = Instructor.objects.get(kerberosID=request.user.username)
            deptID = faculty.deptID
            uid = faculty.uid
            return Response({'name': name, 'email': email, 'phoneNumber': phoneNumber, 'deptID': deptID, 'uid': uid}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
def login(request):
    data = request.data
    code = data['code']
    #get client_id and client_secret from environment variables
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    res = requests.post('https://oauth.iitd.ac.in/token.php', data={'grant_type': 'authorization_code', 'code': code, 'client_id': client_id, 'client_secret': client_secret})
    if res.status_code != 200:
        return Response({'error': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
    access_token = res.json()['access_token']
    res = requests.post('https://oauth.iitd.ac.in/resource.php', data={'access_token': access_token})
    if res.status_code != 200:
        return Response({'error': 'Login Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
    data = res.json()
    kerberosID = data['user_id']
    mail = data['mail']
    name = data['name']
    uniqueIITDid = data['uniqueiitdid']
    category = data['category']
    department = data['department']

    if(category=='faculty'):
        instructors = Instructor.objects.filter(kerberosID=kerberosID)
        if not instructors.exists():
            people = Profile.objects.filter(kerberosID=kerberosID)
            if not people.exists():
                people = Profile.objects.create(kerberosID=kerberosID, name=name, email=mail, category='Faculty')
            instructors = Instructor.objects.create(kerberosID=kerberosID, uid=uniqueIITDid, deptID=department)
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=[];',./{}|:<>?"
            password = ""
            for i in range(16):
                password += random.choice(chars)
            user = User.objects.create_user(username=kerberosID, password=password, is_staff=True)
            return Response({'message': 'Login successful', 'token': get_tokens_for_user(user), 'type': 'faculty'}, status=status.HTTP_200_OK)
        else:
            user = User.objects.get(username=kerberosID)
            return Response({'message': 'Login successful', 'token': get_tokens_for_user(user), 'type': 'faculty'}, status=status.HTTP_200_OK)
    else:
        student = Student.objects.filter(kerberosID=kerberosID)
        if not student.exists():
            people = Profile.objects.filter(kerberosID=kerberosID)
            if not people.exists():
                people = Profile.objects.create(kerberosID=kerberosID, name=name, email=mail, category='Student')
            student = Student.objects.create(kerberosID=kerberosID, entryNumber=uniqueIITDid, programme=category, deptID=department)
            chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=[];',./{}|:<>?"
            password = ""
            for i in range(16):
                password += random.choice(chars)
            user = User.objects.create_user(username=kerberosID, password=password)
            return Response({'message': 'Login successful', 'token': get_tokens_for_user(user), 'type': 'student'}, status=status.HTTP_200_OK)
        else:
            user = User.objects.get(username=kerberosID)
            return Response({'message': 'Login successful', 'token': get_tokens_for_user(user), 'type': 'student'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def signupStudent(request):
#     data = request.data
#     validate_signup = validate_signup(data)
#     if(validate_signup != True):
#         return Response({'error': validate_signup}, status=status.HTTP_400_BAD_REQUEST)
#     student = Student.objects.filter(kerberosID=data['kerberosID'])
#     if student:
#         return Response({'error': 'Kerberos already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # check LDAP for kerberosID
#     binddn = 'ou=IITDpersonDetails,dc=cse,dc=iitd,dc=ernet,dc=in'
#     searchFilter = '(&(uid='+data['kerberosID']+'))'
#     searchAttribute = ['category','department','username','uniqueIITDid']
#     result = l.search(binddn, ldap.SCOPE_SUBTREE, searchFilter, searchAttribute)
#     result_type, result_data = l.result(result, 0)

#     # if kerberosID not found:
#     if(result_type != ldap.RES_SEARCH_ENTRY):
#         return Response({'error': 'Kerberos ID not found'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # create user
#     category = result_data[0][1].get('category')
#     category = category[0].decode('utf-8')
#     department = result_data[0][1].get('department')
#     department = department[0].decode('utf-8')
#     name = result_data[0][1].get('username')
#     name = name[0].decode('utf-8')
#     entryNumber = result_data[0][1].get('uniqueIITDid')
#     entryNumber = entryNumber[0].decode('utf-8')

#     binddn = 'ou=AddressBook,dc=cse,dc=iitd,dc=ernet,dc=in'
#     searchAttribute = ['mail']
#     result = l.search(binddn, ldap.SCOPE_SUBTREE, searchFilter, searchAttribute)
#     result_type, result_data = l.result(result, 0)

#     if(result_type != ldap.RES_SEARCH_ENTRY):
#         return Response({'error': 'Kerberos not found'}, status=status.HTTP_400_BAD_REQUEST)
    

#     mail = result_data[0][1].get('mail')
#     mail = mail[0].decode('utf-8')
#     people = Profile.objects.filter(kerberosID=data['kerberosID'])
#     if not people.exists():
#         people = Profile.objects.create(kerberosID=data['kerberosID'], name=name, email=mail, phoneNumber=data['phoneNumber'], category='Student')
#     student = Student.objects.create(kerberosID=data['kerberosID'], entryNumber=entryNumber, programme=category, deptID=department)
#     # create user in django auth with random password
#     chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=[];',./{}|:<>?"
#     password = ""
#     for i in range(16):
#         password += random.choice(chars)
#     user = User.objects.create_user(username=data['kerberosID'], password=password)
#     return Response({'message': 'Student added successfully'}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def signupFaculty(request):
#     data = request.data
#     validate_signup = validate_signup(data)
#     if(validate_signup != True):
#         return Response({'error': validate_signup}, status=status.HTTP_400_BAD_REQUEST)
#     instructors = Instructor.objects.filter(kerberosID=data['kerberosID'])
#     if instructors:
#         return Response({'error': 'Kerberos already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # check LDAP for kerberosID
#     binddn = 'ou=IITDpersonDetails,dc=cse,dc=iitd,dc=ernet,dc=in'
#     searchFilter = '(&(uid='+data['kerberosID']+'))'
#     searchAttribute = ['category','department','username','uniqueIITDid']
#     result = l.search(binddn, ldap.SCOPE_SUBTREE, searchFilter, searchAttribute)
#     result_type, result_data = l.result(result, 0)

#     # if kerberosID not found:
#     if(result_type != ldap.RES_SEARCH_ENTRY):
#         return Response({'error': 'Kerberos ID not found'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # create user
#     category = result_data[0][1].get('category')
#     category = category[0].decode('utf-8')
#     if(category != 'faculty'):
#         return Response({'error': 'Kerberos ID not a faculty'}, status=status.HTTP_401_UNAUTHORIZED)
#     department = result_data[0][1].get('department')
#     department = department[0].decode('utf-8')
#     name = result_data[0][1].get('username')
#     name = name[0].decode('utf-8')
#     uid = result_data[0][1].get('uniqueIITDid')
#     uid = uid[0].decode('utf-8')

#     binddn = 'ou=AddressBook,dc=cse,dc=iitd,dc=ernet,dc=in'
#     searchAttribute = ['mail']
#     result = l.search(binddn, ldap.SCOPE_SUBTREE, searchFilter, searchAttribute)
#     result_type, result_data = l.result(result, 0)

#     if(result_type != ldap.RES_SEARCH_ENTRY):
#         return Response({'error': 'Kerberos not found'}, status=status.HTTP_400_BAD_REQUEST)
    

#     mail = result_data[0][1].get('mail')
#     mail = mail[0].decode('utf-8')

#     people = Profile.objects.filter(kerberosID=data['kerberosID'])
#     if not people.exists():
#         people = Profile.objects.create(kerberosID=data['kerberosID'], name=name, email=mail, phoneNumber=data['phoneNumber'], category='Faculty')
#     instructors = Instructor.objects.create(kerberosID=data['kerberosID'], uid=uid, deptID=department)
#     # create user in django auth with random password
#     chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-=[];',./{}|:<>?"
#     password = ""
#     for i in range(16):
#         password += random.choice(chars)
#     user = User.objects.create_user(username=data['kerberosID'], password=password, is_staff=True)
#     return Response({'message': 'Faculty added successfully'}, status=status.HTTP_201_CREATED)

# @api_view(['POST'])
# def loginFaculty(request):
#     data = request.data
#     if ('kerberosID' not in data):
#         return Response({'error': 'Kerberos ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
#     if ('password' not in data):
#         return Response({'error': 'Password not provided'}, status=status.HTTP_400_BAD_REQUEST)
#     #check oAuth for kerberosID and password and token
#     if ('token' not in data):
#         return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
#     # oAuth token validation
#     # if token not valid:
#     # return Response({'error': 'Token not valid'}, status=status.HTTP_400_BAD_REQUEST)
#     profile = Instructor.objects.filter(kerberosID=data['kerberosID'])
#     if not profile.exists():
#         return Response({'error': 'Faculty not found'}, status=status.HTTP_401_UNAUTHORIZED)
#     user = User.objects.get(username=data['kerberosID'])
#     if not user.is_staff:
#         return Response({'error': 'Not a faculty'}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({'message': 'Login successful', 'token': get_tokens_for_user(user)}, status=status.HTTP_200_OK)

@api_view(['POST'])
def userLogout(request):
    data = request.data
    if ('kerberosID' not in data):
        return Response({'error': 'Kerberos ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if ('token' not in data):
        return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
    # oAuth token validation
    # if token not valid:
    # return Response({'error': 'Token not valid'}, status=status.HTTP_400_BAD_REQUEST)
    # remove token from database
    if not request.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
    
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

