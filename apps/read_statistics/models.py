from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class ReadTimes(models.Model):
	"""
	可复用的阅读数记录
	"""
	read_times = models.IntegerField(default=0)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey("content_type", "object_id")

	class Meta:
		verbose_name = "阅读数"
		verbose_name_plural = "阅读数"


class ReadDetail(models.Model):
	"""
	一天的详细的访问记录
	"""
	date = models.DateField(default=now, verbose_name="访问时间")  # 传的是函数引用
	read_number = models.IntegerField(default=0, verbose_name="访问次数")

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey("content_type", "object_id")

	class Meta:
		verbose_name = "访问详情"
		verbose_name_plural = "访问详情"
