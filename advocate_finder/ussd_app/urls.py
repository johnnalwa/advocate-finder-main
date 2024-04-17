from django.urls import path

from . import views  # Correct import statement

urlpatterns = [
    path('ussdapp/', views.ussd_handler, name='ussd'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('add-lawyer/', views.add_lawyer, name='add_lawyer'),


]