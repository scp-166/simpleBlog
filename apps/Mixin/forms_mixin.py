"""
获取表单错误的Mixin
"""


class FormErrorMixin(object):
	def get_errors(self):
		"""
		获取form对象.errors.get_json_data()中message字段内的键值对
		:return: dict() key:错误类型 value: 错误值
		"""
		# 提取error.get_json_data()中"message"有关的信息
		if hasattr(self, 'errors'):
			errors = self.errors.get_json_data()
			new_error = {}
			for key, message_dict in errors.items():
				messages = []
				for message in message_dict:
					messages.append(message["message"])
				new_error[key] = messages
			return new_error
		else:
			return {}
