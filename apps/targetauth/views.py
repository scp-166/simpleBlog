from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm
from django.contrib import auth
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from utils import restful


@method_decorator(csrf_exempt, name='dispatch')  # 给dispatch装饰
class DemoView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'users/login.html')

	def post(self, request, *args, **kwargs):
		try:
			# print(request.body)  # b(dict(json_data))
			ret = json.loads(request.body)
			username = ret.get('username')
			password = ret.get('password')
		except json.JSONDecodeError:
			# print(type(request.body))  # b("查询字符字符串")
			username = request.POST.get('username')
			password = request.POST.get('password')

		context = {
			'username': username,
			'password': password,
		}
		return JsonResponse(context)


class LoginView(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'targetauth/login.html')

	def post(self, request, *args ,**kwargs):
		form = LoginForm(request.POST)

		if form.is_valid():
			remember = form.cleaned_data.get('remember')
			user = form.cleaned_data.get('user')  # 验证成功是会返回user对象的

			if user is None:
				return restful.param_error("不存在该用户")
			else:
				if user.is_active:
					auth.login(request, user)  # 会重新设置token
					if remember:
						request.session.set_expiry(None)  # 默认session保存时间
					else:
						request.session.set_expiry(0)  # 浏览器关闭即终止
					return restful.ok()
				else:
					return restful.un_auth("你的账号被锁定了")

		else:
			errors = form.get_errors()
			return restful.param_error(message=errors)


def logout(request):
	"""
	注销
	:param request:
	:return:
	"""
	auth.logout(request)
	return redirect(reverse('home'))


def token(request):
	"""
	根据request是否设置了csrf_cookies，返回相应csrf_token且设置csrf_cookies
	:param request:
	:return: jsonReponse({'csrftoken': old or new csrf_token})
	"""
	if "CSRF_COOKIE" in request.META:
		return JsonResponse({'csrftoken': request.META['CSRF_COOKIE']})
	else:
		token = get_token(request)
		return JsonResponse({'csrftoken': token})
