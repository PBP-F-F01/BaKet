# pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'limit': self.get_page_size(self.request),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'results': data
        })
    
class ReplyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'limit': self.get_page_size(self.request),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'next_page': self.get_next_link(),
            'previous_page': self.get_previous_link(),
            'results': data
        })