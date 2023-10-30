from django.urls import path

from users import views

urlpatterns = [
    path('', views.home_page_view, name='home'),

    # General application information
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),
]
