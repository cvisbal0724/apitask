from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
	# page_size = 100
	page_size_query_param = 'page_size'
	# max_page_size = 1000
	def get_paginated_response(self, data):		
		paginacion = {	
			'total': self.page.paginator.num_pages, # self.page.paginator.count,		
			'per_page': self.page.paginator.per_page,
			'current_page': self.page.number,
			'total_pages': self.page.paginator.num_pages,
			'last_page': self.page.paginator.num_pages,
			'next_page_url': self.get_next_link(),
			'prev_page_url': self.get_previous_link(),			
			'data': data['data']
		}
		# respuesta=Estructura.success(message, paginacion)
		data['data']=paginacion	
		return Response(data)