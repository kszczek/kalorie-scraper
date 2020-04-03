from requests.exceptions import RequestException
from contextlib import closing
import logging
import requests


def simple_get(url):
    try:
        with closing(requests.get(url, stream=True)) as response:
            if is_html(response):
                return response.content
            else:
                return None
    except RequestException as e:
        logging.info('GET request to {} failed'.format(url))
        logging.exception(e)


def is_html(response):
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)