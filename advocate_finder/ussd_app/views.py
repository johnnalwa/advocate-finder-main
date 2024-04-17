from django.contrib import messages

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
from django.shortcuts import render, redirect
import base64
import json
from datetime import datetime
import africastalking
from .models import CaseType, UserSession, Advocate, Appointment
import logging
import requests

logging.basicConfig(level=logging.ERROR)

# Set up Africa's Talking credentials
africastalking_username = "devjnalwa"
africastalking_api_key = "64cf4b4482f4826835ab57e9dfe25102bcfe95c3efc5150d4ce49ac7ace1eab0"

# Initialize Africa's Talking SMS
africastalking.initialize(africastalking_username, africastalking_api_key)
sms = africastalking.SMS

class Appointment:
    def __init__(self, client, advocate, appointment_date):
        self.client = client
        self.advocate = advocate
        self.appointment_date = appointment_date

class Payment:
    def __init__(self, appointment, amount):
        self.appointment = appointment
        self.amount = amount

def send_sms(phone_number, message):
    # Ensure phone number is in the correct format for Africa's Talking
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    
    try:
        response = sms.send(message, [phone_number])
        if response['SMSMessageData']['Recipients'][0]['status'] == 'Success':
            return 'SMS sent successfully.'
        else:
            return f'Failed to send SMS. Status: {response["SMSMessageData"]["Recipients"][0]["status"]}'
    except Exception as e:
        # Log the error
        logging.error(f"Error sending SMS: {e}")
        return f'Error: {str(e)}'

def send_stk_push(phone_number, amount):
    # Remove "+" sign from the phone number if present
    phone_number = phone_number.replace('+', '')
    
    # Format phone number to include country code (254) and remove leading zeros
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif not phone_number.startswith('254'):
        phone_number = '254' + phone_number
    
    # M-PESA Credentials
    consumerKey = '4C3mkwwnUaq8AsSZ6ig0lGzEVrfNuLO9'
    consumerSecret = 'T9vB9MUhf8hRKocz'
    BusinessShortCode = '174379'
    Passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    
    Timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    Password = base64.b64encode((BusinessShortCode + Passkey + Timestamp).encode()).decode('utf-8')
    
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(access_token_url, auth=(consumerKey, consumerSecret))
    
    try:
        response_data = response.json()  # Parse JSON response
        if not response_data:  # If response_data is empty
            response_data = {"errorMessage": "Empty response from API"}
    except json.decoder.JSONDecodeError:
        response_data = {"errorMessage": "Invalid JSON response from API"}

    access_token = response_data.get("access_token")

    initiate_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    CallBackURL = 'https://7dab-102-140-203-238.ngrok-free.app'

    payload = {
        'BusinessShortCode': BusinessShortCode,
        'Password': Password,
        'Timestamp': Timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': BusinessShortCode,
        'PhoneNumber': phone_number,
        'CallBackURL': CallBackURL,
        'AccountReference': 'Donation Platform',
        'TransactionDesc': 'charity {}',
    }

    response = requests.post(initiate_url, headers=headers, json=payload)
        
    try:
        response_data = response.json()  # Parse JSON response
        if not response_data:  # If response_data is empty
            response_data = {"errorMessage": "Empty response from API"}
    except json.decoder.JSONDecodeError:
        response_data = {"errorMessage": "Invalid JSON response from API"}

    if response.status_code == 200:
        # Check if the API response indicates success
        if response_data.get('errorCode') == '0':
            success_message = response_data.get('ResponseDescription', 'Donation has been initiated successfully.')
            # After sending STK Push, send an SMS
            sms_message_stk_push = f"Thanks! Your donation of {amount} KES has been received."
            sms_result_stk_push = send_sms(phone_number, sms_message_stk_push)
            # Additional message
            additional_message = "Thank you."
            sms_result_additional = send_sms(phone_number, additional_message)
            return success_message
        else:
            # Log the error
            logging.error(f"Failed to initiate STK push. Error: {response_data}")
            # Handle API error
            error_message = response_data.get('errorMessage', 'Failed to initiate payment.')
            # Include phone number in error message
            error_message_with_phone = f'{error_message} Phone Number: {phone_number}'
            return error_message_with_phone
    else:
        # Log the error
        logging.error(f"HTTP Error: {response.status_code}")
        # Handle HTTP error
        error_message = f'HTTP Error: {response.status_code}'
        # Include phone number in error message
        error_message_with_phone = f'{error_message} Phone Number: {phone_number}'
        return error_message_with_phone

@csrf_exempt
def ussd_handler(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId', None)
        phone_number = request.POST.get('phoneNumber', None)
        text = request.POST.get('text', '')

        try:
            session, created = UserSession.objects.get_or_create(session_id=session_id, defaults={
                'phone_number': phone_number, 'stage': "register_name"
            })
        except UserSession.DoesNotExist:
            session = UserSession.objects.create(session_id=session_id, phone_number=phone_number, stage="register_name")

        text_array = text.split('*')
        user_response = text_array[-1]

        try:
            if session.stage == "register_name":
                if not text.strip():
                    session.stage = "register_name"
                    session.save()
                    response = "CON Welcome to Advocate Finder. Enter your full name to register:"
                else:
                    session.name = user_response
                    session.stage = "register_location"
                    session.save()
                    response = "CON Enter your location (e.g., Nairobi, Mombasa):"

            elif session.stage == "register_location":
                if text.strip():
                    session.location = user_response
                    session.stage = "select_case_type"
                    session.save()
                    response = "CON Select the type of case:\n1. Civil Litigation\n2.Criminal Defense\n3. Corporate Law\n4. Real Estate Law\n5. Employment Law\n6. Family Law\n7. Estate Planning and Probate\n8. Intellectual Property Law\n9. Immigration Law\n10. Bankruptcy Law"
                else:
                    response = "END Please enter your location."

            elif session.stage == "select_case_type":
                valid_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
                if user_response in valid_options:
                    case_types = [
                        "Civil Litigation", "Criminal Defense", "Corporate Law", "Real Estate Law",
                        "Employment Law", "Family Law", "Estate Planning and Probate",
                        "Intellectual Property Law", "Immigration Law", "Bankruptcy Law"
                    ]
                    session.case_type = case_types[int(user_response) - 1]
                    session.stage = "search_advocates"
                    session.save()
                    advocates = Advocate.objects.filter(location=session.location, case_types__name=session.case_type)
                    if advocates:
                        response = "CON Select an advocate to view profile:\n" + "\n".join([f"{i+1}. {advocate.name}" for i, advocate in enumerate(advocates)])
                    else:
                        response = "END No advocates found for the specified location and case type. Please try again."
                else:
                    response = "END Invalid option. Please try again."

            elif session.stage == "search_advocates":
                try:
                    advocate_index = int(user_response) - 1
                    advocates = Advocate.objects.filter(location=session.location, case_types__name=session.case_type)
                    if advocate_index >= 0 and advocate_index < len(advocates):
                        advocate = advocates[advocate_index]
                        session.selected_advocate = advocate.id
                        session.stage = "make_appointment"
                        session.save()
                        response = f"CON {advocate.name}\n{advocate.description}\nRate: {advocate.rate}\n\nEnter '1' to make an appointment or '2' to search again:"
                    else:
                        response = "END Invalid option. Please select a valid advocate."
                except ValueError:
                    response = "END Invalid option. Please enter a valid number."

            elif session.stage == "make_appointment":
                if user_response == "1":
                    session.stage = "appointment_details"
                    session.save()
                    response = "CON Enter the appointment date (YYYY-MM-DD):"
                elif user_response == "2":
                    session.stage = "select_case_type"
                    session.save()
                    response = "CON Select the type of case:"
                else:
                    response = "END Invalid option. Please try again."

            elif session.stage == "appointment_details":
                try:
                    appointment_date = datetime.strptime(user_response, "%Y-%m-%d").date()
                    advocate = Advocate.objects.get(id=session.selected_advocate)
                    appointment = Appointment.objects.create(
                        phone_number=session.phone_number,
                        full_name=session.name,
                        advocate_name=advocate.name,
                        advocate_description=advocate.description,
                        advocate_location=advocate.location,
                        advocate_case_types=",".join([case_type.name for case_type in advocate.case_types.all()]),
                        advocate_rate=advocate.rate,
                        case_type=session.case_type,
                        appointment_date=appointment_date
                    )
                    session.stage = "payment"
                    session.save()
                    response = f"CON Appointment created with {advocate.name} on {appointment_date}.\nEnter the payment amount:"
                except ValueError:
                    response = "END Invalid date format. Please enter the date in YYYY-MM-DD format."

            elif session.stage == "payment":
                try:
                    payment_amount = int(user_response)
                    appointment = Appointment.objects.get(phone_number=session.phone_number, appointment_date=appointment_date)
                    payment = Payment.objects.create(
                        appointment=appointment,
                        amount=payment_amount
                    )
                    # Call the send_stk_push function to initiate payment
                    send_stk_push(session.phone_number, payment_amount)
                    response = "END Payment initiated successfully. You will receive a prompt shortly."
                except ValueError:
                    response = "END Invalid amount. Please enter a valid numeric amount."

            else:
                response = "END An error occurred. Please try again."

        except Exception as e:
            logging.error("An error occurred: %s", e)
            response = "END An unexpected error occurred. Please try again later."

        return HttpResponse(response, content_type="text/plain")
    else:
        return HttpResponse("Method Not Allowed", status=405)


def search_advocates(location, case_type_name):
    try:
        case_type = CaseType.objects.get(name=case_type_name)
        matching_advocates = Advocate.objects.filter(location=location, case_types=case_type)
        return matching_advocates
    except CaseType.DoesNotExist:
        return []
   
 


def add_lawyer(request):
    case_types = CaseType.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        description = request.POST.get('description')
        location = request.POST.get('location')
        rate = request.POST.get('rate')
        case_type_ids = request.POST.getlist('case_types')

        lawyer = Advocate.objects.create(
            name=name,
            phone_number=phone_number,
            description=description,
            location=location,
            rate=rate
        )

        case_types = CaseType.objects.filter(id__in=case_type_ids)
        lawyer.case_types.set(case_types)

        # Set success message
        messages.success(request, 'Lawyer added successfully!')
        return render(request, 'advocates/add_lawyer.html', {'case_types': case_types})

    return render(request, 'advocates/add_lawyer.html', {'case_types': case_types})