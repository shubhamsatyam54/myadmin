from django.contrib import admin
from .models import Account, Subscription

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'password')  # Customize which fields are displayed in the list view
    search_fields = ('email',)            # Enable search functionality by email
    list_filter = ('email',)              # Add filtering options by email

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('account', 'vehicle', 'subscription')  # Customize which fields are displayed in the list view
    search_fields = ('account__email', 'vehicle')  # Enable search functionality by account email and vehicle
    list_filter = ('subscription',)               # Add filtering options by subscription type

# Register the models with the admin site
admin.site.register(Account, AccountAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
