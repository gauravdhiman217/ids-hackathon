from rest_framework.views import exception_handler
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import pagination


import logging

logger = logging.getLogger("backend")


def custom_exception_handler(exc, context):
    """this function is called when an exception and generated define schema of
    exception response for simplicity. it only took first exception and first message

    Args:
        exc (Exception): generated exception

    Returns:
        json: custom response data
    """

    response = exception_handler(exc, context)
    if response is not None and isinstance(response.data, dict):
        for field, errors in response.data.items():
            if isinstance(errors, list):
                response.data = {
                    "status": False,
                    "status_code": response.status_code,
                    "message": errors[0],  # Use the first error message
                    "error_field": field,
                }
                break
    return response


class BasePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "status": True,
                "status_code": status.HTTP_200_OK,
                "message": "Data fetched successfully.",
                "page_size": self.page_size,
                "page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "data": data,
            }
        )


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Custom base ViewSet to standardize response structure for all actions.
    """

    def get_queryset(self):
        """Ensure queryset is always available"""
        if not hasattr(self, "queryset") or self.queryset is None:
            raise ValueError(
                f"ViewSet {self.__class__.__name__} is missing a queryset."
            )
        return self.queryset

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "status_code": response.status_code,
                "message": "Created successfully",
                "data": response.data,
            },
            status=response.status_code,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "status_code": response.status_code,
                "message": "Updated successfully",
                "data": response.data,
            },
            status=response.status_code,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "status_code": status.HTTP_200_OK,
                "message": "Deleted successfully",
            },
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "status_code": response.status_code,
                "message": "Retrieved successfully",
                "data": response.data,
            },
            status=response.status_code,
        )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "status": True,
                "status_code": response.status_code,
                "message": "List retrieved successfully",
                "data": response.data,
            },
            status=response.status_code,
        )
