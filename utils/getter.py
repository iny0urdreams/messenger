from datetime import datetime
import requests
import time

last_timestamp = 0.0

while True:
    response = requests.get(
        'http://127.0.0.1:5000/get_messages',
        params={'after': last_timestamp}
    )
    messages = response.json()['messages']

    for message in messages:
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%H:%M:%S')
        print(f'{dt} {message["username"]}:')
        print(message['text'], '\n')
        last_timestamp = message['timestamp']
    time.sleep(1)
