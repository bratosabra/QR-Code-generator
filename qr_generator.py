import tkinter as tk
from tkinter import messagebox
import qrcode
import vobject

def generate_qr_code():
    # Получаем данные из полей ввода
    employee_name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    street = street_entry.get().strip()
    city = city_entry.get().strip()
    region = region_entry.get().strip()
    code = postal_code_entry.get().strip()
    country = country_entry.get().strip()
    title = title_entry.get().strip()
    url = url_entry.get().strip()
    note = note_entry.get().strip()

    # Проверка на пустые поля
    if not employee_name or not phone or not email:
        messagebox.showerror("Ошибка", "Пожалуйста, заполните обязательные поля (ФИО, телефон, email).")
        return

    # Создаем vCard для сотрудника
    vcard = vobject.vCard()
    vcard.add('fn').value = employee_name
    vcard.add('tel').value = phone
    vcard.tel.type_param = 'CELL'
    vcard.add('email').value = email

    # Корректная структура для адреса
    adr = vcard.add('adr')
    adr.value = vobject.vcard.Address(street=street, city=city, region=region, code=code, country=country)

    # Дополнительные поля
    vcard.add('title').value = title
    vcard.add('url').value = url
    vcard.add('note').value = note

    # Конвертация vCard в строку
    vcard_data = vcard.serialize()

    # Генерация QR-кода
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L if error_correction_var.get() == 'L' else
                         qrcode.constants.ERROR_CORRECT_M if error_correction_var.get() == 'M' else
                         qrcode.constants.ERROR_CORRECT_Q if error_correction_var.get() == 'Q' else
                         qrcode.constants.ERROR_CORRECT_H,
        box_size=size_var.get(),
        border=4,
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)

    # Создание и сохранение изображения QR-кода
    img = qr.make_image(fill_color="black", back_color="white")

    # Формируем имя файла на основе имени сотрудника и формата
    file_name = f"{employee_name.replace(' ', '_')}.{format_var.get().lower()}"
    img.save(file_name, format=format_var.get())

    # Уведомление о сохранении
    messagebox.showinfo("Успех", f"QR-код сохранен как {file_name}")

    # Отображение превью QR-кода
    img.thumbnail((100, 100))  # Измените размер для превью
    img_preview = tk.PhotoImage(img)  # Это может потребовать конвертации
    qr_preview.config(image=img_preview)
    qr_preview.image = img_preview  # Сохраните ссылку на изображение

# Создание основного окна
root = tk.Tk()
root.title("Генератор QR-кода")

# Создание полей ввода
tk.Label(root, text="ФИО:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Телефон:").grid(row=1, column=0)
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

tk.Label(root, text="Улица:").grid(row=3, column=0)
street_entry = tk.Entry(root)
street_entry.grid(row=3, column=1)

tk.Label(root, text="Город:").grid(row=4, column=0)
city_entry = tk.Entry(root)
city_entry.grid(row=4, column=1)

tk.Label(root, text="Регион:").grid(row=5, column=0)
region_entry = tk.Entry(root)
region_entry.grid(row=5, column=1)

tk.Label(root, text="Почтовый код:").grid(row=6, column=0)
postal_code_entry = tk.Entry(root)
postal_code_entry.grid(row=6, column=1)

tk.Label(root, text="Страна:").grid(row=7, column=0)
country_entry = tk.Entry(root)
country_entry.grid(row=7, column=1)

tk.Label(root, text="Должность:").grid(row=8, column=0)
title_entry = tk.Entry(root)
title_entry.grid(row=8, column=1)

tk.Label(root, text="Ссылка:").grid(row=9, column=0)
url_entry = tk.Entry(root)
url_entry.grid(row=9, column=1)

tk.Label(root, text="Примечание:").grid(row=10, column=0)
note_entry = tk.Entry(root)
note_entry.grid(row=10, column=1)

# Добавляем выбор формата изображения
tk.Label(root, text="Формат изображения:").grid(row=12, column=0)
format_var = tk.StringVar(value='PNG')
format_menu = tk.OptionMenu(root, format_var, 'PNG', 'JPEG')
format_menu.grid(row=12, column=1)

# Добавляем размер QR-кода
tk.Label(root, text="Размер QR-кода:").grid(row=14, column=0)
size_var = tk.IntVar(value=10)  # По умолчанию размер 10
size_entry = tk.Entry(root, textvariable=size_var)
size_entry.grid(row=14, column=1)

# Создание элемента для отображения QR-кода
qr_preview = tk.Label(root)
qr_preview.grid(row=15, columnspan=2)

# Кнопка для генерации QR-кода
generate_button = tk.Button(root, text="Сгенерировать QR-код", command=generate_qr_code)
generate_button.grid(row=11, columnspan=2)

# Запуск основного цикла приложения
root.mainloop()
