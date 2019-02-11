from django.db import models
# from django.contrib.auth.models import User  # use new User
from apps.targetauth.models import User
# from ckeditor_uploader.fields import RichTextUploadingField  # used ckeditor
from apps.read_statistics.Mixin import ReadTimeExpandMixin
from apps.read_statistics.models import ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField


class BlogCategory(models.Model):
	type_name = models.CharField(verbose_name="博客分类", max_length=10)

	def __str__(self):
		return self.type_name

	class Meta:
		verbose_name = "博客分类"
		verbose_name_plural = "博客分类"


class Blog(models.Model, ReadTimeExpandMixin):
	title = models.CharField(verbose_name="标题", max_length=50)
	content = MDTextField(verbose_name="内容")
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
	create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
	last_updated_time = models.DateTimeField(verbose_name="最后更新时间", auto_now=True)
	type_name = models.ForeignKey("BlogCategory", on_delete=models.CASCADE, verbose_name="博客分类")
	# ReadDetail使用了contenttype将Blog和自身关联，这里可以使用GenericRelation来翻转获得信息
	# 注意， 不用迁移数据库
	read_details = GenericRelation(ReadDetail, verbose_name="访问详情")

	def __str__(self):
		return "<blog>: {}".format(self.title)

	class Meta:
		verbose_name = "博客"
		verbose_name_plural = "博客"
		ordering = ['-create_time']
