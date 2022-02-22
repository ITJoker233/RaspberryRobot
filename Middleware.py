
class Middleware(object):
	def __init__(self):
		self.middlewares = {}

	def add(self, func):
		self.middlewares[func.__class__.__name__] = func

	def remove(self,func):
		del self.middlewares[func.__class__.__name__]
  
	def handle(self, context):
		for func in self.middlewares:
			if not func.handle(context): break

middleware = Middleware()