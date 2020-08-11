from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import arrow
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'{self.username}'


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.timestamp} {self.username} {self.text}'


class PrivateMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    receiver = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.Float, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.timestamp} {self.sender} {self.text}'


@app.route('/')
def hello():
    return 'Hello! Это мой мессенджер. Его <a href="/status">статус</a>'


local_start = arrow.now()


@app.route('/status')
def status():
    local_now = arrow.now()
    return {
        'status': 'OK',
        'name': 'Bereg Messenger',
        'messages_count': len(Messages.query.all()),
        'private_messages_count': len(PrivateMessages.query.all()),
        'users_count': len(User.query.all()),
        'server_curr_time': local_now.format('HH:mm:ss'),
        'server_start_time': local_start.format('HH:mm:ss'),
    }


@app.route('/log_in')
def log_in():
    username = request.json['username']
    password = request.json['password']
    choice = request.json['choice']
    if choice == 'autorisation':
        if username in (str(i) for i in User.query.all()):
            user = User.query.filter_by(username=username).first()
            if password != user.password:
                return {'status': 'Неправильный пароль'}
            return {'status': 'Все четко', 'username': username}
        else:
            return {'status': 'Неправильный логин'}
    else:
        if username in (str(i) for i in User.query.all()):
            return {'status': 'Имя занято'}
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return {'status': 'Все четко', 'username': username}


@app.route('/send_message')
def send_message():
    username = request.json['username']
    receiver = request.json['receiver']
    text = request.json['text']

    # user_id = User.query.filter_by(username=username).first()
    if receiver == 'Общий чат':
        new_message = Messages(username=username,
                               text=text,
                               timestamp=time.time()
                               ) # user_id=user_id.id)
        db.session.add(new_message)
        db.session.commit()
    else:
        new_private_message = PrivateMessages(sender=username,
                                              receiver=receiver,
                                              text=text,
                                              timestamp=time.time()
                                              )
        db.session.add(new_private_message)
        db.session.commit()
    # messages.append({'username': username, 'text': text, 'timestamp': time.time()})

    return {'OK': True}


@app.route('/get_messages')
def get_messages():
    after = float(request.args['after'])
    receiver = request.json['receiver']

    result = []
    if receiver == 'Общий чат':
        for message in Messages.query.all():
            if message.timestamp > after:
                result.append({'username': message.username,
                               'text': message.text,
                               'timestamp': message.timestamp
                               })
    else:
        for message in PrivateMessages.query.all():
            if message.timestamp > after:
                result.append({'sender': message.sender,
                               'receiver': message.receiver,
                               'text': message.text,
                               'timestamp': message.timestamp
                               })

    return {
        'messages': result
    }

if __name__ == "__main__":
    app.run()
