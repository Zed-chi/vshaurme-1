from flask import url_for

from vshaurme.extensions import db
from vshaurme.models import Notification


def push_follow_notification(follower, receiver):
    message = 'Пользователь подписан на вас. User <a href="%s">%s</a> followed you.' % \
              (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)


def push_comment_notification(photo_id, receiver, page=1):
    message = '<a href="%s#comments">Под этим фото появился комментарий/ответ. This photo</a> has new comment/reply.' % \
              (url_for('main.show_photo', photo_id=photo_id, page=page))
    notification = Notification(message=message, receiver=receiver)


def push_collect_notification(collector, photo_id, receiver):
    message = 'Пользователь взял ваше фото в коллекцию. User <a href="%s">%s</a> collected your <a href="%s">photo</a>' % \
              (url_for('user.index', username=collector.username),
               collector.username,
               url_for('main.show_photo', photo_id=photo_id))
    notification = Notification(message=message, receiver=receiver)
