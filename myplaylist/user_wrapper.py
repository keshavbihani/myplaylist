class UserWrapper():

	def __init__(self, user_info):
		self.user_id = user_info['id']
		self.username = user_info['username']
		self.roles = user_info['roles']

	@classmethod	
	def get_user_object(cls,user_info):
		return UserWrapper(user_info)	