from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import LoginForm, RegisterForm, EditProfileForm, EditUserForm, AddDoctorForm, BookAppointmentForm, DoctorLoginForm
from .models import Profile, Doctor, Appiontment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.messages import constants as message_constants
from django.views.decorators.cache import cache_control
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from datetime import time, timedelta

MESSAGE_TAGS = {
    message_constants.SUCCESS: 'success bg-green-100 text-green-800 border-green-300',
    message_constants.ERROR: 'error bg-red-100 text-red-800 border-red-300',
}

# Create your views here.
def home(request):
    doctors = Doctor.objects.all()[:8]

    context = {'doctors':doctors}
    return render(request, "users/home.html",context=context)

def user_login(request):

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user=user)
                messages.success(request, "Login successfull")
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        login_form = LoginForm()
    
    context = {'login_form': login_form}

    return render(request, "users/login_form.html",context=context)

@login_required(login_url='login')
def user_logout(request):

    logout(request)
    messages.success(request, "Logout Successfull")

    return redirect('login')

def register_user(request):

    if request.method == 'POST':
        user_form = RegisterForm(data=request.POST)

        email = request.POST.get('email')
        username = request.POST.get('username')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")

        if user_form.is_valid():
            password = user_form.cleaned_data['password']
            new_form = user_form.save(commit=False)
            new_form.set_password(password)
            new_form.save()
            Profile.objects.create(user=new_form)
            messages.success(request, "User registered successfully")
            return redirect('login')
        else:
            messages.error(request,"Some error occured... please try again")
        
    else:
        user_form = RegisterForm()

    context = {'user_form': user_form}

    return render(request, "users/register_form.html", context=context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def edit_user(request):

    if request.method == 'POST':
        user_form = EditUserForm(instance=request.user, data=request.POST)
        profile_form = EditProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Profile updated successfully")
            return redirect('profile')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, "users/edit_profile.html", context=context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def view_profile(request):

    user_profile = Profile.objects.filter(user=request.user)

    context = {
               'user_profile': user_profile
               }
    return render(request, "users/view_profile.html", context=context)

def about_us(request):

    return render(request, "users/about.html")

def contact_us(request):

    return render(request, "users/contact.html")

# doctor related views
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def add_doctor(request):

    if request.method == 'POST':
        form = AddDoctorForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            doctor = form.save(commit=False)
            raw_password = form.cleaned_data['password']
            doctor.set_password(raw_password)
            doctor.save()
            messages.success(request,"Doctor added successfully")
            return redirect('add_doctor')

    else:
        form = AddDoctorForm()
    
    context={'form':form}
    return render(request, "users/add_doctor.html", context=context)

def doctor_login(request):
    if request.session.get('doctor_id'):
        return redirect('doctor_dashboard')
        
    if request.method == 'POST':
        form = DoctorLoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            doctor = Doctor.objects.get(email=email)
            request.session['doctor_id'] = doctor.id
            messages.success(request, 'Login Successfull')
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    else:
        form = DoctorLoginForm()
    
    context = {'form': form}

    return render(request, "users/doctor_login.html", context=context)

def doctor_logout(request):

    if 'doctor_id' in request.session:
        del request.session['doctor_id']
        messages.success(request,'Logout successfull')

    return redirect('doctor_login')

def all_doctors(request, speciality):

    if speciality == 'all':
        docs = Doctor.objects.all()
    else:
        docs = Doctor.objects.filter(speciality = speciality)

    context = {'docs': docs}

    return render(request, "users/all_doctors.html", context=context)

def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        return redirect('doctor_login')

    doctor = Doctor.objects.get(id=doctor_id)
    appointments = Appiontment.objects.filter(doctor=doctor)
    total_appointments = Appiontment.objects.filter(doctor=doctor).count()
    appointment_count = Appiontment.objects.filter(doctor=doctor, status='Complete').count()
    patient_count = Appiontment.objects.filter(doctor_id=doctor_id).values('patient').distinct().count()
    doctor_fees = doctor.fees
    total_earnings = appointment_count * doctor_fees

    context = {
        'doctor': doctor,
        'appointments' : appointments,
        'total_earnings': total_earnings,
        'total_appointments': total_appointments,
        'patient_count': patient_count,
    }

    return render(request, "users/doctor_dashboard.html", context=context)

def doctor_appointments(request):
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        return redirect('doctor_login')
    
    doctor = get_object_or_404(Doctor, id = doctor_id)

    appointments = Appiontment.objects.filter(doctor=doctor)

    context = {'appointments':appointments}

    return render(request, "users/doctor_appointments.html", context=context)

# appointments views
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def book_appointment(request, slug):

    doctor = get_object_or_404(Doctor, slug=slug)
    patient = request.user
    if request.method == 'POST':
        form = BookAppointmentForm(data=request.POST)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.doctor = doctor
            new_form.patient = patient
            new_form.save()
            messages.success(request, "Appointment booked successfully")
            return redirect('appointments')
    else:
        form = BookAppointmentForm()

    context = {'form':form,
               'doctor':doctor,
               }

    return render(request, "users/book_appointment.html",context=context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def my_appointments(request):

    my_appointments = Appiontment.objects.filter(patient=request.user)

    context = {'appointments':my_appointments}

    return render(request, "users/my_appointments.html", context=context)

def cancel_appointment(request, id):

    appointment = get_object_or_404(Appiontment,id=id)

    if appointment.status != 'Cancelled' and appointment.status == 'Scheduled':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, "Appointment Cancelled")
    else:
        messages.error(request, "Cannot cancel appointment")
    
    return redirect('appointments')

def complete_appointment(request, id):
    appointment = get_object_or_404(Appiontment,id=id)

    if appointment.status != 'Cancelled' and appointment.status != 'Complete' and appointment.status == 'Scheduled':
        appointment.status = 'Complete'
        appointment.save()
        messages.success(request, "Appointment Complete")
    else:
        messages.error(request, "Cannot complete appointment")
    
    return redirect('doctor_appointments')

# admin views
def admin_login(request):

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_superuser:
                login(request,user=user)
                messages.success(request, "Login successfull")
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        login_form = LoginForm()
    
    context = {'login_form': login_form}

    return render(request, "users/admin_login.html",context=context)

def admin_check(user):
    return user.is_superuser

@user_passes_test(admin_check)
def admin_dashboard(request):

    appointments = Appiontment.objects.all().order_by('-appointment_date')[:5]
    total_appointments = Appiontment.objects.all().count()
    total_patients = User.objects.filter(is_superuser=False, is_staff=False).count()
    total_doctors = Doctor.objects.all().count()
    cancelled_appointments = Appiontment.objects.filter(status='Cancelled').count()
    scheduled_appointments = Appiontment.objects.filter(status='Scheduled').count()
    complete_appointments = Appiontment.objects.filter(status='Complete').count()



    context={'appointments': appointments,
             'total_appointments': total_appointments,
             'total_patients': total_patients,
             'total_doctors': total_doctors,
             'cancelled_appointments': cancelled_appointments,
             'scheduled_appointments': scheduled_appointments,
             'complete_appointments': complete_appointments,
             }

    return render(request, "users/admin_dashboard.html", context=context)

@user_passes_test(admin_check)
def admin_appointments(request):

    appointments = Appiontment.objects.all()

    context = {'appointments':appointments}

    return render(request, "users/admin_appointments.html", context=context)

@user_passes_test(admin_check)
def admin_doctors(request):

    doctors = Doctor.objects.all()

    context = {'doctors':doctors}

    return render(request, "users/admin_doctors.html", context=context)












