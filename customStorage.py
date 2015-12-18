from django.conf import settings
from django.core.files.storage import Storage

#modules for RPC operations
from grpc.beta import implementations
import sys
import manager_django_pb2
import time

_TIMEOUT_SECONDS = 100




class MyStorage(Storage):
	def __init__(self, option=None):
		if not option:
			option = settings.CUSTOM_STORAGE_OPTIONS
	def _open(self, name, mode='rb'):
		print "####CALLED SAVE####"



		return name

	def _save(self, name, content):
		print "####CALLED SAVE####"
		#content is a subclass of Django File object
		#https://docs.djangoproject.com/en/1.9/ref/files/file/
		
		#should make into format [user/resume/text.txt, timeStampInEpoch]
		
		fileName = str(content).split("@")

		file_path = name[0]
		timeStamp = name[1]

		#THIS IS THE FUNCTION CALL TO THE MANAGER VIA RPC
		filePath = self.sendFile(content, file_path, timeStamp)

		#You need to return the save URL
		return file_path

	#dummy implementation
	def get_available_name(self, name):
		return name
	#dummy implementation
	def url(self, name):
		return name

	#call to the manager via RPC
	def sendFile(self, transferFile, filePath, timeStamp):
		print "Sending file to Manager"

		transferFile.open(mode='rb') 
		hello = transferFile.read()

		channel = implementations.insecure_channel('localhost', 50050)
		stub = manager_django_pb2.beta_create_Manager_stub(channel)

		response = stub.SaveFile(manager_django_pb2.SaveRequest(save_file=hello, save_path=filePath, timestamp=timeStamp), _TIMEOUT_SECONDS)

		#print response.transfer_status
		# print transferFile
		# print type(transferFile)
		# print "ATTEMPTING CONVERSION"
		# # print str(transferFile)
		

		# print hello

		return filePath




