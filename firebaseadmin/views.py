from django.http import JsonResponse
from django.shortcuts import render, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import firebase_admin
from firebase_admin import credentials, firestore, auth
from .forms import CreateAccountForm, AddVehicleForm, ChangeSubscriptionForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import pytz

from .models import Subscription, Account

# Create your views here.
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "C:\\My Data\\my freelance\\mge\\myvltsproject-beb380465d07.json", scope)
client = gspread.authorize(creds)
sheet = client.open("VLTS APP SUBSCRITION").worksheet("GRL")

cred = credentials.Certificate("C:\\My Data\\GPS\\app\\myvltsproject-firebase-adminsdk-93q2h-1d45d70c31.json")
default = firebase_admin.initialize_app(cred)
db = firestore.client()

india_tz = pytz.timezone('Asia/Kolkata')


def create_new_user(email, password, display_name=None, phone_number=None):
    try:
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
            phone_number=phone_number
        )

        return user_record.uid
    except:
        return None


def add_user_to_user(uid, name, mobile):
    doc_ref = db.collection("users").document(uid)
    data = {
        "name": name,
        "mobile": mobile
    }
    doc_ref.set(data)


def add_vehicle_to_user(uid, Vehicle, VendorId, IMEI, Longitude, Latitude):
    doc_ref = db.collection("users").document(uid).collection("Vehicles").document(Vehicle)
    data = {
        "VendorId": VendorId,
        "IMEI": IMEI,
        "Longitude": Longitude,
        "Latitude": Latitude
    }
    doc_ref.set(data)


def add_user_to_subscription(uid, vehicle, subscription):
    doc_ref = db.collection("subscription").document(uid)
    data = {
        vehicle: subscription,
    }
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update(data)
    else:
        doc_ref.set(data)


def add_vehicle_to_history(vehicle):
    doc_ref = db.collection("history").document(vehicle)
    data = {}
    doc_ref.set(data)


def get_uid_by_email(email):
    user_record = auth.get_user_by_email(email)
    uid = user_record.uid
    return uid


def home(request):
    return render(request, 'firebaseadmin\home.html')


@login_required
def create_account(request):
    if request.method == 'POST':
        current_date_india = datetime.now(india_tz)
        form = CreateAccountForm(request.POST)
        result = {}
        if form.is_valid():
            # Handle the form data here
            # For example, you can save it to the database or perform other actions
            name = form.cleaned_data['name']
            mobile_no = form.cleaned_data['mobile_no']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            vehicle_number = form.cleaned_data['vehicle_number']
            imei = form.cleaned_data['imei']
            subscription = form.cleaned_data['subscription']
            if subscription == '2_days':
                after_days = current_date_india + timedelta(days=2)
            elif subscription == '3_Days':
                after_days = current_date_india + timedelta(days=3)
            elif subscription == '10_Days':
                after_days = current_date_india + timedelta(days=10)
            else:
                after_days = current_date_india + timedelta(days=31)

            subscription_end_date = after_days.strftime('%d-%m-%Y')

            uid = create_new_user(email, password, display_name=None, phone_number=None)
            if uid != None:

                try:
                    add_user_to_user(uid, name, mobile_no)
                    add_vehicle_to_user(uid, vehicle_number, "GRL", imei, 0, 0)
                    add_user_to_subscription(uid, vehicle_number, subscription_end_date)
                    add_vehicle_to_history(vehicle_number)
                    row_data = [name, mobile_no, vehicle_number, "GRL", imei, 0, 0, email, password, uid,
                                subscription_end_date]
                    sheet.append_row(row_data)

                    result = {
                        'form': CreateAccountForm(),
                        'res': True,
                        'error': False,
                        'email': email,
                        'password': password,
                        'subscription': subscription_end_date}

                    account = Account.objects.create(
                        email=email,
                        password=password
                    )

                    # Save to Subscription model
                    Subscription.objects.create(
                        account=account,
                        vehicle=vehicle_number,
                        subscription=subscription
                    )

                except Exception as e:

                    result = {
                        'form': form,
                        'submitted': True,
                        'error': True,
                        'errorText': f"{e}",
                    }
            else:

                result = {
                    'form': form,
                    'submitted': True,
                    'error': True,
                    'errorText': "email already in use",
                    }

            return render(request, 'firebaseadmin\\create_account.html', result)
    else:
        form = CreateAccountForm()

    return render(request, 'firebaseadmin\\create_account.html', {'form': form})


@login_required
def add_vehicle(request):
    if request.method == 'POST':
        current_date_india = datetime.now(india_tz)
        form = AddVehicleForm(request.POST)
        if form.is_valid():

            email = str(form.cleaned_data['email'])
            vehicle_number = form.cleaned_data['vehicle_number']
            imei = form.cleaned_data['imei']
            subscription = form.cleaned_data['subscription']
            if subscription == '2_days':
                after_days = current_date_india + timedelta(days=2)
            elif subscription == '3_Days':
                after_days = current_date_india + timedelta(days=3)
            elif subscription == '10_Days':
                after_days = current_date_india + timedelta(days=10)
            else:
                after_days = current_date_india + timedelta(days=31)

            subscription_end_date = after_days.strftime('%d-%m-%Y')
            try:
                try:
                    uid = get_uid_by_email(email)
                except Exception as e:
                    print(e)
                print(type(uid))

                add_vehicle_to_user(uid, vehicle_number, "GRL", imei, 0, 0)
                add_user_to_subscription(uid, vehicle_number, subscription_end_date)
                add_vehicle_to_history(vehicle_number)
                row_data = ["", "", vehicle_number, "GRL", imei, 0, 0, email, "", uid,
                            subscription_end_date]
                sheet.append_row(row_data)

                account = Account.objects.get(email=email)

                # Create the Subscription linked to the existing Account
                Subscription.objects.create(
                    account=account,
                    vehicle=vehicle_number,
                    subscription=subscription_end_date
                )

                result = {
                    'form': CreateAccountForm(),
                    'res': True,
                    'error': False,
                    'email': email,
                    'vehicle_number': vehicle_number,
                    'subscription': subscription_end_date}

            except Exception as e:
                result = {
                    'form': form,
                    'submitted': True,
                    'error': True,
                    'errorText': f"{e}",
                }

            # Handle form data
            return render(request, 'firebaseadmin\\add_vehicle.html', result)
    else:
        form = AddVehicleForm()

    return render(request, 'firebaseadmin\\add_vehicle.html', {'form': form})


@login_required
def change_subscription(request):
    if request.method == 'POST':
        form = ChangeSubscriptionForm(request.POST)
        if form.is_valid():
            # Handle form data
            return redirect('home')
    else:
        form = ChangeSubscriptionForm()

    return render(request, 'firebaseadmin\\change_subscription.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            # Handle form data
            return redirect('home')
    else:
        form = ChangePasswordForm()

    return render(request, 'firebaseadmin\\change_password.html', {'form': form})


def get_vehicles(request):
    email = request.GET.get('email')
    vehicles = Subscription.objects.filter(account__email=email).values_list('vehicle', flat=True)
    for v in vehicles:
        print(v)
    return JsonResponse({'vehicles': list(vehicles)})
