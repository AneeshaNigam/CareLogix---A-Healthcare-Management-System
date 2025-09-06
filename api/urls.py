from django.urls import path
from . import views

urlpatterns = [
    # Authentication APIs
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    
    # Patient Management APIs
    path('patients/', views.add_patient, name='add_patient'),
    path('patients/', views.get_patients, name='get_patients'),
    path('patients/<int:id>/', views.get_patient, name='get_patient'),
    path('patients/<int:id>/update/', views.update_patient, name='update_patient'),
    path('patients/<int:id>/delete/', views.delete_patient, name='delete_patient'),
    
    # Doctor Management APIs
    path('doctors/', views.add_doctor, name='add_doctor'),
    path('doctors/', views.get_doctors, name='get_doctors'),
    path('doctors/<int:id>/', views.get_doctor, name='get_doctor'),
    path('doctors/<int:id>/update/', views.update_doctor, name='update_doctor'),
    path('doctors/<int:id>/delete/', views.delete_doctor, name='delete_doctor'),
    
    # Patient-Doctor Mapping APIs
    path('mappings/', views.assign_doctor, name='assign_doctor'),
    path('mappings/', views.get_mappings, name='get_mappings'),
    path('mappings/<int:patient_id>/', views.get_patient_doctors, name='get_patient_doctors'),
    path('mappings/<int:id>/delete/', views.remove_mapping, name='remove_mapping'),
]