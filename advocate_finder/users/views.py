from django.http import HttpResponseNotFound, JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import *
from django.contrib import messages
from .utils import get_logged_in_users
from django.urls import reverse_lazy
from ussd_app.views import add_lawyer as ussd_add_lawyer  # Import the view function from ussd_app module



def login(request):
    form = LoginForm
    context = {
        'form': form
    }
    return render(request, 'login.html', context)

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')  # Display login error message
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            users_info = get_logged_in_users()
            self.request.session['logged_in_users'] = users_info  # Store info in session

            if user.is_client:
                messages.success(self.request, 'Welcome to the clients dashboard.')
                return reverse('clients_dashboard')
            elif user.is_advocate:
                messages.success(self.request, 'Welcome to the Advocate dashboard.')
                return reverse('advocates_dashboard')
        
        # Redirect unauthenticated users to the login page with an error message
        messages.error(self.request, 'You are not authenticated. Please log in.')
        return reverse('login')
        

class RegisterClientView(SuccessMessageMixin, CreateView):
    model = User
    form_class = MemberSignUpForm
    template_name = 'clients/register.html'
    success_url = reverse_lazy('login')  # Redirect to login on successful registration
    success_message = "Registration successful. You can now log in."

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please check your inputs.')  # Error message
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Additional logic if needed after successful registration
        return response

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)
  
    
class RegisterAdvocatesView(CreateView):
    model = User
    form_class = AdvocatesSignUpForm
    template_name = 'advocates/register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'advocate'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('login')
    


# @login_required
# @member_required
def ClientsDashboard(request):
    
    return render(request, 'clients/dashboard.html', {
        
    })
    


# @login_required
# @management_required
def AdvocatesDashboard(request):
    return render(request, 'Advocates/dashboard.html', {

    })



def create_lawyer_profile(request):
    if request.method == 'POST':
        form = LawyerProfileForm(request.POST)
        if form.is_valid():
            lawyer_profile = form.save(commit=False)
            lawyer_profile.user = request.user
            lawyer_profile.save()
            return render(request, 'advocates/success_profile_update.html')  # Render a success template
    else:
        form = LawyerProfileForm()
    return render(request, 'advocates/lawyer_profile_form.html', {'form': form})


def advocate_profile(request):
    advocates = Advocate.objects.all()
    return render(request, 'clients/advocate_profiles.html', {'advocates': advocates})



@login_required
def advocate_form(request):
    if request.method == 'POST':
        form = AdvocateForm(request.POST)
        if form.is_valid():
            advocate = form.save(commit=False)
            advocate.user = request.user
            advocate.save()
            return render(request, 'advocates/advocate_form.html', {'form': form, 'success_message': True})
        else:
            form = AdvocateForm()
            return render(request, 'advocates/advocate_form.html', {'form': form, 'errors': form.errors})
    else:
        form = AdvocateForm()
    return render(request, 'advocates/advocate_form.html', {'form': form})


@login_required
def book_appointment_view(request, advocate_id):
    try:
        advocate = get_object_or_404(Advocate, id=advocate_id)
    except Advocate.DoesNotExist:
        # Handle case where advocate does not exist
        return HttpResponseNotFound('<h1>Advocate not found</h1>')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.advocate = advocate
            appointment.save()
            # Redirect to a success page or a confirmation message
    else:
        form = AppointmentForm()
    return render(request, 'clients/appointment_booking.html', {'form': form, 'advocate': advocate})


@login_required
def update_profile(request):
    user = request.user
    try:
        lawyer_profile = LawyerProfile.objects.get(user=user)
    except LawyerProfile.DoesNotExist:
        # If LawyerProfile doesn't exist, create a new instance with minimal data
        lawyer_profile = LawyerProfile(user=user)
        lawyer_profile.save()

    if request.method == 'POST':
        form = LawyerProfileForm(request.POST, instance=lawyer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_updated')
    else:
        form = LawyerProfileForm(instance=lawyer_profile)
    
    return render(request, 'advocates/update_profile.html', {'form': form})

def profile_updated(request):
    return render(request, 'advocates/profile_updated.html')


def get_advocate_details(request, advocate_id):
    advocate = Advocate.objects.get(pk=advocate_id)
    return render(request, 'clients/advocate_details_modal.html', {'advocate': advocate})


@login_required
def create_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.lawyer = request.user  # Assign currently logged-in user to lawyer field
            case.save()
            return JsonResponse({'success': True, 'message': 'Case created successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CaseForm()
    return render(request, 'advocates/create_case.html', {'form': form})



def add_lawyer(request):
    # Delegate to the view function from ussd_app module
    return ussd_add_lawyer(request)