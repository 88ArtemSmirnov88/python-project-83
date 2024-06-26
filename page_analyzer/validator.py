from urllib.parse import urlparse
from validators.url import url as url_validator


def validate(url):
    errors = []
    if len(url) > 255:
        errors.append('URL превышает 255 символов')
    if not url_validator(url):
        errors.append('Некорректный URL')
    if not url:
        errors.append('URL обязателен')
    return errors


def normalize(url):
    output = urlparse(url)
    scheme = output.scheme.lower()
    netloc = output.netloc.lower()
    return f'{scheme}://{netloc}'
