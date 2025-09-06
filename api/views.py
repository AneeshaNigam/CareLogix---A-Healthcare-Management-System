from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer, 
    PatientSerializer, 
    DoctorSerializer, 
    PatientDoctorMappingSerializer
)

# Authentication APIs
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    POST /api/auth/register/
    Register a new user with name, email, and password.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    POST /api/auth/login/
    Log in a user and return a JWT token.
    """
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

# Patient Management APIs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient(request):
    """
    POST /api/patients/
    Add a new patient (Authenticated users only).
    """
    data = request.data.copy()
    data['user'] = request.user.id
    
    serializer = PatientSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Patient created successfully',
            'patient': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patients(request):
    """
    GET /api/patients/
    Retrieve all patients created by the authenticated user.
    """
    patients = Patient.objects.filter(user=request.user)
    serializer = PatientSerializer(patients, many=True)
    return Response({
        'count': patients.count(),
        'patients': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request, id):
    """
    GET /api/patients/<id>/
    Get details of a specific patient.
    """
    patient = get_object_or_404(Patient, id=id, user=request.user)
    serializer = PatientSerializer(patient)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_patient(request, id):
    """
    PUT /api/patients/<id>/
    Update patient details.
    """
    patient = get_object_or_404(Patient, id=id, user=request.user)
    serializer = PatientSerializer(patient, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Patient updated successfully',
            'patient': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_patient(request, id):
    """
    DELETE /api/patients/<id>/
    Delete a patient record.
    """
    patient = get_object_or_404(Patient, id=id, user=request.user)
    patient.delete()
    return Response({'message': 'Patient deleted successfully'})

# Doctor Management APIs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_doctor(request):
    """
    POST /api/doctors/
    Add a new doctor (Authenticated users only).
    """
    data = request.data.copy()
    data['user'] = request.user.id
    
    serializer = DoctorSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Doctor created successfully',
            'doctor': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctors(request):
    """
    GET /api/doctors/
    Retrieve all doctors created by the authenticated user.
    """
    doctors = Doctor.objects.filter(user=request.user)
    serializer = DoctorSerializer(doctors, many=True)
    return Response({
        'count': doctors.count(),
        'doctors': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor(request, id):
    """
    GET /api/doctors/<id>/
    Get details of a specific doctor.
    """
    doctor = get_object_or_404(Doctor, id=id, user=request.user)
    serializer = DoctorSerializer(doctor)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_doctor(request, id):
    """
    PUT /api/doctors/<id>/
    Update doctor details.
    """
    doctor = get_object_or_404(Doctor, id=id, user=request.user)
    serializer = DoctorSerializer(doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Doctor updated successfully',
            'doctor': serializer.data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_doctor(request, id):
    """
    DELETE /api/doctors/<id>/
    Delete a doctor record.
    """
    doctor = get_object_or_404(Doctor, id=id, user=request.user)
    doctor.delete()
    return Response({'message': 'Doctor deleted successfully'})

# Patient-Doctor Mapping APIs
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_doctor(request):
    """
    POST /api/mappings/
    Assign a doctor to a patient.
    """
    patient_id = request.data.get('patient')
    doctor_id = request.data.get('doctor')
    
    # Check if patient and doctor belong to the user
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    doctor = get_object_or_404(Doctor, id=doctor_id, user=request.user)
    
    # Check if mapping already exists
    if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
        return Response({
            'error': 'This doctor is already assigned to this patient'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    mapping = PatientDoctorMapping(patient=patient, doctor=doctor)
    mapping.save()
    
    serializer = PatientDoctorMappingSerializer(mapping)
    return Response({
        'message': 'Doctor assigned to patient successfully',
        'mapping': serializer.data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mappings(request):
    """
    GET /api/mappings/
    Retrieve all patient-doctor mappings for the authenticated user.
    """
    mappings = PatientDoctorMapping.objects.filter(patient__user=request.user)
    serializer = PatientDoctorMappingSerializer(mappings, many=True)
    return Response({
        'count': mappings.count(),
        'mappings': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_doctors(request, patient_id):
    """
    GET /api/mappings/<patient_id>/
    Get all doctors assigned to a specific patient.
    """
    patient = get_object_or_404(Patient, id=patient_id, user=request.user)
    mappings = PatientDoctorMapping.objects.filter(patient=patient)
    serializer = PatientDoctorMappingSerializer(mappings, many=True)
    return Response({
        'patient': patient.name,
        'doctors_count': mappings.count(),
        'doctors': serializer.data
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_mapping(request, id):
    """
    DELETE /api/mappings/<id>/
    Remove a doctor from a patient.
    """
    mapping = get_object_or_404(PatientDoctorMapping, id=id, patient__user=request.user)
    mapping.delete()
    return Response({'message': 'Doctor removed from patient successfully'})