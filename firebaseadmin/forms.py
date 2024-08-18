from django import forms
from django import template

from firebaseadmin.models import Account

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={"class": css_class})

class CreateAccountForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_no = forms.CharField(max_length=15, required=True, label="Mobile No",widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, required=True, label="Email",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label="New Password")
    vehicle_number = forms.CharField(max_length=20, required=True, label="Vehicle Number",
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    imei = forms.CharField(max_length=20, required=True, label="IMEI",
                           widget=forms.NumberInput(attrs={'class': 'form-control'}))

    SUBSCRIPTION_CHOICES = [
        ('2_days', '2 Days'),
        ('3_days', '3 Days'),
        ('10_days', '10 Days'),
        ('1_month', '1 Month')
    ]
    subscription = forms.ChoiceField(choices=SUBSCRIPTION_CHOICES, required=True, label="Subscription",
                                     widget=forms.Select(attrs={'class': 'form-control'}))


class AddVehicleForm(forms.Form):

    email = forms.ModelChoiceField(required=True,
                                   queryset=Account.objects.all(),
                                   empty_label="Select Email",
                                   to_field_name="email",
                                   label="Email",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    vehicle_number = forms.CharField(max_length=20, required=True, label="Vehicle Number",
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    imei = forms.CharField(max_length=20, required=True, label="IMEI",
                           widget=forms.NumberInput(attrs={'class': 'form-control'}))

    SUBSCRIPTION_CHOICES = [
        ('2_days', '2 Days'),
        ('3_days', '3 Days'),
        ('10_days', '10 Days'),
        ('1_month', '1 Month')
    ]
    subscription = forms.ChoiceField(choices=SUBSCRIPTION_CHOICES, required=True, label="Subscription",
                                     widget=forms.Select(attrs={'class': 'form-control'}))


class ChangeSubscriptionForm(forms.Form):
    email = forms.ModelChoiceField(required=True,
                                   queryset=Account.objects.all(),
                                   empty_label="Select Email",
                                   to_field_name="email",
                                   label="Email",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    vehicle_number = forms.ChoiceField(choices=[], required=True, label="Vehicle",
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    SUBSCRIPTION_CHOICES = [
        ('2_days', '2 Days'),
        ('10_days', '10 Days'),
        ('1_month', '1 Month'),
        ('end_subscription', 'End Subscription')
    ]
    subscription = forms.ChoiceField(choices=SUBSCRIPTION_CHOICES, required=True, label="Subscription",
                                     widget=forms.Select(attrs={'class': 'form-control'}))




class ChangePasswordForm(forms.Form):
    email = forms.ModelChoiceField(required=True,
                                   queryset=Account.objects.all(),
                                   empty_label="Select Email",
                                   to_field_name="email",
                                   label="Email",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, label="New Password")
