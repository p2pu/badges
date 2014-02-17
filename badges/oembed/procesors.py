from urlparse import urlparse
from django.conf import settings
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def check_if_url_is_valid(url):
	""" validates oEmbed url parameter"""

	val = URLValidator(verify_exists=False)

	try:
		val(url)
	except ValidationError as e:
		print e
		return False

	domain = urlparse(url).netloc
	if domain.split('.')[0] == 'www':
		domain = '.'.join(domain.split('.')[1:])

	if domain != settings.ORGANISATION_URL:
		return False
	return True


def set_url_to_relative(url):
	if url.startswith('http://'):
		return url[5:]
	if url.startswith('https://'):
		return url[6:]
	return url