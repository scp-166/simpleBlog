"""
haystack
给需要的模型所属的app下新建该文件，创建索引类
"""
from haystack import indexes
from .models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
	# text是默认需要的， 修改需要在settings中修改
	text = indexes.CharField(document=True, use_template=True)

	def get_model(self):  # 为那个模型服务
		return Blog

	def index_queryset(self, using=None):  # 模型提取的时候提取什么值，这里提取全部
		return self.get_model().objects.all()
