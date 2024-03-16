from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', UserLogout, name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('salon/', SalonView.as_view(), name='salon'),
    path('salon-view/', StylistView.as_view(), name='salon-view'),
    path('stylists/<int:salon_id>', StylistView.as_view(), name='stylist'),
    path('appointment/<int:pk>', Appointmentview.as_view(), name='appointment'),
    path('details/', PersonalDetails.as_view(), name='details'),
    path('update/', EditDetails.as_view(), name='update'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('my_appointments/', Myappointments.as_view(), name='my_appointments'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('password-reset/', password_reset_view, name='password-reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done' ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)