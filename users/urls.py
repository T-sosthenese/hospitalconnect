from django.urls import path

from users import views


urlpatterns = [
    path('', views.home_page_view, name='home'),

    # General application information
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus/', views.contactus_view, name='contactus'),
    path('logout/', views.logout_view, name='logout'),
    # Admin-related views
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('adminsignup/', views.admin_signup_view, name='adminsignup'),
    path("adminlogin/", views.admin_login_view, name='adminlogin'),
    path('admin-dashboard/', views.admin_dashboard_view,name='admin-dashboard'),

    # Doctor-related views
    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('doctorsignup/', views.doctor_signup_view,name='doctorsignup'),
    path('doctorlogin/', views.doctorlogin_view, name='doctorlogin'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'),
]