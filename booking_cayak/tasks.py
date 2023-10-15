from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from background_task import background


@background(schedule=28800, repeat=False)  # Запускати один раз о 8:00 кожного 20 числа місяця
def generate_monthly_spreadsheet():

    # Підключення до Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
    gc = gspread.authorize(credentials)

    # Отримуємо сьогоднішню дату та дату наступного місяця
    today = datetime.today()
    next_month = today.replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)

    # Отримуємо ім'я місяця
    month_name = next_month.strftime("%B")

    # Створюємо книгу та додаткові аркуші для кожного дня місяця
    workbook = gc.create(f"Книга на {month_name}")

    while next_month.month == today.month:
        # Отримуємо ім'я дня тижня та формуємо ім'я аркуша
        day_name = next_month.strftime("%a")
        sheet_name = next_month.strftime("%d-%m-%y") + "_" + day_name

        # Копіюємо шаблонний аркуш у новий згенерований аркуш
        template_sheet = workbook.worksheet("Шаблон")
        new_sheet = template_sheet.duplicate(new_sheet_name=sheet_name)

        # Переходимо до наступного дня
        next_month += timedelta(days=1)

    # Видаляємо шаблонний аркуш
    workbook.del_worksheet(template_sheet)

    print(f"Книга на {month_name} створена успішно!")
    return workbook

