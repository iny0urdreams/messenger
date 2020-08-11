from server import db, User, Messages, PrivateMessages
import time, arrow

a = arrow.get(time.time())
print(a)

# admin_mes = Messages(username='admin', text='sad', timestamp=1.0)
# # admin_us = User(username='admin', password='123')
# admin_mes = Messages.query.filter_by(username='admin').first()
# db.session.delete(admin_mes)
# db.session.commit()
# db.session.add(admin_mes)
# db.session.commit()
# a = [i.username for i in User.query.all()]
# # usernames = [i.username for i in a]
# # print(usernames)
# # db.session.add(admin)
# # db.session.commit()
# a = len([i.username for i in User.query.all()])
# if User.query.filter_by(username='peter').first():
#     print('yes')
# print(User.query.all()[-1])

# print(len(User.query.all()))
# for i in Messages.query.all():
#     print(i.username)
#     print(type(i.timestamp))
#
# for i in User.query.all():
#     print(type(i.username))
#     print(i.password)
# a = 'Idar'
# if a in (str(i) for i in User.query.all()):
#     print('yes')
#
# print([str(i) for i in User.query.all()])
# pet = User.query.filter_by(id=1).first()
# print(pet.username)