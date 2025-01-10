from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.register_user, name="register"),
    path('edit_profile/', views.edit_user, name="edit_profile"),
    path('profile/', views.view_profile, name="profile"),
    path('doctors/<str:speciality>/', views.all_doctors, name='all_doctors'),
    path('appointment/<slug:slug>/',views.book_appointment, name="book_appointment"),
    path('my_appointments/', views.my_appointments, name="appointments"),
    path('cancel/<int:id>', views.cancel_appointment, name="cancel"),
    path('complete/<int:id>', views.complete_appointment, name="complete"),
    path('logout/', views.user_logout, name="logout"),
    path('doctor_login/', views.doctor_login, name="doctor_login"),
    path('doctor_logout/', views.doctor_logout, name="doctor_logout"),
    path('doctor_dashboard/', views.doctor_dashboard, name="doctor_dashboard"),
    path('doctor_appointments/', views.doctor_appointments, name="doctor_appointments"),
    path('about/', views.about_us, name="about"),
    path('contact/', views.contact_us, name="contact"),
    path('admin/login/', views.admin_login, name="admin_login"),
    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin/add_doctor/', views.add_doctor, name="add_doctor"),
    path('admin/all_appointments/', views.admin_appointments, name="admin_appointments"),
    path('admin/all_doctors/', views.admin_doctors, name="admin_doctors"),
]
