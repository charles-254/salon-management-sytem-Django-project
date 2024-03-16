from django.shortcuts import render, redirect
from .models import Salon, Stylist, CustomUser, Appointment
from .forms import CustomUserCreationForm, SalonAppointmentForm, EditDetailsForm, PasswordResetForm
from django.views.generic import View, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.urls import reverse_lazy

class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm
        return render(request, 'signup.html', {'form':form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
        return render(request, 'signup.html', {'form':form})

class LoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('home')
        return super().form_valid(form)

def UserLogout(request):
    logout(request)
    return render(request, 'logout.html')

class HomeView(TemplateView):
    def get(self, request):
        salons = Salon.objects.all()
        stylists = Stylist.objects.all()
        return render(request, 'home.html',{"salons": salons, 'stylists': stylists},)

class SalonView(LoginRequiredMixin,View):
    def get(self, request):
        salons = Salon.objects.all().order_by('id')
        return render(request, 'salons.html',{"salons": salons})

class StylistView(LoginRequiredMixin, View):
    def get(self, request, salon_id):
        salon = get_object_or_404(Salon, id=salon_id)
        stylists = Stylist.objects.filter(salon=salon).order_by('id')
        return render(request, 'stylist_list.html', {"salon": salon, "stylists": stylists})

class Appointmentview(LoginRequiredMixin, View):
    def get(self, request, pk):
        stylist = Stylist.objects.get(pk=pk)
        username = CustomUser.objects.get(username=request.user.username)
        initial_data = {
            'stylist_name': stylist.name,
            'stylist_specialty': stylist.specialty,
            'price': stylist.price,
            'customuser_username': username
        }
        form = SalonAppointmentForm(initial_data)
        return render(request, 'make_appointment.html', {'form': form})

    def post(self, request, pk):
        if request.method == 'POST':
            form = SalonAppointmentForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['stylist_name']
                client_username = form.cleaned_data['customuser_username']
                appointment_date = form.cleaned_data['appointment_date_time']

                custom_user = CustomUser.objects.get(username=client_username)
                stylist_nm = Stylist.objects.get(name=name)

                appointment = Appointment(
                    stylist=stylist_nm,
                    client_username=custom_user,
                    appointment_date=appointment_date
                )
                appointment.save()

                return render(request, 'appointment_saved.html')

        return render(request, 'make_appointment.html', {'form': form})

class Myappointments(LoginRequiredMixin, View):
    def get(self, request):
        appointments = Appointment.objects.all().filter(client_username_id=request.user.id).order_by('-appointment_date')
        return render(request, 'my_appointments.html', {'appointments': appointments})



class PersonalDetails(LoginRequiredMixin, View):
    def get(self, request):
        details = CustomUser.objects.all().filter(id=request.user.id)
        return render(request, 'personal_details.html', {"details": details})

class EditDetails(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditDetailsForm
    template_name = 'edit_details.html'
    success_url = reverse_lazy('details')

    def get_object(self, queryset=None):
        # Return the object to edit based on the logged-in user
        return CustomUser.objects.get(username=self.request.user.username)

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('password_change_done')

class PasswordChangeDoneView(TemplateView):
    template_name = 'password_change_done.html'


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(email=email, username=username)
            return redirect('password-reset')
        except CustomUser.DoesNotExist:
            messages.error(request,  "User with this email and username does not exist.")
            return render(request, 'forgot_password.html', )
    return render(request, 'forgot_password.html')


def password_reset_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            user = request.user
            user.set_password(new_password)
            user.save()
            return redirect('password_reset_done')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'password_reset.html')

    else:
        return render(request, 'password_reset.html')

class PasswordResetDoneView(TemplateView):
    template_name = 'password_reset_done.html'