from django import forms
from .models import CustomUser, Patient, Doctor
from appointment.models import Appointment

# Base User form for user creation
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

# Doctor user form
class DoctorUserForm(UserForm):
    class Meta(UserForm.Meta):
        pass  # No extra fields for doctor user form for now

# Form for Doctor details
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']

# Patient user form
class PatientUserForm(UserForm):
    class Meta(UserForm.Meta):
        pass  # No extra fields for patient user form for now

# Form for Patient details
class PatientForm(forms.ModelForm):
    assignedDoctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(status=True),
        empty_label="Name and Department",
        to_field_name="user_id"
    )

    class Meta:
        model = Patient
        fields = ['address', 'mobile', 'symptoms', 'assignedDoctorId', 'status', 'profile_pic']

# Appointment Form
class AppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(status=True),
        empty_label="Doctor Name and Department",
        to_field_name="user_id"
    )
    patientId = forms.ModelChoiceField(
        queryset=Patient.objects.filter(status=True),
        empty_label="Patient Name and Symptoms",
        to_field_name="user_id"
    )

    class Meta:
        model = Appointment
        fields = ['description', 'status']

# Patient Appointment Form
class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(status=True),
        empty_label="Doctor Name and Department",
        to_field_name="user_id"
    )

    class Meta:
        model = Appointment
        fields = ['description', 'status']

# Contact Us Form
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
