import datetime
from django.utils import timezone
from django.contrib.contenttypes.fields import ContentType
from apps.blog.models import Blog
from apps.read_statistics.models import ReadTimes, ReadDetail
from django.db.models import Sum, F


def read_statistic_once_by_cookies(request, obj):
    """
    根据有无cookies来添加被阅读次数
    :param request: 视图函数的request
    :param obj: 和ReadTimes有关联的模型实例化对象，比如Blog的实例化对象
    :return: set_cookies()时的控制字符串
    """
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_{}_read".format(ct.model, obj.pk)
    if not request.COOKIES.get(key):
        # 总阅读数+1
        read_times = ReadTimes.objects.filter(content_type=ct, object_id=obj.pk)
        if read_times.exists():
            read_times.update(read_times=F("read_times")+1)
        else:
            ReadTimes.objects.create(content_type=ct, object_id=obj.pk, read_times=1)

        # 当天(详细)阅读数+1
        date = timezone.now().date()

        read_detail = ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date)
        if read_detail.exists():
            read_detail.update(read_number=F("read_number")+1)
        else:
            ReadDetail.objects.create(content_type=ct, object_id=obj.pk, date=date, read_number=1)

    else:
        print("cookies被设置")

    return key


def get_week_read_data(content_type):
    """
    获取一个星期的访问量
    :param content_type: 与ReadDetail相关的模型实例
    :return: tupe(list(), list())  分别是日期和对应日期的阅读数
    """
    today = timezone.now().date()
    read_times_total_list = []  # 保存每天的访问总数
    dates = []  # 保存各日期，给前端使用
    for i in range(6, -1, -1):  # 获取前七天(包括今天)

        date = today - datetime.timedelta(days=i)  # 取得前第i天
        dates.append(date.strftime("%m/%d"))  # 前端要求字符串

        read_detail = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_detail.aggregate(read_number_total=Sum("read_number"))  # 分组统计，统计命名为read_times_total
        read_times_total_list.append(result["read_number_total"] or 0)

    return dates, read_times_total_list


def get_today_hot_data(content_type):
    """
    获得当天的访问量排名
    :param content_type:
    :return:
    """
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by("-read_number")  # 倒序排列
    return read_details[:5]


def get_yesterday_hot_data(content_type):
    """
    获得昨天的访问量排名
    :param content_type:
    :return:
    """
    today = timezone.now().date()
    date = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=date).order_by("-read_number")
    print(type(read_details))
    return read_details[:5]


def get_7_hot_data(content_type):
    """
    获得前七天的访问量排名
    :param content_type:
    :return:
    """
    today = timezone.now().date()
    date = today - timezone.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lte=today, read_details__date__gt=date).values("id", "title") \
                        .annotate(read_number_total=Sum("read_details__read_number")) \
                        .order_by("-read_number_total")  # 访问量按照从大到小排
    print(type(blogs))
    return blogs[:5]

