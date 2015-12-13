from django.conf import settings
from django.core.files.storage import Storage

class MyStorage(Storage):
	def __init__(self, option=None):
		if not option:
			option = settings.CUSTOM_STORAGE_OPTIONS
	def _open(name, mode='rb'):
		print "called open"
		return name
	def _save(name, content):
		print "called save"
		return name