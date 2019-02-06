from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogCategory
from django.core.paginator import Paginator
from django.conf import settings
from utils.read_statistic_method import read_statistic_once_by_cookies


def get_blog_list_common_data(request, blogs):
	"""
	根据传入来的QuerySet对象blogs进行分页
	:param request: 原样请求
	:param blogs: QuerySet对象
	:return: dict() 有以下键值对
		"blogs": Page() 根据request.GET获得查询字符串page获得的实际的Page对象
		"blog_categoryes": QuerySet 获得全部的BlogCategory，对字段blog_set进行懒惰查询处理，后期可以添加缓存中进行处理(几乎都要用到)
		"arround_page_num": list() 根据当前页索引，设置左右范围
		"blog_dates": dict() 根据降序的月份作为键，对应月份的博客数作为值
	"""
	paginator = Paginator(blogs, settings.PAGE_NUM)  # 10是一页多少项
	page_num = request.GET.get("page", 1)  # 需要查找第几页，默认1
	page = paginator.get_page(page_num)  # 实际的页，内容是models， 无需关心page_num是否字符串或数字

	paginator_page_range = paginator.page_range  # 页面的区间，返回range(), 如果有三页，则返回range(1,4)
	paginator_num_pages = paginator.num_pages  # 一共可以分成多少页

	# 根据当前页，设置左右页码索引
	# 假设左右n(page.number-NEAR_RANGE)个，则一共2n+1个页， 页码索引要求从1到最后
	# 要求i在页码区间内，不然会出现负数啥的
	arround_page_num = [i for i in range(page.number-settings.NEAR_RANGE,
	                                     page.number+settings.NEAR_RANGE+1) if i in paginator_page_range]

	# 加上省略页码
	if arround_page_num[0] >= settings.NEAR_RANGE:  # 如果首个值大于范围最小，则添加省略页码
		arround_page_num.insert(0, "...")
	if arround_page_num[-1] <= paginator_num_pages - settings.NEAR_RANGE + 1:  # 如果最大值小于范围最大
		arround_page_num.append("...")

	# 加上首页和尾页
	if arround_page_num[0] != 1:  # 如果不是从1开始，则添加首页1
		arround_page_num.insert(0, 1)
	if arround_page_num[-1] != paginator_num_pages:  # 如果末尾不是最后一页，添加末尾页
		arround_page_num.append(paginator_num_pages)

	# 按照时间算博客篇数
	blog_dates = Blog.objects.dates("create_time", "month", order="DESC")  # 获得降序的月份
	blog_dates_dict = dict()
	for blog_date in blog_dates:
		blog_count = Blog.objects.filter(create_time__year=blog_date.year,  # 按照datetime__对应属性=blog_date对应属性
		                                 create_time__month=blog_date.month).count()
		blog_dates_dict[blog_date] = blog_count

	context = {
		"blogs": page,
		"blog_categories": BlogCategory.objects.all().prefetch_related("blog_set"),  # 博客分类。提前缓存
		"arround_page_num": arround_page_num,
		"blog_dates": blog_dates_dict,
	}
	return context


def blog_list(request):
	"""
	初始博客列表
	:param request:
	:return:
	"""
	blogs = Blog.objects.all()
	context = get_blog_list_common_data(request, blogs)
	return render(request, "blog/blog_list.html", context=context)


def get_blog_with_category(request, blog_category_id):
	"""
	根据分类获得的博客列表
	:param request:
	:param blog_category_id:
	:return:
	"""
	blog_type = get_object_or_404(BlogCategory, pk=blog_category_id)  # 根据查询字符串获得分类

	blogs = Blog.objects.filter(type_name=blog_type)

	context = get_blog_list_common_data(request, blogs)

	return render(request, 'blog/blog_list.html', context)


def get_blog_with_date(request, year, month):
	"""
	根据日期获得博客列表
	:param request:
	:param year:
	:param month:
	:return:
	"""
	blogs = Blog.objects.filter(create_time__year=year, create_time__month=month)  # 根据查询字符串获得博客QuerySet
	context = get_blog_list_common_data(request, blogs)

	return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
	blog = get_object_or_404(Blog, pk=blog_pk)
	# 给阅读数加一
	read_statistic_once_by_cookies(request, blog)

	context = {
		# Blog是倒序的，找到前一篇就是找比当前博客时间早的， 选集合中的最后一篇
		'previous_blog': Blog.objects.filter(type_name=blog.type_name, create_time__gt=blog.create_time).last(),
		# Blog是倒序的，找到后一篇就是找比当前博客时间晚的，选集合中的第一篇
		'next_blog': Blog.objects.filter(type_name=blog.type_name, create_time__lt=blog.create_time).first(),
		'blog': blog,
	}

	# 设置cookies
	response = render(request, 'blog/blog_detail.html', context)
	response.set_cookie("blog_{}_read".format(blog_pk), "true")  # 浏览器关闭即删除cookies
	return response
