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
		print "####CALLED OPEN####"

		fileName = name.split("@")

		file_path = fileName[0]
		timeStamp = fileName[1]

		#THIS IS THE FUNCTION CALL TO THE MANAGER VIA RPC. It should return a file.
		fileContent = self.readFile(file_path, timeStamp)
		
		return fileContent

	def _save(self, name, content):
		print "####CALLED SAVE####"
		#content is a subclass of Django File object
		#https://docs.djangoproject.com/en/1.9/ref/files/file/

		#should make into format [user/resume/text.txt, timeStampInEpoch]
		
		fileName = str(content).split("@")

		file_path = fileName[0]
		timeStamp = fileName[1]

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

	#sendFile to the manager via RPC
	def sendFile(self, transferFile, filePath, timeStamp):
		print "Sending file to Manager"

		transferFile.open(mode='rb') 
		hello = transferFile.read()

		channel = implementations.insecure_channel('localhost', 50050)
		stub = manager_django_pb2.beta_create_Manager_stub(channel)

		response = stub.SaveFile(manager_django_pb2.SaveRequest(save_file=hello, save_path=filePath, timestamp=long(timeStamp)), _TIMEOUT_SECONDS)

		#print response.transfer_status
		# print transferFile
		# print type(transferFile)
		# print "ATTEMPTING CONVERSION"
		# # print str(transferFile)
		

		# print hello

		return filePath



	#readFile from the manager via RPC
	def openFile(self, filePath, timeStamp):
		print "Reading file from Manager"


		channel = implementations.insecure_channel('localhost', 50050)
		stub = manager_django_pb2.beta_create_Manager_stub(channel)

		response = stub.OpenFile(manager_django_pb2.OpenRequest(open_path=filePath, timestamp=timeStamp), _TIMEOUT_SECONDS)

		fileContent = response.open_file

		#the response should be a file
		
		#This is just test code for saving file
		filename = os.path.basename(filePath)

		with open(filename, 'wb') as f:
			f.write(fileContent)

		#we should be returning the file
		return response
