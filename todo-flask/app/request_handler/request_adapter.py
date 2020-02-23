import requests
import json
from . import setup
from .request import make_request
import time

'''
    Open a session setting a header. Header information is contained in setup.py
'''
session = requests.Session()
session.headers.update(setup.header)

'''
    This function has the responsibility to contact the API and ask for the profile JSON. Whenever a problem occurs, 
    it returns an HTTP response with an error. make_request sends an HTTP requests to url using the current session
'''


def user_request(url):
    try:
        message = make_request(session, url)
        return message
    except json.decoder.JSONDecodeError as e:
        print(' [x] Wrong username -- see requst_adapter.py\n')
        print(e)


'''
    This function has the responsibility to contact the API ask for the post JSON, that only contains information about
    the post of a given Instagram profile. time.sleep() is not mandatory but strongly recommended since a given profile 
    may have huge number of post and it's better to wait after making a request
'''


def user_media_request(url):
    message = make_request(session, url)
    time.sleep(1)
    return message


'''
    This function has the responsibility to contact the API ask for the comment JSON, that only contains information 
    about the comment of a given post. time.sleep() is not mandatory but strongly recommended since a given post 
    may have huge number of comment and it's better to wait after making a request
'''


def comment_media_request(url):
    message = make_request(session, url)
    time.sleep(1)
    return message







