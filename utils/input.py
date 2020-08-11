import requests

username = input('Имя: ')
password = input('Пароль: ')

while True:
    text = input('Введите текст: ')

    requests.get(
        'http://127.0.0.1:5000/send_message',
        json={
            'username': username,
            'password': password,
            'text': text,
        }
    )