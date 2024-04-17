
from ussd_app import views as ussd_views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.login, name="login"),
    path('login/', views.LoginView.as_view(), name="user_login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    
    path('clients/dashboard/',views.ClientsDashboard, name="clients_dashboard"),
    path('clients/register/',views.RegisterClientView.as_view(), name="register_clients"),
    path('advocate-profiles/', views.advocate_profile, name='advocate_profiles'),
    path('book_appointment/<int:advocate_id>/', views.book_appointment_view, name='book_appointment'),
    path('book_appointment/<int:advocate_id>/', views.book_appointment_view, name='book_appointment'),


    path('add-lawyer/', ussd_views.add_lawyer, name='add_lawyer'),  # Importing from ussd_app.views

    
    path('advocates/dashboard/',views.AdvocatesDashboard, name="advocates_dashboard"),
    path('adcocates/register/',views.RegisterAdvocatesView.as_view(), name="register_advocates"),
    path('profile/', views.create_lawyer_profile, name='create_lawyer_profile'),
    path('advocate-form/', views.advocate_form, name='advocate_form'),
    path('advocate-edit/', views.advocate_form, name='advocate_edit'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile-updated/', views.profile_updated, name='profile_updated'),
    path('create_case/', views.create_case, name='create_case'),
     




    

 ]
