from django.shortcuts import render
from django.contrib.contenttypes.fields import ContentType
from utils.read_statistic_method import get_week_read_data, get_today_hot_data, get_yesterday_hot_data, get_7_hot_data
from apps.blog.models import Blog
from django.core.cache import cache


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)

	# 获得前七天日期和对应的阅读量
	dates, read_statistics_total_list = get_week_read_data(blog_content_type)
	today_hot_data = get_today_hot_data(blog_content_type)
	yesterday_hot_data = cache.get('yesterday_hot_data')
	if yesterday_hot_data is None:
		cache.set('yesterday_hot_data', get_yesterday_hot_data(blog_content_type), 10)

	seven_days_hot_data = cache.get('seven_days_hot_data')
	if seven_days_hot_data is None:
		cache.set('seven_days_hot_data', get_7_hot_data(blog_content_type), 10)

	context = {
		'dates': dates,
		'read_statistics_total': read_statistics_total_list,
		'today_hot_data': today_hot_data,
		'yesterday_hot_data': yesterday_hot_data,
		'seven_days_hot_data': seven_days_hot_data,
	}
	return render(request, 'home.html', context)

#  传统搜索
# from django.db.models import Q
# from apps.blog.views import get_blog_list_common_data
# def search(request):
# 	q = request.GET.get('q')
# 	context = {}
# 	if q:
# 		blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
# 		context = get_blog_list_common_data(request, blogs)
#
# 	return render(request, 'blog/blog_list.html', context)

