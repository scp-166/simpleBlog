"""
返回JsonResponse数据，内容为
{
	"code": "状态码",
	"message": "错误信息",
	"data": "需要传输的数据",
	[
	"other": "可选 需要传输的其他内容"
	]
}
"""
from django.http import JsonResponse


class HttpCode(object):
	"""
	存储状态码(类似Http状态码格式)
	"""
	ok = 200
	params_error = 400
	un_auth = 401
	method_error = 405
	server_error = 500


def result(code=HttpCode.ok, message='', data=None, other=None):
	"""
	封装JsonResponse()， 默认状态码为200， 信息为空， 数据为None， 其他信息为None
	:param code: HttpCode类内存储的状态码，默认为200
	:param message: 信息字段，默认为空
	:param data: 数据字段，默认为None
	:param other: 其他字段，默认为None
	:return: 包含以上内容的JsonResponse()
	"""
	json_code = {'code': code, 'message': message, 'data': data,}  # 至少包含三个字段
	if other and isinstance(other, dict) and other.keys():  # 如果有other字段。且为字典。且有键。
		json_code.update(other)  # 添加该other字段
	return JsonResponse(json_code,  json_dumps_params={'ensure_ascii': False})


def ok():
	"""
	成功时调用，纯粹只有状态码
	:return: JsonResponse({"code"=200, "message":"", "data":None})
	"""
	return result()


def param_error(message="", data=None):
	"""
	参数错误时调用
	:param message: 信息字段，内容是传入的错误信息
	:param data: 数据字段，内容传入的数据
	:return: JsonResponse({"code":400, "message"=message, "data"=data})
	"""
	return result(HttpCode.params_error, message=message, data=data)


def un_auth(message="", data=None):
	"""
	权限验证失败时调用
	:param message: 信息字段，内容是传入的错误信息
	:param data: 数据字段，内容传入的数据
	:return: JsonResponse({"code":401, "message"=message, "data"=data})
	"""
	return result(HttpCode.un_auth, message=message, data=data)


def method_error(message="", data=None):
	"""
	方法调用错误时调用
	:param message: 信息字段，内容是传入的错误信息
	:param data: 数据字段，内容传入的数据
	:return: JsonResponse({"code":405, "message"=message, "data"=data})
	"""
	return result(HttpCode.method_error, message=message, data=data)


def server_error(message="", data=None):
	"""
	服务器错误时调用
	:param message: 信息字段，内容是传入的错误信息
	:param data: 数据字段，内容传入的数据
	:return: JsonResponse({"code":500, "message"=message, "data"=data})
	"""
	return result(HttpCode.server_error, message=message, data=data)
