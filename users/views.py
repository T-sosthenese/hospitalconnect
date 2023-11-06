from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect 
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Doctor, Patient
from appointment.models import Appointment
from medicalrecords.models import PatientRecords


# View for the homepage
def home_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'home.html')


# Displays admin's signup/login buttons
def adminclick_view(request):
    return render(request,'users/adminclick.html')


# Views for the program's general information
def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})

def admin_signup_view(request):
    if request.method == 'POST':
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                # Authenticating the user after registration
                auth_user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                if auth_user is not None:
                    login(request, auth_user)
                    messages.success(request, "Registration and Login successful.")
                    return redirect('adminlogin')

            # Handling a situation where user creation was successful but login failed
            messages.error(request, "Unsuccessful login after registration.")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")

    form = forms.AdminSignupForm()
    return render(request, 'users/adminsignup.html', {'form': form})


def login_view(request, form_class, template_name, redirect_url):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = form_class()

    return render(request=request, template_name=template_name, context={"login_form": form})

def admin_login_view(request):
    return login_view(request, forms.AdminLoginForm, "users/adminlogin.html", "admin-dashboard")

def doctorlogin_view(request):
    return login_view(request, forms.DoctorLoginForm, "users/doctorlogin.html", "doctor-dashboard")

def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors = Doctor.objects.all().order_by('-id')
    patients = Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount = Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = Doctor.objects.all().filter(status=False).count()

    patientcount = Patient.objects.all().filter(status=True).count()
    pendingpatientcount = Patient.objects.all().filter(status=False).count()

    appointmentcount =  Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'users/admin-dashboard.html',context=mydict)

def logout_view(request):
    logout(request)
    return redirect('home')

# Doctor-related views
def doctorclick_view(request):
    return render(request,'users/doctorclick.html')

def doctor_signup_view(request):
    userForm = forms.DoctorSignupForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}

    if request.method == 'POST':
        userForm = forms.DoctorSignupForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.save()

            print("saved")

            # Authenticating the user after successful signup
            auth_user = authenticate(username=user.username, password=user.password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Registration and Login successful.")
                print("authenticated")
                return redirect('doctorlogin')
            else:
                messages.error(request, "Unsuccessful login after registration.")

    return render(request, 'users/doctorsignup.html', context=mydict)




def doctor_dashboard_view(request):
    # Information for card display
    patientcount = Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount = Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged = PatientRecords.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    # For displaying table in doctor dashboard
    appointments = Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients = Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'users/doctor_dashboard.html',context=mydict)