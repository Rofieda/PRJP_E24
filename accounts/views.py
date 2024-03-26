from ast import Expression
from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail


from accounts.serializers import UserRegisterSerializer, LoginSerializer, AddUserSerializer, UserSerializer, \
    PasswordResetRequestSerializer, SetNewPasswordSerializer
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework.generics import DestroyAPIView
from .permissions import IsAdminUser
class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
        full_name = f"{user.first_name} {user.last_name}"  # Access attributes using dot notation
        message = f'Bonjour {full_name},\n\nVous avez été ajouté au labo LMCS avec succès.'
        from_email = 'your_email@example.com'  # Set your sender email here
        to_email = user.email  # Access email attribute using dot notation
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
        return Response(response_data, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    def post(self, request):
        # Perform logout actions here
        # For example, clear user session
        request.session.clear()

        # Optionally, you can also perform other cleanup tasks

        return Response({"detail": "Déconnexion réussie.."}, status=status.HTTP_200_OK)



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
        full_name = f"{user.first_name} {user.last_name}"  # Access attributes using dot notation
        message = f'Bonjour {full_name},\n\nVous avez été ajouté à LMCSQUEST avec succès. Pour vous connecter, utilisez simplement cette adresse e-mail et utilisez les deux premières lettres de votre prénom comme mot de passe : LMCS_lesdeuxpremiereslettredevotreprenomenminiscule.'
        from_email = 'your_email@example.com'  # Set your sender email here
        to_email = user.email  # Access email attribute using dot notation
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

class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            # Check if the user sending the request is a superuser or has an admin role
            if request.user.is_superuser or (request.user.role == 'admin' and request.user != user):
                user.delete()
                return Response({"detail": "L'utilisateur a été supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Vous n'avez pas la permission de supprimer cet utilisateur."},
                                status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Nous vous avons envoyé un lien pour réinitialiser votre mot de passe'}, status=status.HTTP_200_OK)
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
        return Response({'success':True, 'message':"La réinitialisation du mot de passe a réussi"}, status=status.HTTP_200_OK)
