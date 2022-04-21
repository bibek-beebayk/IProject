from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, status
from .serializers import UserSerializer, ChangePasswordSerializer
from .models import User

# Create your views here.

class RegisterView(CreateAPIView):
    '''Endpoint for User Registration'''
    # def post(self, request):
    #     serializer = UserSerializer(data = request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    serializer_class = UserSerializer

class LoginView(APIView):
    '''Endpoint for User Login'''
    def post(self, request):
        print(request.data)
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User Not Found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')

        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        return Response(
            {
                'message': 'Success'
            }
        )

class ListUserView(ListCreateAPIView):
    '''Endpoint for viewing all users in the system and creating new users.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class ChangePasswordView(UpdateAPIView):
    '''Endpoint for Changing Password'''
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        # print(vars(obj))
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'message': 'You entered a wrong existing password.'}, status=status.HTTP_400_BAD_REQUEST)

            if not request.data.get('new_password') == request.data.get('new_password_confirm'):
                return Response({'message': 'New Password does not match the Confirmation password.'}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status':'success',
                'code': status.HTTP_200_OK,
                'message': 'Password Updated Successfully',
                'data': []
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def logout_user(request):
#     logout(request)
#     return Response('Seccessfully Logged Out.')

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({
            'message': 'Successfully Logged Out.'
        })