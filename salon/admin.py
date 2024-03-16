from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Salon, Stylist, Appointment, CustomUser

admin.site.register(Salon)
admin.site.register(CustomUser)
admin.site.unregister(Group)
admin.site.site_header = "Salon management - Administration"
admin.site.site_index_title = 'Welcome to salon management Admin Portal'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('stylist', 'client_username', 'appointment_date')  # Specify the fields to display in the list view
    list_filter = ('stylist', 'client_username', 'appointment_date')  # Add filters
    search_fields = ('stylist__name', 'client_username__username', 'appointment_date__icontains') # Add search functionality

admin.site.register(Appointment, AppointmentAdmin)

class StylistAdmin(admin.ModelAdmin):
    list_display = ('salon', 'name', 'specialty', 'price')  # Specify the fields to display in the list view
    list_filter = ('salon', 'name', 'specialty', 'price')
    search_fields = ('salon__name', 'name', 'specialty', 'price')

admin.site.register(Stylist, StylistAdmin)
