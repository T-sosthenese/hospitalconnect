from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_admin = models.BooleanField("is admin", default=False)
    is_doctor = models.BooleanField("is doctor", default=False)
    is_patient = models.BooleanField("is patient", default=False)
    

departments = [
    ('Cardiologist', 'Cardiologist'),
    ('Oncologists', 'Oncologists'),
    ('Ophthalmologists', 'Ophthalmologists'),
    ('Orthopedic Surgeons', 'Orthopedic Surgeons'),
    ('Pediatricians', 'Pediatricians'),
    ('Physiatrists', 'Physiatrists'),
    ('Pulmonologists', 'Pulmonologists'),
    ('Radiologists', 'Radiologists'),
    ('Rheumatologists', 'Rheumatologists'),
    ('Urologists', 'Urologists'),
    ('Vascular Surgeons', 'Vascular Surgeons'),
]

# Model for Doctors
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, choices=departments, default='Cardiologist')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.department})"

# Model for Patients
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=100, null=False)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='patients')
    admit_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.symptoms})"