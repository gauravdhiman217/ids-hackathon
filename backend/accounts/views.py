from core.base import EmailSender
from .models import User, Roles
from .serializers import UserSerializer, RoleSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, logout
from django.views.generic import TemplateView
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from random import randint
from datetime import datetime, timedelta


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Call the original refresh method
        response = super().post(request, *args, **kwargs)

        # Update last_login field
        try:
            access_token = response.data.get("access")
            if access_token:
                # Decode the token to get the user
                token = AccessToken(access_token)
                user_id = token["user_id"]

                # Get the user instance and update the last_login
                user_instance = User.objects.get(id=user_id)
                user_instance.last_login = timezone.now()
                user_instance.save(update_fields=["last_login"])
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response


"""
Admin Login
"""


class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect("accounts:web_login")


"""
SignUp Api
"""


class SignupApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Define permissions based on action
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


class SignupApiView1(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data.get("first_name"):
                return Response(
                    {
                        "message": "Please enter first name",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("last_name"):
                return Response(
                    {
                        "message": "Please enter last name",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("mobile_no"):
                return Response(
                    {
                        "message": "Please enter mobile number",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("email"):
                return Response(
                    {
                        "message": "Please enter email",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("password"):
                return Response(
                    {
                        "message": "Please enter password",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create(
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                email=request.data.get("email"),
                mobile_no=request.data.get("mobile_no"),
                password=make_password(request.data.get("password")),
                role=request.data.get("role_id"),
                gender=request.data.get("gender"),
            )
            data = UserSerializer(user, context={"request": request}).data
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_201_CREATED,
                    "message": "User Registered Successfully",
                    "data": data,
                }
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "User not Registered Successfully",
                    "info": str(e),
                }
            )


class LoginApiView(APIView):
    """
    This LoginApiView class handles user login.

    Only Admin users can log in. The API validates credentials,
    checks account status, and returns tokens upon successful login.
    Methods:
        post(request): Handles admin login.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("email"):
            return Response(
                {"message": "Please enter email", "status": status.HTTP_400_BAD_REQUEST}
            )
        if not request.data.get("password"):
            return Response(
                {"message": "Please enter password"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=request.data.get("email"), password=request.data.get("password")
        )

        if not user:
            return Response(
                {
                    "message": "Invalid Login Credentials.",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # if not user.role or user.role.name != "Admin":
        #     return Response({"message": "Only Admin users can log in."}, status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            user.otp = str(randint(100000, 999999))
            user.otp_expires_at = datetime.now() + timedelta(minutes=30)

            user.save()
            email_sender = EmailSender(user)
            email_sender.send_email(otp=user.otp)
            return Response(
                {
                    "message": "Your email is not verified. Please verify your email Otp resend again to registered email.",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "is_verified": False,
                }
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        data = UserSerializer(user, context={"request": request}).data
        data.update(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )

        return Response(
            {
                "status": True,
                "status_code": status.HTTP_200_OK,
                "message": "Logged In Successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class LogOutView(APIView):
    """
    Logout Api
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # refresh_token = request.headers.get('Authorization').split()[1]
            user = request.user
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
            refesh_token = request.data.get("refresh_token")
            token = RefreshToken(refesh_token)
            token.blacklist()
            logout(request)
            request.session.flush()
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_202_ACCEPTED,
                    "message": "Logged out Successfully",
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad request",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class TestingResponse(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello World"}, status=status.HTTP_200_OK)


class RoleView(ListAPIView):
    serializer_class = RoleSerializer
    queryset = Roles.objects.all()


class ForgotPasswordRequestOtpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response(
                {"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"message": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate OTP
        user.otp = str(randint(100000, 999999))
        user.otp_expires_at = datetime.now() + timedelta(minutes=30)
        user.save()

        email_sender = EmailSender(user)
        email_sender.send_email(
            otp=user.otp,
            subject="Password Reset OTP",
            template="accounts/reset_pwd_email.html",
        )

        return Response(
            {
                "status": True,
                "status_code": status.HTTP_200_OK,
                "message": "OTP has been sent to your email.",
            },
            status=status.HTTP_200_OK,
        )


class ForgotPasswordVerifyOtpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        if not email or not otp:
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Email and OTP are required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "User with this email does not exist."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.otp != otp:
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid OTP."
                },
                status=status.HTTP_400_BAD_REQUEST
            )   
        if user.otp_expires_at < timezone.now():
            return Response(
                {"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST
            )
        if new_password:
            user.password = make_password(new_password)
            user.otp = None
            user.otp_expires_at = None
            user.save()
            return Response(
                {
                    "status": True,
                    "status_code": status.HTTP_200_OK,
                    "message": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )


class VerifyOtpView(APIView):
    """
    This VerifyOtpView class handles OTP verification.

    Users can verify their OTP for login or registration. The API validates the
    provided email and OTP, checks for expiry, and activates the user account
    upon successful verification.

    Methods:
        post(request): Handles OTP verification.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        user_email = request.data.get("email")
        otp_sent = request.data.get("otp")

        if not user_email or not otp_sent:
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Please provide both email and OTP.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=user_email).first()
        if not user:
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Invalid User email provided! Please provide a correct email.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.otp != otp_sent:
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Invalid OTP provided!",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if OTP is expired
        if timezone.now() > user.otp_expires_at:
            user.otp = None
            user.otp_expires_at = None
            user.save()
            return Response(
                {
                    "status": False,
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "OTP has expired. Please Regenerate Again!",
                    "is_verified": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save()

        serializer = UserSerializer(user)
        return Response(
            {
                "status": True,
                "status_code": status.HTTP_200_OK,
                "message": "User verified successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
