from .models import ReadTimes
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import ContentType


class ReadTimeExpandMixin(object):
	"""
	返回将自身实例作为ReadTimes模型的content_type所需的对象
	"""
	def get_read_times(self):
		try:
			# 用自身实例获得ContentType实例
			ct = ContentType.objects.get_for_model(self)
			# 获得ReadTimes实例
			read_times = ReadTimes.objects.get(content_type=ct, object_id=self.pk)
			return read_times.read_times
		except exceptions.ObjectDoesNotExist:
			return 0
