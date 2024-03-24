from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail


from accounts.serializers import UserRegisterSerializer, LoginSerializer, \
    PasswordResetRequestSerializer, SetNewPasswordSerializer, AddUserSerializer, UserSerializer
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from .models import User
from .permissions import IsAdminUser




class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            role = request.data.get('role')
            user = serializer.save()

            # Send email notification
            self.send_signup_email(user)

            user_data = serializer.data
            return Response({
                'data': user_data,
                'message': 'vous êtes inscrit au lmcs'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_signup_email(self, user):
        subject = 'Bienvenue à LMCS'
        full_name = f"{user.first_name} {user.last_name}"
        message = f'Bonjour {full_name},\n\nVous avez été ajouté au labo LMCS avec succès.'
        from_email = 'your_email@example.com'  # Set your sender email here
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # Extract the user's role from the validated data
        role = serializer.validated_data.get('role')
        # Add the role to the response data
        response_data = serializer.data
        response_data['role'] = role
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST


class PasswordResetConfirm(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':"password reset is succesful"}, status=status.HTTP_200_OK)


class TestingAuthenticatedReq(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'msg': 'its works'
        }
        return Response(data, status=status.HTTP_200_OK)




class LogoutAPIView(APIView):
    def post(self, request):
        # Perform logout actions here
        # For example, clear user session
        request.session.clear()

        # Optionally, you can also perform other cleanup tasks

        return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)




class AddUserView(CreateAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not (self.request.user.is_superuser or self.request.user.role == 'admin'):
            raise PermissionDenied("Vous n'avez pas la permission d'effectuer cette action.")
        user = serializer.save()

        # Envoyer un email à l'utilisateur ajouté
        self.send_email_to_user(user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def send_email_to_user(self, user):
        subject = 'Bienvenue à LMCS'
        full_name = f"{user.first_name} {user.last_name}"
        message = f'Bonjour {full_name},\n\nVous avez été ajouté au labo LMCS avec succès.'
        from_email = 'votre_email@example.com'  # Remplacez par votre adresse e-mail
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])


class ListUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Vous n'êtes pas authentifié."}, status=401)

        if request.user.is_superuser or request.user.role in ['admin', 'assistant']:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Vous n'avez pas la permission d'effectuer cette action."}, status=403)



