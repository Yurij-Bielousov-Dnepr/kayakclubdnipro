# views.py
from datetime import datetime
import gspread
from django.shortcuts import render, redirect
from django.template import response
from .models import Boat, Booking, Price
from django.shortcuts import render
from .constants import BOAT_TYPES, HOURS
from django.conf import settings
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from .utils import get_google_sheets_credentials
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def update_cell(spreadsheet_id, range_name, new_value, comment):
    # Отримуємо об'єкт авторизації Google Sheets API
    credentials = Credentials.from_authorized_user_file('path/to/credentials.json')

    # Створюємо об'єкт Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)

    # Оновлюємо вміст комірки та додаємо коментар
    body = {
        'values': [[new_value]],
        'comments': comment
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()

    return result

def read_google_sheets(request):
    # Отримуємо об'єкт авторизації Google Sheets API
    credentials = get_google_sheets_credentials()

    # Створюємо об'єкт Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)

    # Тепер можемо використовувати об'єкт service для роботи з Google Sheets API
    # Наприклад, можемо отримати дані з таблиці
    spreadsheet_id = 'your_spreadsheet_id'
    range_name = 'Sheet1!A1:B2'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()

    data = result.get('values', [])

    # Передаємо дані у шаблон HTML та повертаємо його у відповідь
    return render(request, 'crm.html', {'data': data, 'hours': HOURS})

def get_google_sheets_credentials():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SHEETS_CONFIG_FILE, scopes=scope
    )
    # Авторизуйтесь у Google Таблицях API / чи треба це?
    client = gspread.authorize(credentials)
    return credentials



def statistics_view(request):
    # Отримайте потрібні дані для статистики з вашої моделі Booking
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(Sum('total_price'))['total_price__sum']
    # Додайте додаткові розрахунки та аналіз даних залежно від вашого бізнесу

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        # Додайте інші дані для відображення на сторінці статистики
    }

    return render(request, 'admin/booking_cayak/statistics.html', context)


def assortment_view(request):
    context = {
        'boat_types': BOAT_TYPES
    }
    return render(request, 'assortment_2.html', context)


def index_view(request):
    return render(request, 'Index.html')


def price_view(request):
    return render(request, 'price.html')


def routes_view(request):
    return render(request, 'routes.html')


def booking_crm(request):
    prices = Price.objects.all()
    context = {
        'prices': prices
    }
    return render(request, 'booking_cayak/crm.html', context)


def booking(request):
    if request.method == 'POST':
        boat_id = request.POST.get('boat')
        start_date = request.POST.get('start_date')
        duration = request.POST.get('duration')

        # Получить выбранную лодку
        boat = Boat.objects.get(id=boat_id)

        # Рассчитать цену на основе продолжительности проката
        price_per_hour = Price.objects.get(boat=boat).price
        price = price_per_hour * int(duration)

        # Создать объект бронирования и сохранить его в базе данных
        booking = Booking(boat=boat, start_date=start_date, duration=duration, price=price)
        booking.save()

        return redirect('booking_success')
    else:
        # Получить список доступных лодок
        boats = Boat.objects.all()

        return render(request, 'booking_cayak/booking.html', {'boats': boats})


def booking_success(request):
    return render(request, 'booking_cayak/booking_success.html')
