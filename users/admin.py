from django.contrib import admin
from .models import Doctor, Patient
from medicalrecords.models import PatientRecords
from appointment.models import Appointment


class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientRecordsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientRecords, PatientRecordsAdmin)
