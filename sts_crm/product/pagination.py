from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'current_page':self.page.number,
            'total_pages':self.page.paginator.num_pages,
            'items_page' : len(self.page),
            'results': data
        })