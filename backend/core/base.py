from rest_framework.views import exception_handler
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import pagination
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.conf import settings
import os


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


class EmailSender:
    def __init__(self, user):
        self.user = user
        self.email = user.email
        self.from_email = settings.DEFAULT_FROM_EMAIL

    def build_html_content(self, template, otp=None):
        context = {
            "user": self.user,
            "otp": otp,
            "now_year": datetime.now().year,
            "from_email": self.from_email,
        }
        return render_to_string(template, context)

    def send_email(
        self,
        otp,
        subject="Your OTP for BluCygnus Signup",
        template="accounts/signup_email.html",
    ):
        try:
            html_content = self.build_html_content(template=template, otp=otp)
            text_content = f"Hello {self.user.first_name}, your OTP for BluCygnus signup is {otp}. It is valid for 30 minutes."

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[self.user.email],
            )
            email.attach_alternative(html_content, "text/html")

            logo_path = os.path.join(settings.BASE_DIR, "static", "logo.png")
            with open(logo_path, "rb") as logo_file:
                logo = MIMEImage(logo_file.read(), _subtype="png")
                logo.add_header("Content-ID", "<company_logo>")
                email.attach(logo)

            email.send()
            logger.info(f"Signup OTP email sent to {self.user.email}")
            return True
        except Exception as e:
            logger.exception(
                f"Error sending signup OTP email to {self.user.email}: {str(e)}"
            )
            return False


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
