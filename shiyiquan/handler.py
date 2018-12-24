from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
import logging

logger = logging.getLogger('quan-logger')

class UploadProgressCachedHandler(FileUploadHandler):
	"""
		Tracks progress for mutiple file uploads.
		The http post request must contain a header or query parameter, 'X-Progress-ID'
		which should contain a unique string to identify the upload to be tracked.
	"""

	def __init__(self, request=None):
		super(UploadProgressCachedHandler, self).__init__(request)
		self.progress_id = None
		self.cache_key = None
		self.queue = []

	def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
		self.content_length = content_length
		self.progress_id = self.request.GET.get('X-Progress-ID')
		addr = self.request.META['REMOTE_ADDR']
		if self.progress_id:
			self.cache_key = "loading_%s_%s" % (addr, self.progress_id)
			cache.set(self.cache_key, self.queue)

	def new_file(self, field_name, file_name, content_type, content_length, charset, content_type_extra):
#		logger.error('new_file ' + file_name + ' size ' + str(content_length))
		file_struct = {
			'serial': len(self.queue),
			'size': 0,
		}
		self.queue.append(file_struct)

	def receive_data_chunk(self, raw_data, start):
		tail = len(self.queue) - 1
		self.queue[tail]['size'] += self.chunk_size
		if self.cache_key:
			cache.set(self.cache_key, self.queue)
		return raw_data
	
	def file_complete(self, file_size):
#		logger.error('file_comp with size ' + str(file_size))
		tail = len(self.queue) - 1
		self.queue[tail]['size'] = -1
		if self.cache_key:
			cache.set(self.cache_key, self.queue)

	def upload_complete(self):
	#	logger.error('upload_complete\n' + str(self.queue)+'\n')
		if self.cache_key:
#			cache.set(self.cache_key, self.queue)
#			cache.delete(self.cache_key)
			pass


