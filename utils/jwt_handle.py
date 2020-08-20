# -*- coding: utf-8 -*-
import datetime


def jwt_response_payload_handler(token, user=None, request=None):
    user.last_login = str(datetime.datetime.today())
    user.save()
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }
