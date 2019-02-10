from apps.Mixin.forms_mixin import FormErrorMixin
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form, FormErrorMixin):
	"""
	用户登陆的表单
	"""
	"""
	error_message该dict的键值对对应错误类型和描述，如果不设置，将使用默认的描述、且该描述使用settings.LANGUAGE_CODE设定的语言
	"""
	telephone = forms.CharField(max_length=11, error_messages={'required': '请输入手机号'})
	password = forms.CharField(max_length=20, min_length=6,
								error_messages={'max_length': '密码最长不能超过20个字符',
												'min_length': '密码最短不能少于6个字符',
												'required': '请输入密码'})
	remember = forms.IntegerField(required=False)

	def clean(self):
		telephone = self.cleaned_data.get('telephone')
		password = self.cleaned_data.get('password')
		remember = self.cleaned_data.get('remember')
		print(remember)

		user = authenticate(username=telephone, password=password)  # 仅作验证

		if user is None:
			# raise forms.ValidationError('用户名或密码不正确')
			self.cleaned_data["user"] = None
		else:
			self.cleaned_data["user"] = user

		return self.cleaned_data

