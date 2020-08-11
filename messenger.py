from _datetime import datetime
import requests
from server import User
from PyQt5 import QtWidgets, QtCore
import clientui


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.lineEdit.setHidden(True)
        self.lineEdit.setDisabled(True)
        self.lineEdit_2.setHidden(True)
        self.lineEdit_2.setDisabled(True)
        self.pushButton_4.setHidden(True)
        self.pushButton_4.setDisabled(True)
        self.pushButton_5.setHidden(True)
        self.pushButton_5.setDisabled(True)
        self.label_2.setHidden(True)
        self.textEdit.setDisabled(True)
        self.pushButton.setDisabled(True)
        self.listWidget.setDisabled(True)

        self.label.adjustSize()
        self.pushButton_2.adjustSize()
        self.pushButton_3.adjustSize()
        self.label_2.adjustSize()
        self.lineEdit.adjustSize()
        self.lineEdit_2.adjustSize()
        self.pushButton_4.adjustSize()
        # self.layOut_1.addStretch()

        # Отправка сообщения
        self.pushButton.pressed.connect(self.send_message)
        # Авторизация
        self.pushButton_2.pressed.connect(lambda: self.choice('autorisation'))
        # Регистрация
        self.pushButton_3.pressed.connect(lambda: self.choice('registration'))
        self.pushButton_5.pressed.connect(self.cancel)
        # Отправка логина и пароля
        self.pushButton_4.pressed.connect(self.log_in)

        self.listWidget.setCurrentRow(0)
        self.current_receiver = 'Общий чат'
        self.listWidget.itemPressed.connect(self.receiver_func)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.timeout.connect(self.update_contacts)
        self.timer.start(1000)  # Миллисекунды

        self.last_timestamp = 0

        self.users_count = len(User.query.all())
        self.mode = 'Общий чат'

    def receiver_func(self):
        self.current_receiver = self.listWidget.currentItem().text()
        self.textBrowser.setText('')
        self.last_timestamp = 0

    def update_contacts(self):
        if self.users_count < len(User.query.all()):
            self.listWidget.addItem(str(User.query.all()[-1]))
            self.users_count = len(User.query.all())

    def choice(self, choice_type):
        self.lineEdit.setHidden(False)
        self.lineEdit.setDisabled(False)
        self.lineEdit_2.setHidden(False)
        self.lineEdit_2.setDisabled(False)
        self.pushButton_4.setHidden(False)
        self.pushButton_4.setDisabled(False)
        self.pushButton_5.setHidden(False)
        self.pushButton_5.setDisabled(False)
        self.pushButton_3.setHidden(True)
        self.pushButton_3.setDisabled(True)
        self.pushButton_2.setHidden(True)
        self.pushButton_2.setDisabled(True)
        self.choice_type = choice_type

    def cancel(self):
        self.lineEdit.setHidden(True)
        self.lineEdit.setDisabled(True)
        self.lineEdit_2.setHidden(True)
        self.lineEdit_2.setDisabled(True)
        self.pushButton_4.setHidden(True)
        self.pushButton_4.setDisabled(True)
        self.pushButton_5.setHidden(True)
        self.pushButton_5.setDisabled(True)
        self.pushButton_3.setHidden(False)
        self.pushButton_3.setDisabled(False)
        self.pushButton_2.setHidden(False)
        self.pushButton_2.setDisabled(False)
        self.label_2.setHidden(True)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

    def log_in(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        choice = self.choice_type
        response = requests.get(
            'http://127.0.0.1:5000/log_in',
            json={
                'username': username,
                'password': password,
                'choice': choice
            }
        )

        response = response.json()

        if response['status'] == 'Все четко':
            self.lineEdit.setHidden(True)
            self.lineEdit_2.setHidden(True)
            self.pushButton_4.setHidden(True)
            self.pushButton_4.setDisabled(True)
            self.pushButton_5.setHidden(True)
            self.pushButton_5.setDisabled(True)
            self.label_2.setHidden(True)
            self.textBrowser.append(f'Добро пожаловать, {response["username"]}!\n')
            for user in User.query.all():
                if str(user) != self.lineEdit.text():
                    self.listWidget.addItem(str(user))
            self.textEdit.setDisabled(False)
            self.pushButton.setDisabled(False)
            self.listWidget.setDisabled(False)
        else:
            self.label_2.setText(response['status'])
            self.label_2.adjustSize()
            self.label_2.setHidden(False)

    def send_message(self):
        username = self.lineEdit.text()
        receiver = self.current_receiver
        text = self.textEdit.toPlainText()

        requests.get(
            'http://127.0.0.1:5000/send_message',
            json={
                'username': username,
                'receiver': receiver,
                'text': text,
            }
        )

        self.textEdit.setText('')  # Делаем поле ввода пустым, после отправки сообщения
        self.textEdit.repaint()  # Заново отрисовываем это поле, т.к. на маках бывает баг

    def update_messages(self):
        receiver = self.current_receiver
        response = requests.get(
            'http://127.0.0.1:5000/get_messages',
            params={'after': self.last_timestamp},
            json={
                'receiver': receiver
            }
        )
        messages = response.json()['messages']
        for message in messages:
            if 'receiver' not in message:
                # time_now = arrow.get(message['timestamp'])
                # time_now = time_now.format('(DD.MM.YY hh:mm:ss)')
                dt = datetime.fromtimestamp(message['timestamp'])
                dt = dt.strftime('(%d/%m/%y %H:%M:%S)')
                self.textBrowser.append(dt + ' ' + message["username"] + ':')
                self.textBrowser.append(message['text'] + '\n')
                self.last_timestamp = message['timestamp']
            else:
                if message['receiver'] == self.current_receiver and message['sender'] == self.lineEdit.text() \
                        or message['receiver'] == self.lineEdit.text() and message['sender'] == self.current_receiver:
                    # time_now = arrow.get(message['timestamp'])
                    # time_now = time_now.format('(DD.MM.YY hh:mm:ss)')
                    dt = datetime.fromtimestamp(message['timestamp'])
                    dt = dt.strftime('(%d/%m/%y %H:%M:%S)')
                    if message['sender'] == self.lineEdit.text():
                        self.textBrowser.append(dt + ' Вы:')
                        self.textBrowser.append(message['text'] + '\n')
                        self.last_timestamp = message['timestamp']
                    elif message['sender'] == self.current_receiver:
                        self.textBrowser.append(f'{dt} {message["sender"]}:')
                        self.textBrowser.append(message['text'] + '\n')
                        self.last_timestamp = message['timestamp']


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec_()
